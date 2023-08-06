#!/usr/bin/env python3

import unittest
from percentdict import PercentDict

class TestPercentDict(unittest.TestCase):
    def setUp(self):
        self.data = [(1, "Everything"), 
                     (0.2, "Twenty"), 
                     (0.5, "Fifty"),
                     (0.75, "Seventy five")]
        self.pd = PercentDict()

    def test_01_setter(self):
        self.pd[0.2] = "Twenty"
        self.assertEqual(self.pd._mapping, [(0.2, "Twenty"), (1, None)])
        self.pd[0.5] = "Fifty"
        self.assertEqual(self.pd._mapping, [(0.2, "Twenty"), (0.5, "Fifty"), (1, None)])
        with self.assertRaises(KeyError):
            self.pd[2] = "Booo"
        self.pd[0.1:0.2] = "True Twenty"
        self.assertEqual(self.pd._mapping, [(0.1, "Twenty"), (0.2, "True Twenty"), (0.5, "Fifty"), (1, None)])
        self.pd[0.7: 0.9] = "Ninety"
        self.assertEqual(self.pd._mapping, [(0.1, "Twenty"), (0.2, "True Twenty"), (0.5, "Fifty"), (0.7, None), (0.9, "Ninety"), (1, None)])
        self.pd[0.15: 0.7] = "Seventy"
        self.assertEqual(self.pd._mapping, [(0.1, "Twenty"), (0.15, "True Twenty"), (0.7, "Seventy"), (0.9, "Ninety"), (1, None)])

    def test_02_update(self):
        self.pd.update(self.data)
        self.data.sort()
        self.assertEqual(self.pd._mapping, self.data)
        pd = PercentDict(self.pd)
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
        self.assertEqual(self.pd[0.3], "Fifty")
        self.assertEqual(self.pd[0.1:0.3], ("Twenty", "Fifty"))

    def test_04_contains(self):
        self.pd.update(self.data)
        for item in self.data:
            self.assertTrue(item[1] in self.pd)

    def test_05_eq_and_en(self):
        self.pd.update(self.data)
        pd2 = PercentDict(self.data)
        pd3 = PercentDict()
        pd3[1] = "Caracola"
        self.assertEqual(self.pd, pd2)
        self.assertNotEqual(self.pd, pd3)
        self.assertNotEqual(pd3, pd2)

    def test_06_delitem(self):
        self.pd.update(self.data)
        del(self.pd[0.15])
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
        self.assertEqual(list(self.pd.keys()), [0.2, 0.5, 0.75, 1])
        self.assertEqual(list(reversed(self.pd.keys())), [1, 0.75, 0.5, 0.2])
        self.assertTrue(all([i in self.pd.keys() for i in [1, 0.75, 0.5, 0.2]]))

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
        self.assertEqual(self.pd._mapping, [(1, None)])

    def test_12_example(self):
        data = ["You PC is poor",
                "Your PC can survive",
                "Your PC is middle class",
                "Your PC is rich",
                "Your PC is millionaire"]
        pd = PercentDict()
        pd[0:0.1] = data[0]
        pd[0.1:0.3] = data[1]
        pd[0.3:0.7] = data[2]
        pd[0.8:0.9] = data[3]
        pd[1] = data[4]
        self.assertEqual(pd[0.1], data[0])
        self.assertEqual(pd[0.15], data[1])
        
        pd.clear()
        pd[0.1] = "You PC is poor"
        pd[0.3] = "Your PC can survive"
        pd[0.7] = "Your PC is middle class"
        pd[0.9] = "Your PC is rich"
        pd[1] = "Your PC is millionaire"
        self.assertEqual(pd[0.15], data[1])
        self.assertEqual(pd[0.2], data[1])