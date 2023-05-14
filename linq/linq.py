import numpy as np
from collections import defaultdict
from functools import reduce
from itertools import chain


class LINQIterator:
    def __init__(self, iterator):
        self._iterator = iterator

    def select(self, operation):
        return LINQIterator(map(operation, self._iterator))

    def where(self, predicate):
        return LINQIterator(filter(predicate, self._iterator))

    def take(self, k):
        return LINQIterator(zip(self._iterator, range(k))).select(lambda x: x[0])

    def orderBy(self, key_function, reverse=False):
        return LINQIterator(sorted(self._iterator, key=key_function, reverse=reverse))
    
    def flatten(self):
        return LINQIterator(reduce(lambda prev, cur: chain(prev, cur), self._iterator))
    
    def groupBy(self, key_function):
        values = defaultdict(list)
        for row in self._iterator:
            values[key_function(row)].append(row)

        return LINQIterator(iter(values.items()))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)

    def toList(self):
        return list(self._iterator)