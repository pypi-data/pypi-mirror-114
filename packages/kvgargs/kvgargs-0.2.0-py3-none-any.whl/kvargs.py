'''
= Key-value command line argument parser =

How to provide command line args:

    python3 example.py xxx foo=123 bar=456 yyy far=0 near=123 near=456 near=789 zzz

How to use this module:

    import kvargs

    print(list(kvargs.all.values()))

    print(kvargs.all['foo'])
    print(kvargs.all['bar'])

    if 'far' in kvargs.all:
        print(kvargs.all['far'])

XXX explain group

See also ``sayyes`` package if you need arguments declaration and validation.

'''

__version__ = '0.2.0'

#-----------------------------------------------------------------------------------
# Basic logic

from collections import defaultdict, OrderedDict

''' All key=value arguments '''
all = OrderedDict()

''' Grouped key=value arguments by preceeding nonparseable arguments, i.e.:

foo=bar abc far=baz -> {None: {'foo': 'bar'}, 'abc': {'far': 'baz'}}

abc def foo=bar hij far=baz -> {('abc', 'def'): {'foo': 'bar'}, 'hij': {'far': 'baz'}}
'''
group = OrderedDict()

def parse_args():
    '''
    Parse ``sys.args`` and populate ``all`` and ``group``.
    '''
    last_group = None
    prev_parseable = False
    for arg in sys.argv[1:]:  # exclude argv[0]
        if '=' in arg:
            # parseable key=value argument
            key, value = arg.split('=', 1)
            # add to all
            _add_to_dict(key, value, all)
            # add to group
            group_kvargs = group.setdefault(last_group, {})
            _add_to_dict(key, value, group_kvargs)
            prev_parseable = True
        else:
            # non-parseable argument
            if prev_parseable:
                # reset last_group after last parseable argument
                last_group = None
            if last_group is None:
                last_group = arg
            else:
                if not isinstance(last_group, tuple):
                    last_group = (last_group,)
                last_group = last_group + (arg,)
            prev_parseable = False

    if not prev_parseable and last_group is not None and last_group not in group:
        # save last non-parseable arguments as an empty group
        group[last_group] = {}

def _add_to_dict(key, value, dest_dict):
    # add kvarg to dest_dict
    if key in dest_dict:
        # multiple occurences
        if not isinstance(dest_dict[key], list):
            dest_dict[key] = [dest_dict[key]]
        dest_dict[key].append(value)
    else:
        # first occurence
        dest_dict[key] = value

#-----------------------------------------------------------------------------------
# Initialization

import sys
parse_args()

#-----------------------------------------------------------------------------------
# Copyright 2019,2021 CME cme@simpledevice.org
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
