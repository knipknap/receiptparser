import re
import codecs
import datetime
import dateutil.parser
from difflib import get_close_matches

class Receipt(object):
    def __init__(self, config, filename, raw):
        """
        :type  config: munch.Munch
        :param config: Configuration as returned by config.read_config()
        :type  filename: str|None
        :param filename: Only stored in the object to ease future debugging
        :type  raw: str
        :param raw: Tesseract textual output
        """
        self.config = config
        self.filename = filename
        self.market = None
        self.date = None
        self.postal = None
        self.sum = None
        self.lines = [l.lower() for l in raw.split('\n') if l.strip()]
        self.parse()

    @classmethod
    def from_file(cls, config, filename):
        with codecs.open(filename) as fp:
            return Receipt(config, filename, fp.read())

    def for_format_string(self):
        return {
            'filename': self.filename,
            'market': self.market or 'unknown',
            'date': self.date or datetime.date(1970, 1, 1),
            'postal': self.postal or 'unknown',
            'sum': '?' if self.sum is None else self.sum,
        }

    def parse(self):
        """
        :return: void
            Parses obj data
        """

        self.market = self.parse_market()
        self.postal = self.parse_postal()
        self.date = self.parse_date()
        self.sum = self.parse_sum()

    def fuzzy_find(self, keyword, accuracy=0.6):
        """
        :param keyword: str
            The keyword string to look for
        :param accuracy: float
            Required accuracy for a match of a string with the keyword
        :return: str
            Returns the first line in lines that contains a keyword.
            It runs a fuzzy match if 0 < accuracy < 1.0
        """
        for line in self.lines:
            words = line.split()
            if re.search(r'\b'+keyword+r'\b', line, re.I):
                return line

            matches = get_close_matches(keyword, words, 1, accuracy)
            if matches:
                return line

    def parse_date(self):
        """
        :return: date
            Parses data
        """

        for line in self.lines:
            match = re.search(self.config.formats.date, line, re.I)
            if match:
                date_str = match.group(1).replace(' ', '')
                try:
                    return dateutil.parser.parse(date_str)
                except:
                    continue

    def parse_postal(self):
        """
        :return: str
        """

        for line in self.lines:
            match = re.search(self.config.formats.postal_code, line, re.I)
            if match:
                try:
                    int(match.group(1))
                except ValueError:
                    continue
                return match.group(1)

    def parse_market(self):
        """
        :return: str
        """

        for int_accuracy in range(10, 6, -1):
            accuracy = int_accuracy/10.0
            for market, spellings in self.config.markets.items():
                for spelling in spellings:
                    line = self.fuzzy_find(spelling, accuracy)
                    if line:
                        return market

    def parse_sum(self):
        """
        :return: str
        """

        for sum_key in self.config.sum_keys:
            sum_line = self.fuzzy_find(sum_key, 0.9)
            if sum_line:
                sum_line = sum_line.replace(",", ".")
                sum_float = re.search(self.config.formats.sum, sum_line)
                if sum_float:
                    return sum_float.group(0)
