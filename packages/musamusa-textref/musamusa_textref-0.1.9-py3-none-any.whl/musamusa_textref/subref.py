#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-TextRef Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-TextRef.
#    MusaMusa-TextRef is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-TextRef is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-TextRef.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-TextRef project : musamusa_textref/subref.py

   The SubRef class is an internal class used by TextRef* classes.


   (pimydoc)about textual references
   ⋅ References to a text are a way to locate an excerpt in a longer text.
   ⋅
   ⋅ For the user, a textual reference (=textref) is a string describing one
   ⋅ or more references:
   ⋅
   ⋅         By example. "title.43a-title.44b" means
   ⋅                     title.43a+title.43b+title.44a+title.44b
   ⋅
   ⋅ Under the hood, three levels of references are distinguished:
   ⋅
   ⋅     - mono-textref like "title.43a"
   ⋅         > "title.43a" means nothing but "title.43a"
   ⋅     - bi-textref like "title.43a" or "title.43a-title.44b"
   ⋅         > "title.43a-title.44b" means
   ⋅           title.43a+title.43b+title.44a+title.44b
   ⋅     - multi-textref like "title.43a-", "title.43a-title.44b"
   ⋅       or "title.43a-title.44b;title.43c"
   ⋅         > "title.43a-title.44b;title.43c" means
   ⋅           title.43a+title.43b+title.44a+title.44b+title.43c

   (pimydoc)monoref/biref/multiref(internal)
   ⋅ Internal representation of mono-/bi-/multi- textref:
   ⋅
   ⋅     o  mono textref: "title.3" is internally stored as:
   ⋅
   ⋅                     ((None, 'title'), ('int', 3))
   ⋅                       ^     ^             ^     ^
   ⋅                       ^     ^             ^     value (here, a int)
   ⋅                       ^     ^             ^
   ⋅                       ^     ^             [0] : value type
   ⋅                       ^     ^
   ⋅                       ^     [1]value : since [0] is None, it's a string.
   ⋅                       ^
   ⋅                       [0] is None if the value (here 'title') is not countable
   ⋅
   ⋅     o  bi textref: "title.3-title.4" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      ((None, 'title'), ('int', 3)),
   ⋅                      ((None, 'title'), ('int', 4))
   ⋅                     )
   ⋅
   ⋅                     "title.3-" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      ((None, 'title'), ('int', 3)),
   ⋅                     )
   ⋅
   ⋅     o  multi textrefs: "title.3-title.4;title.7" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      (((None, 'title'), ('int', 3)),
   ⋅                       ((None, 'title'), ('int', 4))
   ⋅                      ),
   ⋅                      (((None, 'title'), ('int', 7)),
   ⋅                      ),
   ⋅                     )
   ⋅
   ⋅ To get lists-/tuples- only definitions, use
   ⋅     TextRefBaseClass._definition_as_lists() and
   ⋅     TextRefBaseClass._definition_as_tuples()
   ⋅     methods

   ____________________________________________________________________________

   class:

   o  SubRef class
"""
from iaswn.iaswn import Iaswn

# SubRef is a class with attributes and a .__init__() which fill automatically
# the .int2char attribute.
# pylint: disable=too-few-public-methods


class SubRef(Iaswn):
    """
        SubRef class

        Type used by TextRefBaseClass._subrefs

        (pimydoc)TextRefBaseClass._subrefs structure
        ⋅
        ⋅ Beware ! If you modify _subrefs content, please rewrite
        ⋅     o  _init_from_str__extract_def_from_src_mono()
        ⋅     o  _monoref_definition2str()
        ⋅ in the derived class.
        ⋅
        ⋅ TextRefBaseClass._subref is a tuple made of:
        ⋅
        ⋅     *  .regex     : (bytes)a compiled regex
        ⋅     *  .min_value : None or (integer) minimal value
        ⋅     *  .max_value : None or (integer) maximal value
        ⋅     *  .char2int  : None or (a dict)  character to integer value
        ⋅     *  .int2char  : inverse of .char2int, automatically generated
        ⋅
        ⋅     By example:
        ⋅     * re.compile(r"^[a-z]$"),
        ⋅     * 1,
        ⋅     * 26,
        ⋅     * {"a": 1,
        ⋅        "b": 2,
        ⋅        ...
        ⋅        "z": 26}
    """
    def __init__(self,
                 regex,
                 min_value,
                 max_value,
                 char2int):
        self.regex = regex
        self.min_value = min_value
        self.max_value = max_value
        self.char2int = char2int

        self.int2char = dict((value, key) for key, value in self.char2int.items())
