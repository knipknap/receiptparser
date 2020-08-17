# !/usr/bin/python3
# coding: utf-8

# Copyright 2015-2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest
from receiptparser.config import read_config
from receiptparser.receipt import Receipt

DIRNAME = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIRNAME)
TEST_DATA_DIR = os.path.join(DIRNAME, 'data')
TEST_RECEIPTS_TXT_DIR = os.path.join(TEST_DATA_DIR, 'germany', 'txt')


class ReceiptTestCase(unittest.TestCase):
    """Tests for `parser.py`."""

    config = read_config(os.path.join(ROOT_DIR, "data", "configs", "germany.yml"))

    def test_fuzzy_find(self):
        """
            verifies fuzzy_find
        """
        test_file = os.path.join(TEST_RECEIPTS_TXT_DIR, "sample_text_fuzzy_find.txt")
        receipt = Receipt.from_file(self.config, test_file)
        self.assertIsNotNone(receipt)

        self.assertEqual("restaurant", receipt.fuzzy_find("restaurat"))
        self.assertEqual("gas station", receipt.fuzzy_find("as statio"))
        self.assertEqual("uber", receipt.fuzzy_find("ube"))
        self.assertEqual("lyft", receipt.fuzzy_find("ly"))
        self.assertEqual("supermarket", receipt.fuzzy_find("market"))

    def test_parser_date(self):
        """
            Verifies parse_date functions
            dates like 19.08.15 and 19. 08. 2015
        """
        test_file = os.path.join(TEST_RECEIPTS_TXT_DIR, "sample_text_receipt_dates.txt")
        receipt = Receipt.from_file(self.config, test_file)

        self.assertEqual(str(receipt.date), "2015-08-19 00:00:00")

        # test DD.MM.YY
        receipt2 = Receipt(self.config, "test", "18.08.16\n19.09.17\n01.01.18")
        self.assertEqual(str(receipt2.parse_date()), "2016-08-18 00:00:00")

        # test DD.MM.YYYY
        receipt3 = Receipt(self.config, "test", "18.08.2016\n")
        self.assertEqual(str(receipt3.parse_date()), "2016-08-18 00:00:00")

        # HOWEVER these tests should fail:
        # test with DD > 31
        receipt4 = Receipt(self.config, "test", "32.08.2016\n")
        self.assertEqual(receipt4.parse_date(), None)

        # test with MM > 12
        receipt5 = Receipt(self.config, "test", "01.55.2016\n")
        self.assertEqual(receipt5.parse_date(), None)

        # test with invalid date: 31.04.15
        receipt6 = Receipt(self.config, "test", "31.04.15\n")
        self.assertEqual(receipt6.parse_date(), None)

        # And these tests should pass:
        # test with YYYY < 2013
        receipt7 = Receipt(self.config, "test", "18.08.2012\n")
        actual_date_str = receipt7.parse_date()

        # test with YYYY >= 2017
        receipt8 = Receipt(self.config, "test", "18.08.2017\n")
        actual_date_str = receipt8.parse_date()

    def test_parse_market(self):
        """
            Verifies parser.parse_market
        """
        receipt = Receipt(self.config, "test", "penny")
        self.assertEqual("Penny", receipt.parse_market())

        receipt = Receipt(self.config, "test", "p e n n y")
        self.assertEqual("Penny", receipt.parse_market())

        receipt = Receipt(self.config, "test", "m a r k t gmbh")
        self.assertEqual("Penny", receipt.parse_market())

        receipt = Receipt(self.config, "test", "rew")
        self.assertEqual("REWE", receipt.parse_market())

        receipt = Receipt(self.config, "test", "REL")
        self.assertEqual("Real", receipt.parse_market())

        receipt = Receipt(self.config, "test", "netto-onli")
        self.assertEqual("Netto", receipt.parse_market())

        receipt = Receipt(self.config, "test", "kaser")
        self.assertEqual("Kaiser's", receipt.parse_market())

        receipt = Receipt(self.config, "test", "ALDI")
        self.assertEqual("Aldi", receipt.parse_market())

        receipt = Receipt(self.config, "test", "LIDL")
        self.assertEqual("Lidl", receipt.parse_market())

        receipt = Receipt(self.config, "test", "shell")
        self.assertEqual("Tanken", receipt.parse_market())

        receipt = Receipt(self.config, "test", "esso station")
        self.assertEqual("Tanken", receipt.parse_market())

        receipt = Receipt(self.config, "test", "aral")
        self.assertEqual("Tanken", receipt.parse_market())

        receipt = Receipt(self.config, "test", "total tankstelle")
        self.assertEqual("Tanken", receipt.parse_market())

        receipt = Receipt(self.config, "test", "RK Tankstellen")
        self.assertEqual("Tanken", receipt.parse_market())

    def test_parse_sum(self):
        """
            Verifies parse_sum
        """
        test_file = os.path.join(TEST_RECEIPTS_TXT_DIR, "sample_text_receipt.txt")
        receipt = Receipt.from_file(self.config, test_file)
        self.assertIsNotNone(receipt)
        self.assertEqual("0.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "summe   12,99\n")
        self.assertEqual("12.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "summe   *** 12,99 ***\n")
        self.assertEqual("12.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "summe   13.99\n")
        self.assertEqual("13.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "13,99 summe\n")
        self.assertEqual("13.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "gesamtbetrag 1,99\n")
        self.assertEqual("1.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "gesamt 2,99\n")
        self.assertEqual("2.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "total 3,99\n")
        self.assertEqual("3.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "sum 4,99\n")
        self.assertEqual("4.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "zwischensumme 5,99\n")
        self.assertEqual("5.99", receipt.parse_sum())

        receipt = Receipt(self.config, "test", "bar 1,99\n")
        self.assertEqual("1.99", receipt.parse_sum())


if __name__ == "__main__":
    unittest.main()
