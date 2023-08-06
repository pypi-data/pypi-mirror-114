#!/usr/bin/env python3

"""
For a more intuitive implementation in case you want to use like the example a dice like, you can use RangedDict. It will only accept integers in getters, setters and slices.

I.E:

rd = RangedDict(d=12) # d means the faces of the dice

rd[1] = "You PC is poor"
rd[2:4] = "Your PC can survive"
rd[5:9] = "Your PC is middle class"
rd[10:11] = "Your PC is rich"
rd[12] = "Your PC is millionaire"

rd[6]
"Your PC is middle class"

You can use the method random() to get a randomized value.

rd.random()
"""

__package__ = "percentdict"

from percentdict import PercentDict
import random

class NotAValue(): pass #None is not an option

class RangedDict(PercentDict):
    def __init__(self, mapping=None, *, d=100): # TODO Clean mapping
        self._d = d
        super().__init__(mapping)

    def __setitem__(self, key, value):
        if isinstance(key, int) and 0 <= key <= self._d: #Let's accept 0
            for index, item in enumerate(self._mapping):
                if key == item[0]:
                    self._mapping[index] = (key, value)
                    break                
            else:
                self._mapping.append((key, value))
                self._mapping.sort()

        elif (isinstance(key, slice) and 
              0 <= key.start <= self._d and
              0 <= key.stop <= self._d and
              key.start <= key.stop):
            todel = []
            start_value = NotAValue
            last_index = 0
            for index, item in enumerate(self._mapping):
                if key.start <= item[0] <= key.stop:
                    todel.append(index)
                    if start_value is NotAValue:
                        start_value = item[1]
                elif last_index+1 < key.start <= key.stop < item[0]:
                    start_value = item[1]
                    break
                last_index = item[0]
            todel.sort()
            todel.reverse()
            for index in todel:
                del(self._mapping[index])
            if start_value is not NotAValue and key.start > 0:
                self._mapping.append((key.start-1, start_value))
            self._mapping.append((key.stop, value))
            self._mapping.sort()

        else:
            raise KeyError(f"key must be int or a slice of ints between 0 and {self._d}")

    def clear(self):
        self._mapping = [(self._d, None)]

    def get(self, key):
        if isinstance(key, int) and 0 <= key <= self._d: #Let's accept 0
            for item in self._mapping:
                if key <= item[0]:
                    return item[1]
            else:
                raise KeyError("Key not found. If this error is raised I'm a moron")

        elif (isinstance(key, slice) and 
              0 <= key.start <= self._d and
              0 <= key.stop <= self._d and
              key.start <= key.stop):
            final = []
            for item in self._mapping:
                if not final and key.start <= item[0]:
                    final.append(item[1])
                elif final:
                    final.append(item[1])
                    if key.stop <= item[0]:
                        break
            if final:
                return tuple(final)
            else:
                raise KeyError("Key not found. If this error is raised I'm a moron")
        
        else:
            raise KeyError(f"key must be int or a slice of ints between 0 and {self._d}")

    def random(self):
        return self.get(random.randint(self._d))