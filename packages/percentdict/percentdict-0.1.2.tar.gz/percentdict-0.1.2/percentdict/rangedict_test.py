#!/usr/bin/env python3

import unittest
from rangeddict import RangedDict

class TestRangedDict(unittest.TestCase):
    def setUp(self):
        self.data = [(100, "Everything"), 
                     (20, "Twenty"), 
                     (50, "Fifty"),
                     (75, "Seventy five")]
        self.pd = RangedDict()

    def test_01_setter(self):
        self.pd[20] = "Twenty"
        self.assertEqual(self.pd._mapping, [(20, "Twenty"), (100, None)])
        self.pd[50] = "Fifty"
        self.assertEqual(self.pd._mapping, [(20, "Twenty"), (50, "Fifty"), (100, None)])
        with self.assertRaises(KeyError):
            self.pd[200] = "Booo"
        self.pd[11:20] = "True Twenty"
        self.assertEqual(self.pd._mapping, [(10, "Twenty"), (20, "True Twenty"), (50, "Fifty"), (100, None)])
        self.pd[70: 90] = "Ninety"
        self.assertEqual(self.pd._mapping, [(10, "Twenty"), (20, "True Twenty"), (50, "Fifty"), (69, None), (90, "Ninety"), (100, None)])
        self.pd[15: 70] = "Seventy"
        self.assertEqual(self.pd._mapping, [(10, "Twenty"), (14, "True Twenty"), (70, "Seventy"), (90, "Ninety"), (100, None)])

    def test_02_update(self):
        self.pd.update(self.data)
        self.data.sort()
        self.assertEqual(self.pd._mapping, self.data)
        pd = RangedDict(self.pd)
        self.assertFalse(self.pd is pd)
        self.assertEqual(self.pd, pd)
        with self.assertRaises(ValueError):
            pd.update(2)
        with self.assertRaises(ValueError):
            pd.update([(2,)])
        with self.assertRaises(ValueError):
            pd.update([(2, 3, 4)])

    def test_03_getter(self):
        self.pd.update(self.data)
        for item in self.data:
            self.assertEqual(self.pd.get(item[0]), item[1])
        for item in self.data:
            self.assertEqual(self.pd[item[0]], item[1])
        self.assertEqual(self.pd[30], "Fifty")
        self.assertEqual(self.pd[1:30], ("Twenty", "Fifty"))

    def test_04_contains(self):
        self.pd.update(self.data)
        for item in self.data:
            self.assertTrue(item[1] in self.pd)

    def test_05_eq_and_en(self):
        self.pd.update(self.data)
        pd2 = RangedDict(self.data)
        pd3 = RangedDict()
        pd3[1] = "Caracola"
        self.assertEqual(self.pd, pd2)
        self.assertNotEqual(self.pd, pd3)
        self.assertNotEqual(pd3, pd2)

    def test_06_delitem(self):
        self.pd.update(self.data)
        del(self.pd[15])
        data = self.data.copy()
        del(data[1])
        data.sort()
        self.assertEqual(self.pd._mapping, data)

    def test_07_copy(self):
        self.pd.update(self.data)
        self.data.sort()
        pd1 = self.pd.copy()
        self.assertEqual(pd1._mapping, self.data)
        self.assertEqual(pd1, self.pd)
        self.assertFalse(pd1 is self.pd)

    def test_08_keys(self):
        self.pd.update(self.data)
        self.assertEqual(list(self.pd.keys()), [20, 50, 75, 100])
        self.assertEqual(list(reversed(self.pd.keys())), [100, 75, 50, 20])
        self.assertTrue(all([i in self.pd.keys() for i in [100, 75, 50, 20]]))

    def test_09_values(self):
        self.pd.update(self.data)
        self.assertEqual(list(self.pd.values()), ["Twenty", "Fifty", "Seventy five", "Everything"])
        self.assertEqual(list(reversed(self.pd.values())), ["Everything", "Seventy five", "Fifty", "Twenty"])
        self.assertTrue(all([i in self.pd.values() for i in ["Twenty", "Fifty", "Seventy five", "Everything"]]))

    def test_10_items(self):
        self.pd.update(self.data)
        self.data.sort()
        self.assertEqual(list(self.pd.items()), self.data)
        self.data.reverse()
        self.assertEqual(list(reversed(self.pd.items())), self.data)
        self.assertTrue(all([i in self.pd.items() for i in self.data]))

    def test_11_clear(self):
        self.pd.update(self.data)
        self.pd.clear()
        self.assertEqual(self.pd._mapping, [(100, None)])

    def test_12_example(self):
        data = ["You PC is poor",
                "Your PC can survive",
                "Your PC is middle class",
                "Your PC is rich",
                "Your PC is millionaire"]
        pd = RangedDict()
        pd[0:10] = data[0]
        pd[11:30] = data[1]
        pd[31:70] = data[2]
        pd[71:90] = data[3]
        pd[100] = data[4]
        self.assertEqual(pd[1], data[0])
        self.assertEqual(pd[15], data[1])
        
        pd.clear()
        pd[10] = "You PC is poor"
        pd[30] = "Your PC can survive"
        pd[70] = "Your PC is middle class"
        pd[90] = "Your PC is rich"
        pd[100] = "Your PC is millionaire"
        self.assertEqual(pd[15], data[1])
        self.assertEqual(pd[20], data[1])