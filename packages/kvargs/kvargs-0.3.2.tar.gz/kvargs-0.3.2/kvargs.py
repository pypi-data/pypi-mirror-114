'''
Key=value command line argument parser
======================================

This is an example how good design decisions lead to clear solutions
and how "best practices" bloat the code.

Everyone knows ``dd`` utility? So, this is an implementation of
command line parser for the same syntax.

Compare it with ``argparse``. Impressed?

You may argue that argparse does much more. Okay, I could agree with you
if I did not open the documentation each time when I needed to add
a few simple command line options to my new script.

Well, I don't want to disappoint you completely, so I added a useful hack
which makes the code bigger. Unfortunately, it makes your code shorter.

How to use this module
----------------------

example.py::

    import kvargs

    print(list(kvargs.values()))

    print(kvargs['foo'])
    print(kvargs['bar'])

    if 'far' in kvargs:
        print(kvargs['far'])

How to provide command line args
--------------------------------

Same as for ``dd``::

    python3 example.py foo=123 bar=456 far=0 near=123 near=456 near=789

'''

__version__ = '0.3.2'

#-----------------------------------------------------------------------------------
# Basic logic

kvargs = dict()

def parse_args():
    '''
    Parse ``sys.args`` and populate ``kvargs``.
    '''
    for arg in sys.argv[1:]:  # exclude argv[0]
        if '=' in arg:
            key, value = arg.split('=', 1)
            if key in kvargs:
                # multiple occurences
                if not isinstance(kvargs[key], list):
                    kvargs[key] = [kvargs[key]]
                kvargs[key].append(value)
            else:
                # first occurence
                kvargs[key] = value

#-----------------------------------------------------------------------------------
# Initialization

import sys
parse_args()

# Make kvargs keys accessible as this module's keys or attributes.
# See https://docs.python.org/3/reference/datamodel.html#customizing-module-attribute-access

import types

class _ModuleProxy(types.ModuleType):

    def __getattr__(self, name):
        return kvargs[name]

    def __getitem__(self, k):
        return kvargs[k]

    def __contains__(self, k):
        return k in kvargs

    def __len__(self):
        return len(kvargs)

    def __iter__(self):
        return kvargs.__iter__()

    def __next__(self):
        return kvargs.__next__()

    def get(self, k, default):
        return kvargs.get(k, default)

    def keys(self):
        for key in kvargs.keys():
            yield key

    def values(self):
        for value in kvargs.values():
            yield value

    def items(self):
        for key, value in kvargs.items():
            yield key, value

sys.modules[__name__].__class__ = _ModuleProxy

# Copyright 2019,2021 AXY axy@declassed.art
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
