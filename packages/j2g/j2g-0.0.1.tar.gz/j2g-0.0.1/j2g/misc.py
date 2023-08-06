"""
Created on 2020-12-25

@author: jeack_chen@hotmail.com
"""
import re


# def getattr_deepcopy_decorator(func):
#     def wrapper(self, key):
#         if key.startswith("__"):  # for copy.deepcopy
#             raise AttributeError("%r has no attribute %r" % (type(self), key))
#         return func(self, key)
#
#     return wrapper
#
#
# class FakeStore:
#     @getattr_deepcopy_decorator
#     def __getattr__(self, key):
#         return self.worker
#
#     def worker(self, *args, **kwargs):
#         pass
#
#
class PrefixHelper:
    def __init__(self, prefix):
        self.prefix = prefix
        self.prefix_len = len(prefix)

    def remove(self, key):
        return "" if not key.startswith(self.prefix) else key[self.prefix_len:]

    def add(self, key):
        return f'{self.prefix}{key}'


class IndexHelper:
    def __init__(self, left=0, prefix='f'):
        self.left = left
        self.prefix = PrefixHelper(prefix)

    def __call__(self, *args):
        self.left += 1
        return self.prefix.add(self.left)


class TableHelper:
    def __init__(self, node, left='', right=''):
        self.node = node
        self.buf = []
        self.buf.append('<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR>')
        self.buf.append(f'<TD SIDES="R">{left}</TD>')
        self._right = right
        self._index = IndexHelper()

    def append(self, value='+', port=None, sides=None):
        if port is None:
            port = self._index()
        sides = '' if sides is None else f'SIDES="{sides}" '
        self.buf.append(f'<TD {sides}PORT="{port}">{value}</TD>')
        return f'{self.node}:{port}'

    def append_last(self, value, num):
        if num > 0:
            last = re.sub(r' ?PORT=".+"', '', self.buf[-1])
            new_last = re.sub(r'>.+<', f'>{value}<', last)
            # print(f'{self.buf[-1]} => {new_last}')
            for _ in range(num):
                self.buf.append(new_last)

    def done(self, g, parent):
        if self._right is not None:
            self.buf.append(f'<TD SIDES="L">{self._right}</TD>')
            self.buf.append('</TR></TABLE>>')
            self._right = None
        g.node(self.node, '\n'.join(self.buf))
        g.edge(parent, self.node)
        return '\n'.join(self.buf)

