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
   MusaMusa-TextRef project : musamusa_textref/textrefbaseclass.py

   The TextRefBaseClass helps to compare textual references.

   Don't directly use this class : use instead derived classes like TextRefDefault.

   Beware ! TextRef* classes don't store the source string you may used to initialize
            such an object. You have to store this source string apart.


   Unit testing: see tests/textrefbaseclass.py



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

   o  TextRefBaseClass class
"""
# The TextRefBaseClass uses a lot of methods and class attributes
# whose name starts with "_", meaning it's an internal object, not
# to be used by an user.
# pylint: disable=protected-access

import re

from iaswn.iaswn import Iaswn
from musamusa_romannumbers.romannumbers import from_roman, to_roman
from musamusa_errors.error_messages import ListOfErrorMessages, MusaMusaError
from musamusa_textref.subref import SubRef


class TextRefBaseClass(Iaswn):
    """
        TextRefBaseClass class

        Mother class for all TextRef* classes.

        This class has well defined __hash__(), __eq__() and __ne__() methods but
        __ge__(), __gt__(), __lt__() and __le__() will raise the NotImplementedError
        exception.
        _______________________________________________________________________

        CLASS ATTRIBUTES:
        o  (dict, see infra)     _cmp_monoref_vs_biref__data
        o  (dict, see infra)     _subrefs
        o  (str)                 _refs_separator = ";"
        o  (str)                 _ref2ref_separator = "-"
        o  (str)                 _refsubpart_separator = "."

        ATTRIBUTES:
        o  (func)                _cmp_strs
        o  (tuple)               definition
        o  (ListOfErrorMessages) errors
        o  (bool)                is_valid

        METHODS:
        o  __eq__(self, textref2)
        o  __ge__(self, textref2)
        o  __gt__(self, textref2)
        o  __hash__(self)
        o  __init__(self,
                    definition=None,
                    _cmp_strs=None,
                    keep_iter_infos=True,
                    force_validity=True)
        o  __iter__(self)
        o  __le__(self, textref2)
        o  __lt__(self, textref2)
        o  __ne__(self, textref2)
        o  __str__(self)
        o  _cmp_biref_vs_biref(self, biref1, biref2)
        o  _cmp_monoref_vs_biref(self, monoref1, biref2)
        o  _cmp_monoref_vs_monoref(self, monoref1, monoref2)
        o  _cmp_monoref_vs_monoref_almost_eq(monoref1, monoref2)
        o  _cmp_monoref_vs_monoref_eq(monoref1, monoref2)
        o  _cmp_multiref_vs_multiref(self, multiref1, multiref2)
        o  _default_cmp_strs(str1, str2)
        o  _get_reduced_definition(self, keep_iter_infos=True)
        o  _init_from_str__add_mono_or_biref(self, source_string: str)
        o  _init_from_str__extract_def_from_src_mono(self, src)
        o  _monoref_definition2str(self, monoref)
        o  _monoref_as_lists(monoref)
        o  _monoref_as_tuples(monoref)
        o  _monoref_extend_with_the_same_structure_as(monoref1, monoref2)
        o  _monoref_getpredecessor(self, monoref)
        o  _monoref_getsuccessor(self, monoref)
        o  _monoref_has_its_rightest_item_to_its_highest_value(monoref)
        o  _monoref_has_its_rightest_item_to_its_lowest_value(monoref)
        o  _monoref_set_rightest_item_to_its_highest_value(self, monoref)
        o  _monoref_set_rightest_item_to_its_lowest_value(self, monoref)
        o  _multiref_as_lists(definition)
        o  _multiref_as_tuples(definition)
        o  add_and_sort(self, textref2, keep_iter_infos=True)
        o  add_and_sort_from_str(self,
                                 source_string,
                                 strings_must_be_sorted=True,
                                 keep_iter_infos=True)
        o  customized_valid_definition(self, explicit=False)
        o  definition2str(self, reduced=False, keep_iter_infos=True)
        o  init_from_str(self,
                         source_string: str,
                         strings_must_be_sorted=False,
                         keep_iter_infos=True)
        o  is_empty(self)
        o  valid_definition(self, strings_must_be_sorted=False, explicit=False)
    """
    # (pimydoc)TextRefBaseClass._subrefs structure
    # ⋅
    # ⋅ Beware ! If you modify _subrefs content, please rewrite
    # ⋅     o  _init_from_str__extract_def_from_src_mono()
    # ⋅     o  _monoref_definition2str()
    # ⋅ in the derived class.
    # ⋅
    # ⋅ TextRefBaseClass._subref is a tuple made of:
    # ⋅
    # ⋅     *  .regex     : (bytes)a compiled regex
    # ⋅     *  .min_value : None or (integer) minimal value
    # ⋅     *  .max_value : None or (integer) maximal value
    # ⋅     *  .char2int  : None or (a dict)  character to integer value
    # ⋅     *  .int2char  : inverse of .char2int, automatically generated
    # ⋅
    # ⋅     By example:
    # ⋅     * re.compile(r"^[a-z]$"),
    # ⋅     * 1,
    # ⋅     * 26,
    # ⋅     * {"a": 1,
    # ⋅        "b": 2,
    # ⋅        ...
    # ⋅        "z": 26}
    _subrefs = {
              "a-z(1)": SubRef(re.compile(r"^[a-z]$"),
                               1,
                               26,
                               {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5,
                                "f": 6, "g": 7, "h": 8, "i": 9, "j": 10,
                                "k": 11, "l": 12, "m": 13, "n": 14, "o": 15,
                                "p": 16, "q": 17, "r": 18, "s": 19, "t": 20,
                                "u": 21, "v": 22, "w": 23, "x": 24, "y": 25,
                                "z": 26}),
              "A-Z(1)": SubRef(re.compile(r"^[A-Z]$"),
                               1, 26,
                               {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
                                "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
                                "K": 11, "L": 12, "M": 13, "N": 14, "O": 15,
                                "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20,
                                "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25,
                                "Z": 26}),
              "α-ω(1)": SubRef(re.compile(r"^[αβγδεζηθικλμνξοπρστυϕχψω]$"),
                               1, 24,
                               {"α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5,
                                "ζ": 6, "η": 7, "θ": 8, "ι": 9, "κ": 10,
                                "λ": 11, "μ": 12, "ν": 13, "ξ": 14, "ο": 15,
                                "π": 16, "ρ": 17, "σ": 18, "τ": 19, "υ": 20,
                                "ϕ": 21, "χ": 22, "ψ": 23, "ω": 24}),
              "Α-Ω(1)": SubRef(re.compile(r"^[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]$"),
                               1, 24,
                               {"Α": 1, "Β": 2, "Γ": 3, "Δ": 4, "Ε": 5,
                                "Ζ": 6, "Η": 7, "Θ": 8, "Ι": 9, "Κ": 10,
                                "Λ": 11, "Μ": 12, "Ν": 13, "Ξ": 14, "Ο": 15,
                                "Π": 16, "Ρ": 17, "Σ": 18, "Τ": 19, "Υ": 20,
                                "Φ": 21, "Χ": 22, "Ψ": 23, "Ω": 24}),
              "int": SubRef(re.compile(r"^\d+$"),
                            1, 9999, {}),
              "roman numbers": SubRef(re.compile(r"^[IVXLCDM]+$"),
                                      1, 3999, {}),
              "int+a-z(1)": SubRef(re.compile(r"^(?P<subref0>\d+)(?P<subref1>[a-z])$"),
                                   None, None, {}),
              "int+A-Z(1)": SubRef(re.compile(r"^(?P<subref0>\d+)(?P<subref1>[A-Z])$"),
                                   None, None, {}),
              }
    _refs_separator = ";"
    _ref2ref_separator = "-"
    _refsubpart_separator = "."

    # (pimydoc)_cmp_monoref_vs_biref:data
    # ⋅
    # ⋅ _cmp_monoref_vs_biref__data
    # ⋅
    # ⋅ The dict _cmp_monoref_vs_biref__data[operation1, operation2, result] allows to
    # ⋅ the _cmp_monoref_vs_biref() method to return immediatly a result.
    # ⋅
    # ⋅   if M is a textref object and (M1 - M2) a pair of textrefs objects,
    # ⋅   if operation1 is _cmp_monoref_vs_monoref(M1, M)
    # ⋅   if operation1 is _cmp_monoref_vs_monoref(M, M2)
    # ⋅     ... then _cmp_monoref_vs_biref__data[r1, r2] gives _cmp_monoref_vs_biref[M, (M1, M2)] .
    # ⋅
    # ⋅
    # ⋅                                M                        M1       M2
    # ⋅ o M1 < M < M2   How is "title.34" compared to (title.33, title36) ? [inside]
    # ⋅ o M1 < M = M2   How is "title.34" compared to (title.33, title34) ? [inside]
    # ⋅ o M1 < M ⊂ M2  How is "title.34a" compared to (title.33, title34) ? [inside]
    # ⋅ o M1 < M ⊃ M2  How is "title.34"  compared to (title.32, title34a) ? [outside_overlap]
    # ⋅ o M1 < M > M2   How is "title.34a" compared to (title.30, title32) ? [outside_after]
    # ⋅
    # ⋅ o M1 = M < M2   How is "title.34" compared to (title.34, title36) ? [inside]
    # ⋅ o M1 = M = M2   How is "title.34" compared to (title.34, title34) ? [equal]
    # ⋅ o M1 = M ⊂ M2   How is "title.34a" compared to (title.34a, title34) ? [undefined]
    # ⋅ o M1 = M ⊃ M2   How is "title.34" compared to (title.34, title34a) ? [outside_overlap]
    # ⋅ o M1 = M > M2   How is "title.34" compared to (title.34, title33) ?    [undefined]
    # ⋅
    # ⋅ o M1 ⊃ M < M2   How is "title.33a" compared to (title.33, title36) ? [inside]
    # ⋅ o M1 ⊃ M = M2   How is "title.33a" compared to (title.33, title33a) ? [inside]
    # ⋅ o M1 ⊃ M ⊂ M2  How is "title.33a" compared to (title.33, title34) ? [inside]
    # ⋅ o M1 ⊃ M ⊃ M2  How is "title.33a" compared to (title.33, title33a1) ?[outside_overlap]
    # ⋅ o M1 ⊃ M > M2   How is "title.33a" compared to (title.33, title32b) ?  [undefined]
    # ⋅
    # ⋅ o M1 ⊂ M < M2   How is "title.33" compared to (title.33b, title36) ? [outside_before]
    # ⋅ o M1 ⊂ M = M2   How is "title.33" compared to (title.33b, title33) ? [undefined]
    # ⋅ o M1 ⊂ M ⊂ M2   How is "title.33b" compared to (title.33b.1, title33) ? [undefined]
    # ⋅ o M1 ⊂ M ⊃ M2   How is "title.33" compared to (title.33a, title33b) ? [outside_before]
    # ⋅ o M1 ⊂ M > M2   How is "title.33" compared to (title.33a, title32) ? [undefined]
    # ⋅
    # ⋅ o M1 > M < M2   How is "title.30" compared to (title.32, title36) ?   [outside_before]
    # ⋅ o M1 > M = M2   How is "title.30" compared to (title.33, title30) ?   [undefined]
    # ⋅ o M1 > M ⊂ M2   How is "title.30a" compared to (title.33, title30) ? [undefined]
    # ⋅ o M1 > M ⊃ M2   How is "title.30"  compared to (title.33, title30a) ? [undefined]
    # ⋅ o M1 > M > M2   How is "title.30" compared to (title.33, title.40) ?  [outside_before]
    # ⋅
    # ⋅
    # ⋅ Same data with '!' replaced by #0, '=' by #1, and so on.
    # ⋅     (about these values, see pimydoc::_cmp_monoref_vs_monoref:returned value)
    # ⋅
    # ⋅ o M1 3 M 3 M2   How is "title.34" compared to (title.33, title36) ? [#2]
    # ⋅ o M1 3 M 1 M2   How is "title.34" compared to (title.33, title34) ? [#2]
    # ⋅ o M1 3 M 4 M2   How is "title.34a" compared to (title.33, title34) ? [#2]
    # ⋅ o M1 3 M 5 M2   How is "title.34"  compared to (title.32, title34a) ? [#5]
    # ⋅ o M1 3 M 2 M2   How is "title.34a" compared to (title.30, title32) ? [#4]
    # ⋅
    # ⋅ o M1 1 M 3 M2   How is "title.34" compared to (title.34, title36) ? [#2]
    # ⋅ o M1 1 M 1 M2   How is "title.34" compared to (title.34, title34) ? [equal]
    # ⋅ o M1 1 M 4 M2   How is "title.34a" compared to (title.34a, title34) ? [#0]
    # ⋅ o M1 1 M 5 M2   How is "title.34" compared to (title.34, title34a) ? [#5]
    # ⋅ o M1 1 M 2 M2   How is "title.34" compared to (title.34, title33) ?    [#0]
    # ⋅
    # ⋅ o M1 5 M 3 M2   How is "title.33a" compared to (title.33, title36) ? [#2]
    # ⋅ o M1 5 M 1 M2   How is "title.33a" compared to (title.33, title33a) ? [#2]
    # ⋅ o M1 5 M 4 M2   How is "title.33a" compared to (title.33, title34) ? [#2]
    # ⋅ o M1 5 M 5 M2   How is "title.33a" compared to (title.33, title33a1) ? [#5]
    # ⋅ o M1 5 M 2 M2   How is "title.33a" compared to (title.33, title32b) ?  [#0]
    # ⋅
    # ⋅ o M1 4 M 3 M2   How is "title.33" compared to (title.33b, title36) ? [#3]
    # ⋅ o M1 4 M 1 M2   How is "title.33" compared to (title.33b, title33) ? [#0]
    # ⋅ o M1 4 M 4 M2   How is "title.33b" compared to (title.33b.1, title33) ? [#0]
    # ⋅ o M1 4 M 5 M2   How is "title.33" compared to (title.33a, title33b) ? [#3]
    # ⋅ o M1 4 M 2 M2   How is "title.33" compared to (title.33a, title32) ? [#0]
    # ⋅
    # ⋅ o M1 2 M 3 M2   How is "title.30" compared to (title.32, title36) ?   [#3]
    # ⋅ o M1 2 M 1 M2   How is "title.30" compared to (title.33, title30) ?   [#0]
    # ⋅ o M1 2 M 4 M2   How is "title.30a" compared to (title.33, title30) ? [#0]
    # ⋅ o M1 2 M 5 M2   How is "title.30"  compared to (title.33, title30a) ? [#0]
    # ⋅ o M1 2 M 2 M2   How is "title.32" compared to (title.33, title.31) ?  [#0]
    _cmp_monoref_vs_biref__data = {
        (3, 3): 2,
        (3, 1): 2,
        (3, 4): 2,
        (3, 5): 5,
        (3, 2): 4,

        (1, 3): 2,
        (1, 1): 1,
        (1, 4): 0,
        (1, 5): 5,
        (1, 2): 0,

        (5, 3): 2,
        (5, 1): 2,
        (5, 4): 2,
        (5, 5): 5,
        (5, 2): 0,

        (4, 3): 3,
        (4, 1): 0,
        (4, 4): 0,
        (4, 5): 3,
        (4, 2): 0,

        (2, 3): 3,
        (2, 1): 0,
        (2, 4): 0,
        (2, 5): 0,
        (2, 2): 0,
        }

    def __eq__(self,
               textref2):
        """
            TextRefBaseClass.__eq__()

            Is self.definition == textref2.definition ?

                Please notice that THE RESULTS MAY DIFFER WITH THOSE RETURNED BY
            self.is_equal().
                __eq__() is the fastest way to compare two definitions but this
            method will fail if tuples and lists are mixed - which should never
            be the case except in intermediate results.
                On the contrary .is_equal() is indifferent to such a mix.
            ___________________________________________________________________

            ARGUMENT:
            o  textref2: a TextRef* class

            RETURNED VALUE: (bool)
                see https://docs.python.org/3/reference/datamodel.html#object.__eq__
        """
        return self.definition == textref2.definition

    def __ge__(self,
               textref2):
        """
            TextRefBaseClass.__ge__()

            Is self >= textref2 ?

            Since TextRef* classes can't be ordered, raise an NotImplementedError exception.
            ___________________________________________________________________

            ARGUMENT:
            o  (TextRef* class) textref2

            RETURNED VALUE: (bool)
                see https://docs.python.org/3/reference/datamodel.html#object.__ge__
        """
        raise NotImplementedError

    def __gt__(self,
               textref2):
        """
            TextRefBaseClass.__gt__()

            Is self > textref2 ?

            Since TextRef* classes can't be ordered, raise an NotImplementedError exception.
            ___________________________________________________________________

            ARGUMENT:
            o  (TextRef* class) textref2

            RETURNED VALUE: (bool)
                see https://docs.python.org/3/reference/datamodel.html#object.__gt__
        """
        raise NotImplementedError

    def __hash__(self):
        """
            TextRefBaseClass.__hash__()

            TextRef* can be used directly as keys in dict, hence this method.
            ___________________________________________________________________

            RETURNED VALUE: (int)
                see https://docs.python.org/3/reference/datamodel.html#object.__hash__
        """
        return hash(self.definition)

    def __init__(self,
                 definition=None,
                 _cmp_strs=None,
                 keep_iter_infos=True,
                 force_validity=True):
        """
            TextRefBaseClass.__init__()
            ___________________________________________________________________

            ARGUMENTS:
            o  definition:
               (pimydoc)TextRefBaseClass.definition content
               ⋅ At the end of the initialisation, .definition must be made of tuples without
               ⋅ any list.
               ⋅
               ⋅ o  source string:  "title.3-title.4"
               ⋅    .definition:    (
               ⋅                     ((None, 'title'), ('int', 3)),
               ⋅                     ((None, 'title'), ('int', 4))
               ⋅                    )
               ⋅
               ⋅ o  source string:  "title.3-title.4;title.15-title.16"
               ⋅    .definition:    (
               ⋅                     (
               ⋅                      ((None, 'title'), ('int', 3)),
               ⋅                      ((None, 'title'), ('int', 4))
               ⋅                     ),
               ⋅                     (
               ⋅                      (((None, 'title'), ('int', 15)),
               ⋅                      ((None, 'title'), ('int', 16))),
               ⋅                     )
               ⋅                    )
               ⋅
               ⋅ Special syntax for monoref stored as a biref:
               ⋅
               ⋅ o  source string:  "title.3-"
               ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
               ⋅                                                      ^
               ⋅                                         special syntax here: we do not repeat
               ⋅                                             ((None, 'title'), ('int', 3))
            o  _cmp_strs: (None or func)function to be used to compare two strings.
                          By default (_cmp_strs=None) the default function is used,
                          namely TextRefBaseClass._default_cmp_strs()

                          (pimydoc)_cmp_strs:returned value
                          ⋅ 0 si str1==str2, -1 if str1<str2, +1 if str>str2
            o  keep_iter_infos: (bool) parameter used in __init__() (if paramater <definition> is
                                given) by ._get_reduced_definition()
            o  force_validity: (bool) if True, <self> will be marked as valid whatever the value
                               of .definition; e.g. .definition may be empty, .is_valid will be
                               True.
        """
        self.errors = ListOfErrorMessages()

        # (pimydoc)valid definition
        # ⋅ * empty .definition is forbidden (no "") (VALIDDEFINITION001)
        # ⋅ * for each biref[0], biref[1] in .definition:
        # ⋅     * biref[0] can't be empty (no "-mybook.3") (VALIDDEFINITION002a,
        # ⋅                                                 VALIDDEFINITION002b)
        # ⋅     * biref[0] and biref[1] can't be equal (no "mybook.3-mybook.3")
        # ⋅       (VALIDDEFINITION003)
        # ⋅     * biref[0] and biref[1] must have the same structure (VALIDDEFINITION004)
        # ⋅         - "a_string.3.another_string.4-a_string.5.another_string.6" is OK
        # ⋅         - "a_string.3.another_string.4-5.another_string.6" is not OK
        # ⋅     * biref[0] and biref[1] must have the same strings (VALIDDEFINITION005)
        # ⋅         - "title.1-title.2 is OK
        # ⋅         - "another_title.1-title.2 is not OK
        # ⋅     * as long as items are equal the values must be equal or increasing
        # ⋅       (VALIDDEFINITION006)
        # ⋅         - "title.3-title.4" is OK
        # ⋅         - "title.33.h-title.36.b" is OK
        # ⋅         - "title.4-title.3" is not OK
        # ⋅         - "title.33.h-title.33.b" is not OK
        # ⋅ * if strings_must_be_sorted is True,
        # ⋅   for each string in the different biref: the strings must be sorted
        # ⋅   (VALIDDEFINITION007)
        # ⋅   - "another_title;title.3-title.4" is OK
        # ⋅   - "title.3-title.4;another_title" is not OK
        if not force_validity:
            self.is_valid = False
        else:
            self.is_valid = True

        if _cmp_strs:
            self._cmp_strs = _cmp_strs
        else:
            self._cmp_strs = self._default_cmp_strs

        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be made of tuples without
        # ⋅ any list.
        # ⋅
        # ⋅ o  source string:  "title.3-title.4"
        # ⋅    .definition:    (
        # ⋅                     ((None, 'title'), ('int', 3)),
        # ⋅                     ((None, 'title'), ('int', 4))
        # ⋅                    )
        # ⋅
        # ⋅ o  source string:  "title.3-title.4;title.15-title.16"
        # ⋅    .definition:    (
        # ⋅                     (
        # ⋅                      ((None, 'title'), ('int', 3)),
        # ⋅                      ((None, 'title'), ('int', 4))
        # ⋅                     ),
        # ⋅                     (
        # ⋅                      (((None, 'title'), ('int', 15)),
        # ⋅                      ((None, 'title'), ('int', 16))),
        # ⋅                     )
        # ⋅                    )
        # ⋅
        # ⋅ Special syntax for monoref stored as a biref:
        # ⋅
        # ⋅ o  source string:  "title.3-"
        # ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
        # ⋅                                                      ^
        # ⋅                                         special syntax here: we do not repeat
        # ⋅                                             ((None, 'title'), ('int', 3))
        if definition:
            self.definition = self._get_reduced_definition(definition,
                                                           keep_iter_infos=keep_iter_infos)
            self.is_valid = self.valid_definition()

            if not self.is_valid:
                # (pimydoc)error::TEXTREF-ERRORID001
                # ⋅ An error occured while creating a TextRef* object : the object isn't valid.
                error = MusaMusaError()
                error.msgid = "TEXTREF-ERRORID001"
                error.msg = "The TextRef* object has been checked and is invalid : " \
                    f"Returned explanation is '{self.valid_definition(explicit=True)}'."
                self.errors.append(error)

        else:
            self.definition = tuple()

    def __iter__(self):
        """
            TextRefBaseClass.__iter__()

            Generator yielding multirefs made of every (monoref1, None) inside <self>.
            ___________________________________________________________________

            (pimydoc)iterating over a TextRef* object
            ⋅ The __iter__() methods yields multiref made of (mono-ref, None).
            ⋅
            ⋅     for monoref in TextRefDefault().init_from_str("title.33b.α-title.33j")
            ⋅ will yield
            ⋅     title.33b.α, title.33b.β, ..., title.33b.ω, title.33c.α, ... title.33j.ω
            ⋅
            ⋅     for monoref in TextRefOEVerses().init_from_str("title.43a-title.45b")
            ⋅ will yield:
            ⋅     title.43a, title.43b, title.44a, title.44b, title.45a, title.45b
            ⋅
            ⋅     for monoref in TextRefOEVerses().init_from_str("bk.1.chapter.y-bk.2.chapter.a")
            ⋅ will yield:
            ⋅     bk.1.chapter.y, bk.1.chapter.z, bk.2.chapter.a
            ⋅
            ⋅ If errors, nothing is yielded.
        """
        # ==== [ITERREF001] "-titre" > Nothing yielded (erroneous ref object) =
        if self.errors:
            return

        # ==== [ITERREF002] normal case =======================================
        # _definition will be a modified <.definition>, hence the lists:
        _definition = self._multiref_as_lists(self.definition)

        for mono_or_biref in _definition:
            monoref1, monoref2 = mono_or_biref
            # monoref1 = {types common to monoref1 and monoref2} + what's lie after in monoref2
            if monoref2:
                monoref1 = self._monoref_extend_with_the_same_structure_as(monoref1,
                                                                           monoref2)

            # first mono-ref to be yielded is <self> without any mono-ref#2
            yield type(self)(self._multiref_as_tuples(((monoref1, None),)))

            stop = False
            while not stop:
                if monoref2 is None:
                    # If no monoref2 (like in "titre.42") only the first mono-ref is yielded:
                    stop = True
                    continue

                # let's go on: is there a successor to monoref1 ?
                next_monoref1 = self._monoref_getsuccessor(monoref1)
                if next_monoref1 is None:
                    # no successor to monoref1:
                    stop = True
                    continue

                # yes there is a successor to _definition[0][0], so let's initialize
                # monoref1 with its successor:
                monoref1 = next_monoref1

                # (pimydoc)_cmp_monoref_vs_monoref:returned value
                # ⋅ An integer is returned by TextRefBaseClass._cmp_monoref_vs_monoref():
                # ⋅
                # ⋅ o  (! #0) invalid comparison, as in "" compared to "Bible.Genesis.33"
                # ⋅
                # ⋅ o  (= #1) "M1 is equal to M2" (M1 = M2) as in "title.33a" compared to
                # ⋅           "title.33a"
                # ⋅    Please note that you can't write "title.33a" ⊂ "title.33a"
                # ⋅    Please note that you can't write "title.33a" ⊃ "title.33a"
                # ⋅
                # ⋅ o  (> #2) "M1 is placed after M2" (M1 > M2) as in "title.34" compared to
                # ⋅           "title.33"
                # ⋅
                # ⋅ o  (< #3) "M1 is placed before M2" (M1 < M2) as in "title.33" compared to
                # ⋅           "title.34"
                # ⋅
                # ⋅ o  (⊂ #4) "M1 is placed inside M2" (M1 ⊂ M2) as in "title.33a" ⊂ "title.33"
                # ⋅    Please note that you can't write "title.33a" ⊂ "title.33a"
                # ⋅
                # ⋅ o  (⊃ #5) "M1 contains M2" (M1 ⊃ M2) as in "title.33" ⊃ "title.33a"
                # ⋅    Please note that you can't write "title.33a" ⊃ "title.33a"
                if self._cmp_monoref_vs_monoref(monoref1, monoref2) in (2,):
                    # upper limit has been reached:
                    stop = True
                else:
                    yield type(self)(self._multiref_as_tuples(((monoref1, None),)))

    def __le__(self,
               textref2):
        """
            TextRefBaseClass.__le__()

            Is self <= textref2 ?

            Since TextRef* classes can't be ordered, raise an NotImplementedError exception.
            ___________________________________________________________________

            ARGUMENT:
            o  (TextRef* class) textref2

            RETURNED VALUE: (bool)
                see https://docs.python.org/3/reference/datamodel.html#object.__le__
        """
        raise NotImplementedError

    def __lt__(self,
               textref2):
        """
            TextRefBaseClass.__lt__()

            Is self < textref2 ?

            Since TextRef* classes can't be ordered, raise an NotImplementedError exception.
            ___________________________________________________________________

            ARGUMENT:
            o  (TextRef* class) textref2

            RETURNED VALUE: (bool)
                see https://docs.python.org/3/reference/datamodel.html#object.__lt__
        """
        raise NotImplementedError

    def __ne__(self,
               textref2):
        """
            TextRefBaseClass.__ne__()

            Is self != textref2 ?
            ___________________________________________________________________

            ARGUMENT:
            o  textref2: a TextRef* class

            RETURNED VALUE: (bool)
                see https://docs.python.org/3/reference/datamodel.html#object.__eq__
        """
        return self.definition != textref2.definition

    def __str__(self):
        """
                TextRefBaseClass.__str__()
        """
        return str(self.definition)

    def _cmp_biref_vs_biref(self,
                            biref1,
                            biref2):
        """
            TextRefBaseClass._cmp_biref_vs_biref()

            Internal method: compare a biref with a biref and tell if
                             biref1 is undefined / equal / inside / outside_xxx biref2.

            -------------------------------------------------------------------

            ARGUMENTS:
                o  biref1 (vide infra)
                o  biref2 (vide infra)

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

            RETURNED VALUE: (int)
                (pimydoc)_cmp_biref_vs_biref:returned value
                ⋅ An integer is returned by TextRefBaseClass._cmp_biref_vs_biref():
                ⋅
                ⋅ o  (#0) undefined        as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
                ⋅                                ("Old Testament.III.11" - "Odyssey.III.11")
                ⋅ o  (#1) equal            as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
                ⋅                                ("Odyssey.III.11" - "Odyssey.III.11")
                ⋅ o  (#2) inside           as in ("Odyssey.III.10" - "Odyssey.III.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
                ⋅ o  (#3) outside_before   as in ("Odyssey.II.10" - "Odyssey.II.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
                ⋅ o  (#4) outside_after    as in ("Odyssey.IV.10" - "Odyssey.IV.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
                ⋅ o  (#5) outside_overlap  as in ("Odyssey.III.10" - "Odyssey.IV.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
        """
        # [CMPBIREFVSBIREF001]
        # "" compared to "" > 0
        #
        # [CMPBIREFVSBIREF002]
        # "Odyssey.III.11-Odyssey.III.11" cmpd to "Old Testament.III.11-Odyssey.III.11" > 0
        #
        # [CMPBIREFVSBIREF003]
        # "Odyssey.III.11-Odyssey.III.11" compared to "Odyssey.III.11-Odyssey.III.11" > 1
        #
        # [CMPBIREFVSBIREF004]
        # "title.33c-title.33e" compared to "title.33c-title.33e" > 1
        #
        # [CMPBIREFVSBIREF005]
        # "Odyssey.III.10-Odyssey.III.11" compared to "Odyssey.III" > 2
        #
        # [CMPBIREFVSBIREF009]
        # "Odyssey.III.11-Odyssey.III.12" compared to "Odyssey.III-Odyssey.IV" > 2
        #
        # [CMPBIREFVSBIREF006]
        # "Odyssey.II.10-Odyssey.II.11" compared to "Odyssey.III" > 3
        #
        # [CMPBIREFVSBIREF011]
        # "Iliad.II.10-Iliad.II.11" compared to "Odyssey.III" > 3
        #
        # [CMPBIREFVSBIREF007]
        # "Odyssey.IV.10-Odyssey.IV.11" compared to "Odyssey.III" > 4
        #
        # [CMPBIREFVSBIREF012]
        # "Odyssey.IV.10-Odyssey.IV.11" compared to "Iliad.III" > 4
        #
        # [CMPBIREFVSBIREF008]
        # "Odyssey.III.10-Odyssey.V.11" compared to "Odyssey.III" > 5
        #
        # [CMPBIREFVSBIREF010]
        # "title.33c-title.33e" compared to "title.33c" > 5
        res1 = self._cmp_monoref_vs_biref(biref1[0], biref2)

        # (special syntax)
        #
        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be made of tuples without
        # ⋅ any list.
        # ⋅
        # ⋅ o  source string:  "title.3-title.4"
        # ⋅    .definition:    (
        # ⋅                     ((None, 'title'), ('int', 3)),
        # ⋅                     ((None, 'title'), ('int', 4))
        # ⋅                    )
        # ⋅
        # ⋅ o  source string:  "title.3-title.4;title.15-title.16"
        # ⋅    .definition:    (
        # ⋅                     (
        # ⋅                      ((None, 'title'), ('int', 3)),
        # ⋅                      ((None, 'title'), ('int', 4))
        # ⋅                     ),
        # ⋅                     (
        # ⋅                      (((None, 'title'), ('int', 15)),
        # ⋅                      ((None, 'title'), ('int', 16))),
        # ⋅                     )
        # ⋅                    )
        # ⋅
        # ⋅ Special syntax for monoref stored as a biref:
        # ⋅
        # ⋅ o  source string:  "title.3-"
        # ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
        # ⋅                                                      ^
        # ⋅                                         special syntax here: we do not repeat
        # ⋅                                             ((None, 'title'), ('int', 3))
        if biref1[1] is not None:
            res2 = self._cmp_monoref_vs_biref(biref1[1], biref2)
        else:
            res2 = self._cmp_monoref_vs_biref(biref1[0], biref2)

        if res1 == 0 or res2 == 0:
            # [CMPBIREFVSBIREF001]
            # "" compared to "" > 0
            #
            # [CMPBIREFVSBIREF002]
            # "Odyssey.III.11-Odyssey.III.11" compared to "Old Testament.III.11-Odyssey.III.11" > 0
            return 0

        if res1 == res2:
            # a special case
            #
            # [CMPBIREFVSBIREF004]
            # "titre.33c-titre.33e" compared to "titre.33c-titre.33e" > 1
            if res1 == 2 and \
               biref1[1] and \
               biref2[1] and \
               __class__._cmp_monoref_vs_monoref_eq(biref1[0], biref2[0]) and \
               __class__._cmp_monoref_vs_monoref_eq(biref1[1], biref2[1]):
                return 1

            return res1

        # [CMPBIREFVSBIREF008]
        # "Odyssey.III.10-Odyssey.V.11" compared to "Odyssey.III" > 5
        return 5

    def _cmp_monoref_vs_biref(self,
                              monoref1,
                              biref2):
        """
            TextRefBaseClass._cmp_monoref_vs_biref()

            Internal method: compare a monoref with a biref and tell if
                             monoref1 is undefined / equal / inside / outside_xxx biref2.

            -------------------------------------------------------------------

            ARGUMENTS:
                o  monoref1 (vide infra)
                o  biref2 (vide infra)

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

            RETURNED VALUE: (int)
                (pimydoc)_cmp_monoref_vs_biref:returned value
                ⋅ An integer is returned by TextRefBaseClass._cmp_monoref_vs_biref():
                ⋅
                ⋅ o  (#0) undefined        as in "title.34a" compared to (title.34a, title34)
                ⋅ o  (#1) equal            as in "title.34" compared to (title.34, title34)
                ⋅ o  (#2) inside           as in "title.34" compared to (title.34, title36)
                ⋅ o  (#3) outside_before   as in "title.33" compared to (title.33b, title36)
                ⋅ o  (#4) outside_after    as in "title.33" compared to (title.30, title31)
                ⋅ o  (#5) outside_overlap  as in "title.33a" compared to (title.33, title33a1)
        """
        # [CMPMONOREFVSBIREF001], {"..."} representing a monoref.
        # {""} vs "" > 0
        #
        # [CMPMONOREFVSBIREF002], {"..."} representing a monoref.
        # {""} compared to "Odyssey.III.11" > 0
        #
        # [CMPMONOREFVSBIREF003], {"..."} representing a monoref.
        # {"Odyssey.III.11"} compared to "Odyssey.III.11" > 1
        #
        # [CMPMONOREFVSBIREF004], {"..."} representing a monoref.
        # {"Odyssey.III.11"} compared to "Odyssey.III.10-Odyssey.III.12" > 2
        #
        # [CMPMONOREFVSBIREF005], {"..."} representing a monoref.
        # {"Odyssey.III"} compared to "Odyssey.III.10-Odyssey.IV" > 3
        #
        # [CMPMONOREFVSBIREF008], {"..."} representing a monoref.
        # {"Iliad.III"} compared to "Odyssey.III.10-Odyssey.IV" > 3
        #
        # [CMPMONOREFVSBIREF006], {"..."} representing a monoref.
        # {"Odyssey.VII"} compared to "Odyssey.III.10-Odyssey.IV" > 4
        #
        # [CMPMONOREFVSBIREF009], {"..."} representing a monoref.
        # {"Odyssey.III"} compared to "Iliad.III.10-Iliad.IV" > 4
        #
        # [CMPMONOREFVSBIREF007], {"..."} representing a monoref.
        # {"Odyssey.III.10"} compared to "Odyssey.III-Odyssey.III.10.1" > 5
        res1 = self._cmp_monoref_vs_monoref(biref2[0], monoref1)

        # (special syntax)
        #
        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be made of tuples without
        # ⋅ any list.
        # ⋅
        # ⋅ o  source string:  "title.3-title.4"
        # ⋅    .definition:    (
        # ⋅                     ((None, 'title'), ('int', 3)),
        # ⋅                     ((None, 'title'), ('int', 4))
        # ⋅                    )
        # ⋅
        # ⋅ o  source string:  "title.3-title.4;title.15-title.16"
        # ⋅    .definition:    (
        # ⋅                     (
        # ⋅                      ((None, 'title'), ('int', 3)),
        # ⋅                      ((None, 'title'), ('int', 4))
        # ⋅                     ),
        # ⋅                     (
        # ⋅                      (((None, 'title'), ('int', 15)),
        # ⋅                      ((None, 'title'), ('int', 16))),
        # ⋅                     )
        # ⋅                    )
        # ⋅
        # ⋅ Special syntax for monoref stored as a biref:
        # ⋅
        # ⋅ o  source string:  "title.3-"
        # ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
        # ⋅                                                      ^
        # ⋅                                         special syntax here: we do not repeat
        # ⋅                                             ((None, 'title'), ('int', 3))
        if biref2[1] is not None:
            res2 = self._cmp_monoref_vs_monoref(monoref1, biref2[1])
        else:
            res2 = self._cmp_monoref_vs_monoref(monoref1, biref2[0])

        if res1 == 0 or res2 == 0:
            # [CMPMONOREFVSBIREF001], {"..."} representing a monoref.
            # {""} vs "" > 0
            #
            # [CMPMONOREFVSBIREF002], {"..."} representing a monoref.
            # {""} compared to "Odyssey.III.11" > 0
            return 0

        return self._cmp_monoref_vs_biref__data[res1, res2]

    def _cmp_monoref_vs_monoref(self,
                                monoref1,
                                monoref2):
        """
            TextRefBaseClass._cmp_monoref_vs_monoref()

            Internal method: compare two monorefs and tell if
                             monoref1 is "!", "=", ">", "<", "⊂", "⊃" monoref2.

            (special syntax)
            (pimydoc)TextRefBaseClass.definition content
            ⋅ At the end of the initialisation, .definition must be made of tuples without
            ⋅ any list.
            ⋅
            ⋅ o  source string:  "title.3-title.4"
            ⋅    .definition:    (
            ⋅                     ((None, 'title'), ('int', 3)),
            ⋅                     ((None, 'title'), ('int', 4))
            ⋅                    )
            ⋅
            ⋅ o  source string:  "title.3-title.4;title.15-title.16"
            ⋅    .definition:    (
            ⋅                     (
            ⋅                      ((None, 'title'), ('int', 3)),
            ⋅                      ((None, 'title'), ('int', 4))
            ⋅                     ),
            ⋅                     (
            ⋅                      (((None, 'title'), ('int', 15)),
            ⋅                      ((None, 'title'), ('int', 16))),
            ⋅                     )
            ⋅                    )
            ⋅
            ⋅ Special syntax for monoref stored as a biref:
            ⋅
            ⋅ o  source string:  "title.3-"
            ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
            ⋅                                                      ^
            ⋅                                         special syntax here: we do not repeat
            ⋅                                             ((None, 'title'), ('int', 3))

            -------------------------------------------------------------------

            ARGUMENTS:
                o  monoref1 (vide infra)
                o  monoref2 (vide infra)

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

            RETURNED VALUE: (int)
                (pimydoc)_cmp_monoref_vs_monoref:returned value
                ⋅ An integer is returned by TextRefBaseClass._cmp_monoref_vs_monoref():
                ⋅
                ⋅ o  (! #0) invalid comparison, as in "" compared to "Bible.Genesis.33"
                ⋅
                ⋅ o  (= #1) "M1 is equal to M2" (M1 = M2) as in "title.33a" compared to
                ⋅           "title.33a"
                ⋅    Please note that you can't write "title.33a" ⊂ "title.33a"
                ⋅    Please note that you can't write "title.33a" ⊃ "title.33a"
                ⋅
                ⋅ o  (> #2) "M1 is placed after M2" (M1 > M2) as in "title.34" compared to
                ⋅           "title.33"
                ⋅
                ⋅ o  (< #3) "M1 is placed before M2" (M1 < M2) as in "title.33" compared to
                ⋅           "title.34"
                ⋅
                ⋅ o  (⊂ #4) "M1 is placed inside M2" (M1 ⊂ M2) as in "title.33a" ⊂ "title.33"
                ⋅    Please note that you can't write "title.33a" ⊂ "title.33a"
                ⋅
                ⋅ o  (⊃ #5) "M1 contains M2" (M1 ⊃ M2) as in "title.33" ⊃ "title.33a"
                ⋅    Please note that you can't write "title.33a" ⊃ "title.33a"
        """
        # [CMPMONOREFVSMONOREF001], {"..."} representing a monoref.
        # {""} vs {""} > 0
        #
        # [CMPMONOREFVSMONOREF002], {"..."} representing a monoref.
        # {"50.43"} compared to {"first.part.43.12"} > 0
        #
        # [CMPMONOREFVSMONOREF003], {"..."} representing a monoref.
        # {"Odyssey.III.10"} compared to {"Odyssey.III.10"} > 1
        #
        # [CMPMONOREFVSMONOREF004], {"..."} representing a monoref.
        # {"Odyssey.III.11"} compared to {"Odyssey.III.10"} > 2
        #
        # [CMPMONOREFVSMONOREF005], {"..."} representing a monoref.
        # {"Odyssey.III.10"} compared to {"Odyssey.III.11"} > 3
        #
        # [CMPMONOREFVSMONOREF008], {"..."} representing a monoref.
        # {"Iliad.III.10"} compared to {"Odyssey.III.11"} > 3
        #
        # [CMPMONOREFVSMONOREF006], {"..."} representing a monoref.
        # {"Odyssey.III.11"} compared to {"Odyssey.III"} > 4
        #
        # [CMPMONOREFVSMONOREF009], {"..."} representing a monoref.
        # {"Odyssey.III.10"} compared to {"Iliad.III.11"} > 4
        #
        # [CMPMONOREFVSMONOREF007], {"..."} representing a monoref.
        # {"Odyssey.III"} compared to {"Odyssey.III.11"} > 5        len__monoref1 = len(monoref1)
        len__monoref1 = len(monoref1)
        len__monoref2 = len(monoref2)

        if len__monoref1 == 0 or len__monoref2 == 0:
            # [CMPMONOREFVSMONOREF001], {"..."} representing a monoref.
            # {""} vs {""} > 0
            return 0

        # [CMPMONOREFVSMONOREF003]
        # {"Odyssey.III.10"} compared to {"Odyssey.III.10"} > 1
        res = 1  # by default, equality.
        stop = False
        index = 0
        while not stop:
            if index >= len__monoref1 or index >= len__monoref2:
                if len__monoref1 > len__monoref2:
                    # "titre.IV", "titre"
                    #          ^            ^
                    #
                    # [CMPMONOREFVSMONOREF006], {"..."} representing a monoref.
                    # {"Odyssey.III.11"} compared to {"Odyssey.III"} > 4
                    res = 4
                elif len__monoref1 < len__monoref2:
                    # "titre", "titre.IV"
                    #         ^           ^
                    # [CMPMONOREFVSMONOREF007], {"..."} representing a monoref.
                    # {"Odyssey.III"} compared to {"Odyssey.III.11"} > 5
                    res = 5

                stop = True

            elif monoref1[index][0] != monoref2[index][0]:
                # can't compare monoref1 and monoref2:
                #
                # [CMPMONOREFVSMONOREF002], {"..."} representing a monoref.
                # {"50.43"} compared to {"first.part.43.12"} > 0
                res = 0
                stop = True

            elif monoref1[index][0] is None and monoref2[index][0] is None:
                # let's use ._cmp_strs() to compare two strings,
                # monoref1[index][1] and monoref2[index][1].

                # "titre.III.second part.2" vs "titre.III.third part.3"
                #                     ^                          ^
                #
                # [CMPMONOREFVSMONOREF008], {"..."} representing a monoref.
                # {"Iliad.III.10"} compared to {"Odyssey.III.11"} > 3
                #
                # [CMPMONOREFVSMONOREF009], {"..."} representing a monoref.
                # {"Odyssey.III.10"} compared to {"Iliad.III.11"} > 4
                _res = self._cmp_strs(monoref1[index][1],
                                      monoref2[index][1])

                # we have to translate _cmp_strs:returned value to
                # _cmp_monoref_vs_monoref returned value.
                #
                # (pimydoc)_cmp_strs:returned value
                # ⋅ 0 si str1==str2, -1 if str1<str2, +1 if str>str2
                if _res == -1:
                    res = 3
                    stop = True
                elif _res == +1:
                    res = 2
                    stop = True

            # last case : neither monoref1 neither monoref2 is None:
            else:
                if monoref1[index][1] > monoref2[index][1]:
                    # [CMPMONOREFVSMONOREF004], {"..."} representing a monoref.
                    # {"Odyssey.III.11"} compared to {"Odyssey.III.10"} > 2
                    res = 2
                    stop = True

                elif monoref1[index][1] < monoref2[index][1]:
                    # [CMPMONOREFVSMONOREF005], {"..."} representing a monoref.
                    # {"Odyssey.III.10"} compared to {"Odyssey.III.11"} > 3
                    res = 3
                    stop = True

            index += 1
        return res

    @staticmethod
    def _cmp_monoref_vs_monoref_almost_eq(monoref1,
                                          monoref2):
        """
            TextRefBaseClass._cmp_monoref_vs_monoref_almost_eq()

            Internal method: we check that all elements items in monoref1 and monoref2
                             are equal (typevalue+value) EXCEPT THE LAST ITEM
                             whose typevalue must be the same but whose value
                             may differ.
                             The length of monoref1 and monoref2 can't differ:
                             if length differs, this method returns False

            Some examples:
                        book.3.4 vs another_book.1.4 : res=False
                        book.3.4 vs book.1.4         : res=False
                        book.1.4 vs book.1.4         : res=True
                        book.1.4 vs book.1.5         : res=True
            ___________________________________________________________________

            ARGUMENTS:
            o  monoref1: the first monoref to be compared
            o  monoref2: the second monoref to be compared

            RETURNED VALUE: (bool)True if <monoref1> and <monoref2> are "almost" equal.
        """
        len_monoref2 = len(monoref2)

        if len(monoref1) != len_monoref2:
            return False

        res = True
        for index, item1 in enumerate(monoref1):

            if index >= len_monoref2:
                break

            item2 = monoref2[index]
            if item1[0] != item2[0]:
                res = False
                break

            if index != len_monoref2-1 and item1[1] != item2[1]:
                res = False
                break

        return res

    @staticmethod
    def _cmp_monoref_vs_monoref_eq(monoref1,
                                   monoref2):
        """
            TextRefBaseClass._cmp_monoref_vs_monoref_eq()

            Internal method: we check that all elements items in monoref1 and monoref2
                             are equal (typevalue+value)
                             The length of monoref1 and monoref2 can't differ:
                             if length differs, this method returns False

            This method is identical in result, but faster, than:
                TextRefBaseClass()._cmp_monoref_vs_monoref(monoref1,
                                                           monoref2) == 1

            Some examples:
                        book.3.4 vs another_book.1.4 : res=False
                        book.3.4 vs book.1.4         : res=False
                        book.1.4 vs book.1.4         : res=True
                        book.1.4 vs book.1.5         : res=False
            ___________________________________________________________________

            ARGUMENTS:
            o  monoref1: the first monoref to be compared
            o  monoref2: the second monoref to be compared

            RETURNED VALUE: (bool)True if <monoref1> and <monoref2> are equal.
        """
        len_monoref2 = len(monoref2)

        if len(monoref1) != len_monoref2:
            return False

        res = True
        for index, item1 in enumerate(monoref1):

            if index >= len_monoref2:
                break

            item2 = monoref2[index]
            if item1[0] != item2[0]:
                res = False
                break

            if item1[1] != item2[1]:
                res = False
                break

        return res

    def _cmp_multiref_vs_multiref(self,
                                  multiref1,
                                  multiref2):
        """
            TextRefBaseClass._cmp_multiref_vs_multiref()

            Internal method: compare a multiref with a multiref and tell if
                             multiref1 is undefined / equal / inside / outside_xxx multiref2.

            -------------------------------------------------------------------

            ARGUMENTS:
                o  multiref1 (vide infra)
                o  multiref2 (vide infra)

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

            RETURNED VALUE: (int)
                (pimydoc)_cmp_multiref_vs_multiref:returned value
                ⋅ An integer is returned by TextRefBaseClass._cmp_multiref_vs_multiref():
                ⋅
                ⋅ o  (#0) undefined        as in ("Odyssey.III.11" - "Odyssey.III.11"); compared to
                ⋅                                ("Old Testament.III.11" - "Odyssey.III.11")
                ⋅ o  (#1) equal            as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
                ⋅                                ("Odyssey.III.11" - "Odyssey.III.11")
                ⋅ o  (#2) inside           as in ("Odyssey.III.10" - "Odyssey.III.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
                ⋅ o  (#3) outside_before   as in ("Odyssey.II.10" - "Odyssey.II.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
                ⋅ o  (#4) outside_after    as in ("Odyssey.IV.10" - "Odyssey.IV.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
                ⋅ o  (#5) outside_overlap  as in ("Odyssey.III.10" - "Odyssey.IV.11") compared to
                ⋅                                ("Odyssey.III" - "Odyssey.III")
        """
        # [CMPMULTIREFVSMULTIREF001]
        # "" compared to "" > 0
        #
        # [CMPMULTIREFVSMULTIREF002]
        # "Odyssey.III.11" compared to "" > 0
        #
        # [CMPMULTIREFVSMULTIREF005]
        # "Odyssey.III.11" compared to "Odyssey.III.11" > 1
        #
        # [CMPMULTIREFVSMULTIREF006]
        # "Odyssey.III.11-Odyssey.III.12" compared to "Odyssey.III.11-Odyssey.III.12" > 1
        #
        # [CMPMULTIREFVSMULTIREF007]
        # "Odyssey.III.11" compared to "Odyssey.III" > 2
        #
        # [CMPMULTIREFVSMULTIREF008]
        # "Odyssey.III.11-Odyssey.III.12" compared to "Odyssey.III" > 2
        #
        # [CMPMULTIREFVSMULTIREF009]
        # "Odyssey.III.11-Odyssey.III.12" compared to "Odyssey.III-Odyssey.IV" > 2
        #
        # [CMPMULTIREFVSMULTIREF010]
        # "Odyssey.III.11" compared to "Odyssey.III-Odyssey.IV" > 2
        #
        # [CMPMULTIREFVSMULTIREF011]
        # "Odyssey.III.11;Odyssey.IV.12" compared to "Odyssey.III-Odyssey.IV" > 2
        #
        # [CMPMULTIREFVSMULTIREF012]
        # "Odyssey.II.11" compared to "Odyssey.III.11" > 3
        #
        # [CMPMULTIREFVSMULTIREF013]
        # "Odyssey.II.11-Odyssey.II.12" compared to "Odyssey.III.11" > 3
        #
        # [CMPMULTIREFVSMULTIREF014]
        # "Odyssey.II.11-Odyssey.II.12" compared to "Odyssey.III.11-Odyssey.III.12" > 3
        #
        # [CMPMULTIREFVSMULTIREF015]
        # "Odyssey.II.11" compared to "Odyssey.III.11-Odyssey.III.12" > 3
        #
        # [CMPMULTIREFVSMULTIREF003]
        # "Iliad.II.11" compared to "Odyssey.III.11-Odyssey.III.12" > 3
        #
        # [CMPMULTIREFVSMULTIREF016]
        # "Odyssey.III.11" compared to "Odyssey.II.11" > 4
        #
        # [CMPMULTIREFVSMULTIREF017]
        # "Odyssey.III.11-Odyssey.III.12" compared to "Odyssey.II.11" > 4
        #
        # [CMPMULTIREFVSMULTIREF018]
        # "Odyssey.III.11-Odyssey.III.12" compared to "Odyssey.II.11-Odyssey.II.12" > 4
        #
        # [CMPMULTIREFVSMULTIREF019]
        # "Odyssey.III.11" compared to "Odyssey.II.11-Odyssey.II.12" > 4
        #
        # [CMPMULTIREFVSMULTIREF004]
        # "Odyssey.III.11" compared to "Iliad.II.11-Iliad.II.12" > 4
        #
        # [CMPMULTIREFVSMULTIREF020]
        # "Odyssey.II.9-Odyssey.II.12" compared to "Odyssey.II.11-Odyssey.II.12" > 5
        #
        # [CMPMULTIREFVSMULTIREF021]
        # "Odyssey.II.11-Odyssey.II.13" compared to "Odyssey.II.11-Odyssey.II.12" > 5
        #
        # [CMPMULTIREFVSMULTIREF022]
        # "Odyssey.II.12-Odyssey.II.14" compared to "Odyssey.II.11-Odyssey.II.12" > 5
        #
        # [CMPMULTIREFVSMULTIREF023]
        # "Odyssey.II.10-Odyssey.II.14" compared to "Odyssey.II.11" > 5
        #
        # [CMPMULTIREFVSMULTIREF024]
        # "Odyssey.II.10-Odyssey.II.11" compared to "Odyssey.II.11" > 5
        #
        # [CMPMULTIREFVSMULTIREF025]
        # "Odyssey.II.11-Odyssey.II.12" compared to "Odyssey.II.11" > 5
        res = None
        stop = False

        for biref1 in multiref1:
            if stop:
                break

            for biref2 in multiref2:
                r_temp = self._cmp_biref_vs_biref(biref1,
                                                  biref2)

                if res is None:
                    res = r_temp
                elif r_temp == 0:
                    res = 0
                    stop = True
                elif res != r_temp:
                    res = 5
                    # no "stop = True" indeed.
                    # The loop doesn't stop here since later it may encounter a '0' result.

                if stop:
                    break

        if res is None:
            res = 0
        return res

    @staticmethod
    def _default_cmp_strs(str1,
                          str2):
        """
            TextRefBaseClass._default_cmp_strs()

            Default function used to compare two strings by the ._cmp* methods.
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)str1 : the first string to be compared
            o  (str)str2 : the second string to be compared

            RETURNED VALUE:
                (pimydoc)_cmp_strs:returned value
                ⋅ 0 si str1==str2, -1 if str1<str2, +1 if str>str2
        """
        if str1 == str2:
            return 0
        if str1 < str2:
            return -1
        return +1

    def _get_reduced_definition(self,
                                definition,
                                keep_iter_infos=True):
        """
            TextRefBaseClass._get_reduced_definition()

            Return <definition> after reducing the informations.
            By example, "book1;title1;book1;title2" > "book1;title1;title2".
            ___________________________________________________________________

            ARGUMENT:
              o  (bool)keep_iter_infos
                 By default (keep_iter_infos == True) the method keeps the informations required to
                 iter.
                 By example, "title.33.a-title.33.z" will not change in order to yield:
                        "title.33.a"
                        "title.33.b"
                        ...
                        "title.33.z"
                 If keep_iter_infos is False, the methods doesn't keep the informations required to
                 iter.
                 By example, "title.33.a-title.33.z" will become "title.33", yielding only:
                        "title.33"

            no RETURNED VALUE
        """
        # I don't want to split this long method into several sub-methods for the sake of speed
        # and because it would be complex. Let's hope the documentation is sufficient!
        # pylint: disable=too-many-branches

        # [REDUCEDEFINITION001] "delete same birefs"
        #    "book1;title1;book1;title2" > "book1;title1;title2"
        #
        # side-effect of REDUCEDEFINITION001
        # initial definition mixing lists and tuples becomes a tuple-only definition:
        #
        # [REDUCEDEFINITION002] "aggregate (successor)"
        #    "Title.31;Title.32.d;Title.32.e"
        #        > "Title.31;Title.32.d-Title.32.e"
        #
        # [REDUCEDEFINITION003] "aggregate (equality)"
        #    "Title.31;Title.32.b-Title.32.d;Title.32.d-Title.32.e"
        #        > "Title.31;Title.32.b-Title.32.e"
        #
        # [REDUCEDEFINITION004] "extrems up" (!!! if keep_iter_infos is set to False)
        #     "title.33.a-title.33.z" > "title.33"
        #
        # [REDUCEDEFINITION005] "merge duplicate"
        #       "title1-title3;title2" > "title1-title3
        definition = __class__._multiref_as_lists(definition)

        stop = False
        while not stop:
            stop = True  # will be "False" if definition has been modified

            # <modification> format:
            #
            # * either None if no modification to <definition> is expected.
            #
            # * either (0x01, index2)
            #       : biref2 is equal or inside biref, just pop(index2)
            #
            # * either (0x02, index, biref, biref2)
            #       : we have to aggregate (successor) biref and biref2
            #         "Title.31;Title.32.d;Title.32.e"
            #             > "Title.31;Title.32.d-Title.32.e"
            #
            # * either (0x03, index, biref, biref2)
            #       : we have to aggregate (equality) biref and biref2
            #         "Title.31;Title.32.b-Title.32.d;Title.32.d-Title.32.e"
            #             > "Title.31;Title.32.b-Title.32.e"
            #
            # * either (0x04, index)
            #       : "extrems up" if keep_iter_infos is False
            #         "title.33.a-title.33.z" > "title.33"
            #
            modification = None
            for index, biref in enumerate(definition):

                # ---- 0x04 ---------------------------------------------------
                if keep_iter_infos is False:
                    # [REDUCEDEFINITION004] "extrems up" (!!! if keep_iter_infos is set to False)
                    #     "title.33.a-title.33.z" > "title.33"
                    #
                    if biref[1] and \
                       __class__._cmp_monoref_vs_monoref_almost_eq(biref[0], biref[1]) and \
                       self._monoref_has_its_rightest_item_to_its_lowest_value(biref[0]) and \
                       self._monoref_has_its_rightest_item_to_its_highest_value(biref[1]):
                        modification = (0x04, index)
                        break

                for index2 in range(index+1, len(definition)):
                    biref2 = definition[index2]

                    # ---- 0x01 -----------------------------------------------

                    # [REDUCEDEFINITION001] "delete same birefs"
                    #    "book1;title1;book1;title2" > "book1;title1;title2"
                    #
                    # [REDUCEDEFINITION005] "merge duplicate"
                    #       "title1-title3;title2" > "title1-title3

                    # biref2 is equal or inside biref
                    if self._cmp_biref_vs_biref(biref2, biref) in (1, 2):
                        modification = (0x01, index2)
                        break

                    # ---- 0x02 -----------------------------------------------

                    # [REDUCEDEFINITION002] "aggregate (successor)"
                    #    "Title.31;Title.32.d;Title.32.e"
                    #        > "Title.31;Title.32.d-Title.32.e"

                    # what's the <successor> of biref[1] (=of biref[0] if biref[1] is None) ?
                    if biref[1] is not None:
                        successor = self._monoref_getsuccessor(biref[1])
                    else:
                        successor = self._monoref_getsuccessor(biref[0])
                    if successor is not None:
                        successor = __class__._monoref_as_lists(successor)

                    # check: can we aggregate (successor) biref and biref2 ?
                    #  If True, let's break the loop to modify definition.
                    if (biref[1] is not None and
                        successor == biref2[0]) or \
                        (biref[1] is None and
                         successor == biref2[0]):
                        modification = (0x02, index, biref, biref2)
                        break

                    # ---- 0x03 -----------------------------------------------

                    # [REDUCEDEFINITION003] "aggregate (equality)"
                    #    "Title.31;Title.32.b-Title.32.d;Title.32.d-Title.32.e"
                    #        > "Title.31;Title.32.b-Title.32.e"

                    # check: can we aggregate biref and biref2 ?
                    #  If True, let's break the loop to modify definition.
                    if (biref[1] is not None and
                        __class__._cmp_monoref_vs_monoref_eq(biref[1], biref2[0])) or \
                        (biref[1] is None and
                         __class__._cmp_monoref_vs_monoref_eq(biref[0], biref2[0])):
                        modification = (0x03, index, biref, biref2)
                        break

                if modification is not None:
                    break

            # see "<modification> format" supra
            if modification is not None:
                stop = False
                if modification[0] == 0x01:
                    index2 = modification[1]
                    definition.pop(index2)
                elif modification[0] == 0x04:
                    index = modification[1]
                    definition[index] = [definition[index][0][:-1], None]
                elif modification[0] == 0x02 or modification[0] == 0x03:
                    index = modification[1]
                    biref = modification[2]
                    biref2 = modification[3]
                    if biref2[1]:
                        definition[index] = [biref[0], biref2[1]]
                    else:
                        definition[index] = [biref[0], biref2[0]]
                    definition.pop(index2)

        return __class__._multiref_as_tuples(definition)

    def _init_from_str__add_mono_or_biref(self,
                                          source_string: str):
        """
            TextRefBaseClass._init_from_str__add_mono_or_biref()

            Internal method: split mono/bi-reference string <source_string> and
                             add it to .definition .
            ___________________________________________________________________

            ARGUMENT: (str)source_string, a mono/bi-reference string like "titre.92a"
                      or "titre.92a-titre.93b"

            no RETURNED VALUE
        """
        if source_string.count(self._ref2ref_separator) > 1:
            # (pimydoc)error::TEXTREF-ERRORID000
            # ⋅ Only one TextRefBaseClass.ref2ref_separator character is allowed in a source
            # ⋅ string describing a text reference.
            # ⋅
            # ⋅ By example, the following init string...
            # ⋅     "title.43a--title.43b"
            # ⋅ ... will raise an error if TextRefBaseClass.ref2ref_separator is set to "-".
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID000"
            error.msg = f"Only one .ref2ref_separator character " \
                f"(defined here as 'self._ref2ref_separator') " \
                "is allowed in a source string describing a texte reference." \
                f"The source string '{source_string}' contains more than one of this character."
            self.errors.append(error)
            return

        ref1 = source_string
        ref2 = None
        if self._ref2ref_separator in source_string:
            ref1, ref2 = source_string.split(self._ref2ref_separator)

            # a special case:
            #   if we have "titre.3a-3b", we have to understand "titre.3a-titre.3b"
            if ref1.count(self._refsubpart_separator) > 0 and \
               ref2.count(self._refsubpart_separator) == 0 and \
               ref2 != "":
                ref2 = ref1[:ref1.rindex(self._refsubpart_separator)+1] + ref2

        # (special syntax)
        #
        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be made of tuples without
        # ⋅ any list.
        # ⋅
        # ⋅ o  source string:  "title.3-title.4"
        # ⋅    .definition:    (
        # ⋅                     ((None, 'title'), ('int', 3)),
        # ⋅                     ((None, 'title'), ('int', 4))
        # ⋅                    )
        # ⋅
        # ⋅ o  source string:  "title.3-title.4;title.15-title.16"
        # ⋅    .definition:    (
        # ⋅                     (
        # ⋅                      ((None, 'title'), ('int', 3)),
        # ⋅                      ((None, 'title'), ('int', 4))
        # ⋅                     ),
        # ⋅                     (
        # ⋅                      (((None, 'title'), ('int', 15)),
        # ⋅                      ((None, 'title'), ('int', 16))),
        # ⋅                     )
        # ⋅                    )
        # ⋅
        # ⋅ Special syntax for monoref stored as a biref:
        # ⋅
        # ⋅ o  source string:  "title.3-"
        # ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
        # ⋅                                                      ^
        # ⋅                                         special syntax here: we do not repeat
        # ⋅                                             ((None, 'title'), ('int', 3))
        if ref2 == "":
            ref2 = None

        ref1 = self._init_from_str__extract_def_from_src_mono(ref1)
        if ref2:
            ref2 = self._init_from_str__extract_def_from_src_mono(ref2)

        # The second element of a biref is replaced by None if this
        # second element is equal to the first:
        if ref1 == ref2 and ref2 is not None:
            ref2 = None

        self.definition.append((ref1, ref2))

    def _init_from_str__extract_def_from_src_mono(self,
                                                  src):
        """
            TextRefBaseClass._init_from_str__extract_def_from_src_mono()

            Apply several regexes to parse <src> and transform it into
            a list of (typevalue, value) like ('int', 43) or ('roman numbers', 12)
            ___________________________________________________________________

            ARGUMENT:
            o  (str)src: source string to be read

            RETURNED VALUE: (list)res
        """
        res = []
        # (pimydoc)TextRefBaseClass._subrefs structure
        # ⋅
        # ⋅ Beware ! If you modify _subrefs content, please rewrite
        # ⋅     o  _init_from_str__extract_def_from_src_mono()
        # ⋅     o  _monoref_definition2str()
        # ⋅ in the derived class.
        # ⋅
        # ⋅ TextRefBaseClass._subref is a tuple made of:
        # ⋅
        # ⋅     *  .regex     : (bytes)a compiled regex
        # ⋅     *  .min_value : None or (integer) minimal value
        # ⋅     *  .max_value : None or (integer) maximal value
        # ⋅     *  .char2int  : None or (a dict)  character to integer value
        # ⋅     *  .int2char  : inverse of .char2int, automatically generated
        # ⋅
        # ⋅     By example:
        # ⋅     * re.compile(r"^[a-z]$"),
        # ⋅     * 1,
        # ⋅     * 26,
        # ⋅     * {"a": 1,
        # ⋅        "b": 2,
        # ⋅        ...
        # ⋅        "z": 26}
        for _subpart in src.split(self._refsubpart_separator):
            subpart = _subpart.strip()
            if subpart:
                # ---- int ----------------------------------------------------
                _subrefs_res = re.search(self._subrefs["int"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(subpart)))
                    continue

                # ---- int+a-z(1) ---------------------------------------------
                _subrefs_res = re.search(self._subrefs["int+a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(_subrefs_res.group("subref0"))))
                    res.append(
                        ("a-z(1)",
                         self._subrefs["a-z(1)"].char2int[_subrefs_res.group("subref1")]))
                    continue

                # ---- int+A-Z(1) ---------------------------------------------
                _subrefs_res = re.search(self._subrefs["int+A-Z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(_subrefs_res.group("subref0"))))
                    res.append(
                        ("A-Z(1)",
                         self._subrefs["A-Z(1)"].char2int[_subrefs_res.group("subref1")]))
                    continue

                # ---- roman numbers ------------------------------------------
                _subrefs_res = re.search(self._subrefs["roman numbers"].regex,
                                         subpart)
                if _subrefs_res:
                    from_roman__value__ok, from_roman__value = from_roman(subpart)
                    if from_roman__value__ok is True:
                        res.append(
                            ("roman numbers",
                             from_roman__value))
                        continue

                # ---- a-z(1) -------------------------------------------------
                _subrefs_res = re.search(self._subrefs["a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("a-z(1)",
                         self._subrefs["a-z(1)"].char2int[subpart]))
                    continue

                # ---- A-Z(1) -------------------------------------------------
                _subrefs_res = re.search(
                    self._subrefs["A-Z(1)"].regex,
                    subpart)
                if _subrefs_res:
                    res.append(
                        ("A-Z(1)",
                         self._subrefs["A-Z(1)"].char2int[subpart]))
                    continue

                # ---- α-ω(1) -------------------------------------------------
                _subrefs_res = re.search(self._subrefs["α-ω(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("α-ω(1)",
                         self._subrefs["α-ω(1)"].char2int[subpart]))
                    continue

                # ---- Α-Ω(1) -------------------------------------------------
                _subrefs_res = re.search(self._subrefs["Α-Ω(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("Α-Ω(1)",
                         self._subrefs["Α-Ω(1)"].char2int[subpart]))
                    continue

                res.append(
                    (None,
                     subpart))

        return res

    def _monoref_definition2str(self,
                                monoref):
        """
            TextRefBaseClass._monoref_definition2str()

            Method used by .definition2str()

            Internal method: transform .definition into a string that could
                             be read by .init_from_str().
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be converted into a string

            RETURNED VALUE: (str)the string representing <monoref>.
        """
        _monoref = []
        for typevalue, value in monoref:
            if typevalue is None:
                _monoref.append(value)
            elif typevalue == "roman numbers":
                success, data = to_roman(value)
                if success:
                    _monoref.append(data)
                else:
                    # (pimydoc)error::TEXTREF-ERRORID004
                    # ⋅ An error occured while converting an integer into a Roman number.
                    error = MusaMusaError()
                    error.msgid = "TEXTREF-ERRORID004"
                    error.msg = f"Can't convert integer {value} into a roman number."
                    error.suberrors = (data,)
                    self.errors.append(error)

            elif value in self._subrefs[typevalue].int2char:
                _monoref.append(self._subrefs[typevalue].int2char[value])
            else:
                _monoref.append(str(value))
        return self._refsubpart_separator.join(_monoref)

    @staticmethod
    def _monoref_as_lists(monoref):
        """
            TextRefBaseClass._monoref_as_lists()

            Internal method: convert <monoref>, which can be a mix of tuples and lists
                             into a list of lists.
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be converted

            RETURNED VALUE: a monoref made of a list of lists
        """
        return [list(content) for content in monoref]

    @staticmethod
    def _monoref_as_tuples(monoref):
        """
            TextRefBaseClass._monoref_as_tuples()

            Internal method: convert <monoref>, which can be a mix of tuples and lists
                             into a tuple of tuples.
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be converted

            RETURNED VALUE: a monoref made of a tuple of tuples
        """
        return tuple(tuple(content) for content in monoref)

    def _monoref_extend_with_the_same_structure_as(self,
                                                   monoref1,
                                                   monoref2):
        """
            TextRefBaseClass._monoref_extend_with_the_same_structure_as()

            Internal method: return a monoref1 equals to monoref1 but extended
                             using monoref2, the values being minimized.

                             monoref1 + monoref2       result
                             title.33 + title.33.c.9 > title.33.a.1
                                                       |------|
                                                       monoref1
                                                               |--|
                                                           minimized monoref2 suffix

            It is expected that len(monoref1)<len(monoref2) but if
            len(monoref1)>=len(monoref2) monoref1 will be returned.

            Some examples:
               ----------|-------------|-----------------------------------------
               |monoref1 | monoref2    |                 result
               ----------|-------------|-----------------------------------------
               |"title.1", "title.1.a" > "title.1.a" (suffix ".a" can be added)
               |"title.1", "title.1.c" > "title.1.a" (suffix ".a" can be added)
               |                            (we add the minimal value)
               |"title.1", "title"     > "title.1"   (no suffix can be added)
               |"book.1",  "title.1.a" > "book.1"    (no suffix can be added)
               ----------|-------------|-----------------------------------------

            ___________________________________________________________________

            ARGUMENT:
            o  monoref1: the monoref to be extended
            o  monoref2: the monoref used to extend monoref1

            RETURNED VALUE: a monoref
        """
        res = []

        len_monoref1 = len(monoref1)
        len_monoref2 = len(monoref2)

        # ---- a special case : monoref2 has nothing that can be add to monoref1
        if len_monoref1 >= len_monoref2:
            return monoref1

        # ---- first loop: elements common to <monoref1> and <monoref2> -------
        index = 0
        stop = False
        go_on = True
        while not stop:
            if index >= len_monoref1:
                # we'are at the end of monoref1: let's go to the second loop.
                stop = True
                continue
            if index >= len_monoref2:
                # we'are at the end of monoref2: let's go to the second loop.
                stop = True
                continue
            if monoref1[index][0] != monoref2[index][0]:
                # error: types differ, there will be no second loop.
                stop = True
                go_on = False
                continue
            if monoref1[index][0] is None and monoref1[index][1] != monoref2[index][1]:
                # error: strings differ, there will be no second loop.
                stop = True
                go_on = False
                continue
            # everything's alright, let's add <monoref1[index]> (=<monoref2[index]>) to <res>.
            res.append(monoref1[index])
            index += 1

        if not go_on:
            return monoref1

        # ---- second loop: let's add elements present in <monoref2> as suffix to <monoref1>
        stop = False
        while not stop:
            if index >= len_monoref2:
                stop = True
                continue

            if monoref2[index][0] is None:
                res.append(monoref2[index])
            else:
                res.append((monoref2[index][0],
                            self._subrefs[monoref2[index][0]].min_value))

            index += 1

        return res

    def _monoref_getpredecessor(self,
                                monoref):
        """
            TextRefBaseClass._monoref_getpredecessor()

            Internal method: return the predecessor of <monoref>.

            By example, the predecessor of "title.33" is "title.32" .
            By example, the predecessor of "title.33.a" is "title.32.z" .
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref whose predecessor has to be returned.

            RETURNED VALUE: (None|tuple) either None if no successor can be returned
                                         either the predecessor
        """
        len_monoref = len(monoref)
        res = __class__._monoref_as_lists(monoref)

        index = -1
        alright = False
        stop = False

        while not stop:
            if len_monoref + index < 0:
                stop = True
            elif res[index][0] is None:
                index += -1
            elif res[index][1] > self._subrefs[res[index][0]].min_value:
                res[index][1] -= 1
                alright = True
                stop = True
            else:
                res[index][1] = self._subrefs[res[index][0]].max_value
                index += -1

        if alright:
            return __class__._monoref_as_tuples(res)

        # not alright:
        return None

    def _monoref_getsuccessor(self,
                              monoref):
        """
            TextRefBaseClass._monoref_getsuccessor()

            Internal method: return the successor of <monoref>.

            By example, the successor of "title.33" is "title.34" .
            By example, the successor of "title.33.z" is "title.34.a" .
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref whose successor has to be returned.

            RETURNED VALUE: (None|tuple) either None if no successor can be returned
                                         either the successor
        """
        len_monoref = len(monoref)
        res = __class__._monoref_as_lists(monoref)

        index = -1
        alright = False
        stop = False

        while not stop:
            if len_monoref + index < 0:
                stop = True
            elif res[index][0] is None:
                index += -1
            elif res[index][1] < self._subrefs[res[index][0]].max_value:
                res[index][1] += 1
                alright = True
                stop = True
            else:
                res[index][1] = self._subrefs[res[index][0]].min_value
                index += -1

        if alright:
            return __class__._monoref_as_tuples(res)

        # not alright:
        return None

    def _monoref_has_its_rightest_item_to_its_highest_value(self,
                                                            monoref):
        """
            TextRefBaseClass._monoref_has_its_rightest_item_to_its_highest_value()

            Internal method: return True if the last item in <monoref> has a value equal
                             to the maximal value defined in ._subrefs .

            By example "title.3.z" has its last item set to its maximal value.
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be checked

            RETURNED VALUE: (bool)True if the last item in <monoref> has its maximal value.
        """
        if len(monoref) == 0:
            return False
        return monoref[-1][1] == self._subrefs[monoref[-1][0]].max_value

    def _monoref_has_its_rightest_item_to_its_lowest_value(self,
                                                           monoref):
        """
            TextRefBaseClass._monoref_has_its_rightest_item_to_its_lowest_value()

            Internal method: return True if the last item in <monoref> has a value equal
                             to the minimal value defined in ._subrefs .

            By example "title.3.a" has its last item set to its minimal value.
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be checked

            RETURNED VALUE: (bool)True if the last item in <monoref> has its minimal value.
        """
        if len(monoref) == 0:
            return False
        return monoref[-1][1] == self._subrefs[monoref[-1][0]].min_value

    def _monoref_set_rightest_item_to_its_highest_value(self,
                                                        monoref):
        """
            TextRefBaseClass._monoref_set_rightest_item_to_its_highest_value()

            Internal method: return a modified copy of <monoref> with its last item set to a value
                             equal to the maximal value defined in ._subrefs .

            By example "title.3.a" will become "title.3.z"
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be copied and modified

            RETURNED VALUE: (monoref)the modified monoref
        """
        res = self._monoref_as_lists(monoref)
        return res[:-1] + [[res[-1][0],
                           self._subrefs[res[-1][0]].max_value]]

    def _monoref_set_rightest_item_to_its_lowest_value(self,
                                                       monoref):
        """
            TextRefBaseClass._monoref_set_rightest_item_to_its_lowest_value()

            Internal method: return a modified copy of <monoref> with its last item set to a value
                             equal to the minimal value defined in ._subrefs .

            By example "title.3.m" will become "title.3.a"
            ___________________________________________________________________

            ARGUMENT:
            o  monoref: the monoref to be copied and modified

            RETURNED VALUE: (monoref)the modified monoref
        """
        res = self._monoref_as_lists(monoref)
        return res[:-1] + [[res[-1][0],
                           self._subrefs[res[-1][0]].min_value]]

    @staticmethod
    def _multiref_as_lists(definition):
        """
            TextRefBaseClass._multiref_as_lists()

            Return <definition> with only lists.
            ___________________________________________________________________

            ARGUMENT:
            o  definition

                (pimydoc)TextRefBaseClass.definition content
                ⋅ At the end of the initialisation, .definition must be made of tuples without
                ⋅ any list.
                ⋅
                ⋅ o  source string:  "title.3-title.4"
                ⋅    .definition:    (
                ⋅                     ((None, 'title'), ('int', 3)),
                ⋅                     ((None, 'title'), ('int', 4))
                ⋅                    )
                ⋅
                ⋅ o  source string:  "title.3-title.4;title.15-title.16"
                ⋅    .definition:    (
                ⋅                     (
                ⋅                      ((None, 'title'), ('int', 3)),
                ⋅                      ((None, 'title'), ('int', 4))
                ⋅                     ),
                ⋅                     (
                ⋅                      (((None, 'title'), ('int', 15)),
                ⋅                      ((None, 'title'), ('int', 16))),
                ⋅                     )
                ⋅                    )
                ⋅
                ⋅ Special syntax for monoref stored as a biref:
                ⋅
                ⋅ o  source string:  "title.3-"
                ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
                ⋅                                                      ^
                ⋅                                         special syntax here: we do not repeat
                ⋅                                             ((None, 'title'), ('int', 3))

            RETURNED VALUE: modified <definition> with only lists.
        """
        res = []
        for monoref1, monoref2 in definition:
            _monoref1 = [[key, value] for key, value in monoref1]
            if monoref2 is not None:
                _monoref2 = [[key, value] for key, value in monoref2]
            else:
                _monoref2 = None
            res.append([_monoref1, _monoref2])
        return res

    @staticmethod
    def _multiref_as_tuples(definition):
        """
            TextRefBaseClass._multiref_as_tuples()

            Return <definition> with only tuples.
            ___________________________________________________________________

            ARGUMENT:
            o  definition

                (pimydoc)TextRefBaseClass.definition content
                ⋅ At the end of the initialisation, .definition must be made of tuples without
                ⋅ any list.
                ⋅
                ⋅ o  source string:  "title.3-title.4"
                ⋅    .definition:    (
                ⋅                     ((None, 'title'), ('int', 3)),
                ⋅                     ((None, 'title'), ('int', 4))
                ⋅                    )
                ⋅
                ⋅ o  source string:  "title.3-title.4;title.15-title.16"
                ⋅    .definition:    (
                ⋅                     (
                ⋅                      ((None, 'title'), ('int', 3)),
                ⋅                      ((None, 'title'), ('int', 4))
                ⋅                     ),
                ⋅                     (
                ⋅                      (((None, 'title'), ('int', 15)),
                ⋅                      ((None, 'title'), ('int', 16))),
                ⋅                     )
                ⋅                    )
                ⋅
                ⋅ Special syntax for monoref stored as a biref:
                ⋅
                ⋅ o  source string:  "title.3-"
                ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
                ⋅                                                      ^
                ⋅                                         special syntax here: we do not repeat
                ⋅                                             ((None, 'title'), ('int', 3))

            RETURNED VALUE: modified <definition> with only tuples.
        """
        res = []
        for monoref1, monoref2 in definition:
            _monoref1 = tuple((key, value) for key, value in monoref1)
            if monoref2 is not None:
                _monoref2 = tuple((key, value) for key, value in monoref2)
            else:
                _monoref2 = None
            res.append((_monoref1, _monoref2))
        return tuple(res)

    def add_and_sort(self,
                     textref2,
                     keep_iter_infos=True):
        """
            TextRefBaseClass.add_and_sort()

            Add <textref2.definition> to <self> and make sure that the textrefs in self.definition
            are sorted.

            By example if self is "title.3-4;title.5.a-title.5.f" and if you add "title.5.g",
            self.definition will be
                "title.3-title.4;title.5.a-title.5.g"
            ___________________________________________________________________

            ARGUMENT:
            o  textref2: TextRef* object to be added to self.definition .

            RETURNED VALUE: (bool)True if no problem occured.
        """
        # I don't want to split this long method into several sub-methods for the sake of speed
        # and because it would be complex. Let's hope the documentation is sufficient!
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements

        # [ADDANDSORT001]
        # "title.33" + "title.32"
        #       > "title.32-title.33"
        #
        # [ADDANDSORT002]
        # "title.32" + "title.33"
        #       > "title.32-title.33"
        #
        # [ADDANDSORT003]
        # "title.33b-title.33j" + "title.33e-title.33f"
        #     > "title.33b-title.33j"
        #
        # [ADDANDSORT004]
        # "title.33" + "title.33e-title.33f"
        #     > (keep_iter_infos=True)"title.33a-title.33z" / (keep_iter_infos=False)"title.33"
        #
        # [ADDANDSORT005]
        # "title.33b.α-title.33j" + "title.33e-title.33f"
        #     > "title.33b.α-title.33j"
        #
        # [ADDANDSORT006]
        # "title.33b.ξ-title.33j" + "title.33e.α-title.33k"
        #     > "title.33b.ξ-title.33k"
        #
        # [ADDANDSORT007]
        # "title.33;title.35" + "title.33.h-title.36.b"
        #     > "title.33.a-title.36.b"
        #
        # [ADDANDSORT008]
        # "title.33" + "title.33.c"
        #     > (keep_iter_infos=True)"title.33.a-title.33.z" / (keep_iter_infos=False)"title.33"
        #
        # [ADDANDSORT009]
        # "title.33c-title.33e" + "title.33c-title.33e"
        #     > "title.33c-title.33e"
        #
        # [ADDANDSORT010]
        # "title.32" + "another_title.33"
        #       > "another_title.33;title.32"
        #
        # [ADDANDSORT011]
        # "another_title.33;title.32-title.33" + "another_title.34"
        #       > "another_title.33-another_title.34;title.32-title.33"
        #
        # [ADDANDSORT012]
        # "title.31.c.title.31.f" + "title.31.a-title.31.z"
        #       > "title.31.a-title.31.b;title.31.c-title.31.f;title.31.g-title.31.z"
        # ==== a special case: <self>/textref2 isn't valid empty. =============
        if not self.is_valid:
            return False
        if not textref2.is_valid:
            return False

        # ==== a special case: <self.definition> is empty. ====================
        if not self.definition:
            self.definition = __class__._multiref_as_tuples(textref2.definition)
            return True

        # ==== normal case: self.definition is not empty. =====================
        # for each biref2 in textref2.definition and for each biref in self.definition
        # we define an <action> and we modify .definition according to this <action>.

        # <self.definition> will be modified:
        self.definition = __class__._multiref_as_lists(self.definition)

        for biref2 in textref2.definition:
            # ---- what would be the action specific to <biref2> ? ------------

            # We stop as as soon as the first possible action has been found.
            # Indeed, since self.definition is sorted, we don't have to go further.
            # By example:
            #   "another_title.33;title.32-title.33" + "another_title.34"
            #       > "another_title.33;another_title.34;title.32-title.33"
            #
            # ... the first action is "place another_title.34 AFTER another_title.33"
            # ... the second action would be "place another_title.34 BEFORE title.32-title.33"
            # Only the first action is done.
            action = None
            for index, biref in enumerate(self.definition):
                # what's the <action> to be done ?
                #
                # action:(
                #               (int){0, 1, 2, 3, 4, 5},       : res_op
                #               (int)index                     : index where the action must be done
                #               biref,                         : biref, biref2 : biref{/2} implied
                #               biref2                           for the action
                #        )
                #   action is None if no action defined

                # (pimydoc)_cmp_biref_vs_biref:returned value
                # ⋅ An integer is returned by TextRefBaseClass._cmp_biref_vs_biref():
                # ⋅
                # ⋅ o  (#0) undefined        as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
                # ⋅                                ("Old Testament.III.11" - "Odyssey.III.11")
                # ⋅ o  (#1) equal            as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
                # ⋅                                ("Odyssey.III.11" - "Odyssey.III.11")
                # ⋅ o  (#2) inside           as in ("Odyssey.III.10" - "Odyssey.III.11") compared to
                # ⋅                                ("Odyssey.III" - "Odyssey.III")
                # ⋅ o  (#3) outside_before   as in ("Odyssey.II.10" - "Odyssey.II.11") compared to
                # ⋅                                ("Odyssey.III" - "Odyssey.III")
                # ⋅ o  (#4) outside_after    as in ("Odyssey.IV.10" - "Odyssey.IV.11") compared to
                # ⋅                                ("Odyssey.III" - "Odyssey.III")
                # ⋅ o  (#5) outside_overlap  as in ("Odyssey.III.10" - "Odyssey.IV.11") compared to
                # ⋅                                ("Odyssey.III" - "Odyssey.III")
                res_op = self._cmp_biref_vs_biref(biref2, biref)

                if res_op == 0:
                    # nothing to do, can't compare <biref> and <biref2>:
                    pass
                elif res_op == 4:
                    # a special case.
                    #
                    # if res_op == 4, <biref2> is momentarily AFTER biref as in:
                    #   biref= a.33;a.34;t.32-t.33;a.34  and biref2=a.35
                    #              ^
                    #           biref2 is AFTER a.33
                    #
                    # But biref2 is also AFTER a.34, hence the idea to go on.
                    #
                    # At the end of the loop,
                    # * either we'll found a biref that is AFTER biref2, as in:
                    #   biref= a.33;a.34;t.32-t.33  and biref2=a.40
                    #                    ^
                    #               biref2 is BEFORE t.32: the <action> changes (=insert before)
                    #
                    # * either we'll arrive at the end of the loop, as in:
                    #   biref= a.33;a.34;a.35;a.36  and biref2=a.40
                    #                             ^
                    #    end of the loop, biref2 is AFTER t.36: the <action> remains #4
                    action = (res_op, index, biref, biref2)
                else:
                    # an action has been found:
                    action = (res_op, index, biref, biref2)
                    break

            # ---- so, let's act according to <action> ------------------------
            index = action[1]
            biref = action[2]
            biref2 = action[3]
            if action[0] == 0:
                # can't compare

                self.definition.append(biref2)
            elif action[0] == 1:
                # equality
                pass
            elif action[0] == 2:
                # let's insert biref2 inside self.definition[index].

                # 4 steps are required:
                #
                # (0/3) remove self.definition[index]
                # (1/3) insert at <index> [minimal value, predecessor of biref2[0]]
                # (2/3) insert at <index+1> [biref[0], biref2[1]]
                # (3/3) insert at <index+2> [successor of biref2[1], maximal value]

                # ---- (0/3) remove self.definition[index] ----------------
                self.definition.pop(index)

                # ---- (1/3) insert at <index> [minimal value, predecessor of biref2[0]]
                if self._cmp_monoref_vs_monoref(biref2[0], biref[0]) == 4:
                    # biref2[0] inside biref[0]
                    self.definition.insert(
                        index,
                        [self._monoref_set_rightest_item_to_its_lowest_value(biref2[0]),
                         self._monoref_getpredecessor(biref2[0])])
                else:
                    self.definition.insert(
                        index,
                        [biref[0],
                         self._monoref_getpredecessor(biref2[0])])

                # ---- (2/3) insert at <index+1> [biref[0], biref2[1]]
                self.definition.insert(
                    index+1,
                    [biref2[0],
                     biref2[1]])

                # ---- (3/3) insert at <index+2> [successor of biref2[1], maximal value]
                if biref2[1] is None and biref[1] is None:
                    self.definition.insert(
                        index+2,
                        [self._monoref_getsuccessor(biref2[0]),
                         self._monoref_set_rightest_item_to_its_highest_value(biref2[0])])
                elif biref2[1] is None and biref[1] is not None:
                    self.definition.insert(
                        index+2,
                        [self._monoref_getsuccessor(biref2[0]),
                         biref[1]])
                elif biref2[1] is not None and biref[1] is None:
                    self.definition.insert(
                        index+2,
                        [self._monoref_getsuccessor(biref2[1]),
                         self._monoref_set_rightest_item_to_its_highest_value(biref2[0])])
                else:
                    # here, biref2[1] is not None and biref[1] is not None.
                    self.definition.insert(
                        index+2,
                        [self._monoref_getsuccessor(biref2[1]),
                         biref[1]])
            elif action[0] == 3:
                # let's insert biref2 before self.definition[index]:
                self.definition.insert(index, biref2)
            elif action[0] == 4:
                # let's insert biref2 after self.definition[index]:
                self.definition.insert(index+1, biref2)
            else:
                # action[0] = 5
                #
                # biref    |=============|     i.e. | biref[0] ===== biref[1] |
                #
                # biref2 |-------------------| here, biref2[0] is BEFORE biref[0]
                # biref2         |-----------| here, biref2[0] is INSIDE biref[0]
                #
                if self._cmp_monoref_vs_monoref(biref2[0], biref[0]) == 3:
                    # biref2[0] is BEFORE biref[0]:
                    self.definition.pop(index)
                    if biref[1]:
                        self.definition.insert(index, (biref2[0], biref[0]))
                        self.definition.insert(index+1, (biref[0], biref[1]))
                        self.definition.insert(index+2, (biref[1], biref2[1]))
                    else:
                        self.definition.insert(index, (biref2[0], biref[0]))
                        self.definition.insert(index+1, (biref[0], None))
                        self.definition.insert(index+2, (biref[0], biref2[1]))

                else:
                    # biref2[0] is INSIDE biref[0]:
                    self.definition.pop(index)
                    if biref[1]:
                        self.definition.insert(index, (biref[0], biref2[1]))
                        self.definition.insert(index+1, (biref2[1], biref[1]))
                        self.definition.insert(index+2, (biref[1], biref2[1]))
                    else:
                        self.definition.insert(
                            index,
                            (biref[0],
                             biref2[0]))
                        self.definition.insert(
                            index+1,
                            (self._monoref_getsuccessor(biref2[0]),
                             self._monoref_set_rightest_item_to_its_highest_value(biref2[0])))
                        self.definition.insert(
                            index+2,
                            (self._monoref_getsuccessor(
                                self._monoref_set_rightest_item_to_its_highest_value(biref2[0])),
                             biref2[1]))

        # ==== let's reduce the .definition we got ============================
        # _get_reduced_definition() ends with a call to ._multiref_as_tuples()
        self.definition = self._get_reduced_definition(self.definition,
                                                       keep_iter_infos=keep_iter_infos)

        # ==== is this new .definition a valid one ? ==========================
        self.is_valid = self.valid_definition()

        if not self.is_valid:
            # (pimydoc)error::TEXTREF-ERRORID001
            # ⋅ An error occured while creating a TextRef* object : the object isn't valid.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID001"
            error.msg = "The TextRef* object has been checked and is invalid : " \
                f"Returned explanation is '{self.valid_definition(explicit=True)}'."
            self.errors.append(error)

        # ==== normal returned value: everything's alright ====================
        return True

    def add_and_sort_from_str(self,
                              source_string,
                              strings_must_be_sorted=True,
                              keep_iter_infos=True):
        """
            TextRefBaseClass.add_and_sort_from_str()

            Wrapper around type(self)().init_from_str(source_string).add_and_sort()

            Add init_from_str(source_string) to <self> and make sure that the textrefs in
            self.definition are sorted.
            ___________________________________________________________________

            ARGUMENTS:
            o  source_string: (str) source_string given to .init_from_str()
            o  strings_must_be_sorted: (bool) parameter given to .init_from_str()
            o  keep_iter_infos: (bool) parameter given to .init_from_str() AND TO
                                       add_and_sort()

            RETURNED VALUE: (bool)True if no problem occured.
        """
        textref2 = type(self)()
        textref2.init_from_str(source_string=source_string,
                               strings_must_be_sorted=strings_must_be_sorted,
                               keep_iter_infos=keep_iter_infos)

        if textref2.errors:
            return False

        return self.add_and_sort(textref2=textref2,
                                 keep_iter_infos=keep_iter_infos)

    # This method will be over-written and an access to self.definition will be
    # mandatory.
    # pylint: disable=no-self-use
    def customized_valid_definition(self,
                                    explicit):
        """
            TextRefBaseClass.customized_valid_definition()

            Method called by .valid_definition() : write here special checks specific to your class.

            See an example for the TextRefOEVerses class.
            ___________________________________________________________________

            ARGUMENT:
            o  explicit:               (bool)if True, return a string expliciting
                                       the validation

            RETURNED VALUE: if <explicit>:     (bool) True if self.definition is valid.
                            if not <explicit>: (str)A string expliciting the validation.
        """
        return True if not explicit else "is_valid"

    def definition2str(self,
                       reduced=False,
                       keep_iter_infos=True):
        """
            TextRefBaseClass.definition2str()

            Transform .definition into a string that could be read by .init_from_str().
            ___________________________________________________________________

            ARGUMENTS:
            o  reduced:         (bool)if True, apply a special transformation through
                                ._get_reduced_definition()
            o  keep_iter_infos: (bool)parameter only used when calling
                                ._get_reduced_definition(), if <reduced> is True

            RETURNED VALUE: (str)the string representing self.definition .
        """
        definition = self.definition
        if reduced:
            definition = self._get_reduced_definition(definition,
                                                      keep_iter_infos)

        res = []
        for biref in self.definition:
            monoref1, monoref2 = biref

            str_monoref1 = self._monoref_definition2str(monoref1)

            if monoref2:
                str_monoref2 = self._monoref_definition2str(monoref2)
                res.append(f"{str_monoref1}{self._ref2ref_separator}{str_monoref2}")
            else:
                res.append(f"{str_monoref1}")

        return self._refs_separator.join(res)

    def init_from_str(self,
                      source_string: str,
                      strings_must_be_sorted=False,
                      keep_iter_infos=True):
        """
            TextRefBaseClass.init_from_str()

            Initialize .definition from <source_string> and then .is_valid

            (pimydoc)valid definition
            ⋅ * empty .definition is forbidden (no "") (VALIDDEFINITION001)
            ⋅ * for each biref[0], biref[1] in .definition:
            ⋅     * biref[0] can't be empty (no "-mybook.3") (VALIDDEFINITION002a,
            ⋅                                                 VALIDDEFINITION002b)
            ⋅     * biref[0] and biref[1] can't be equal (no "mybook.3-mybook.3")
            ⋅       (VALIDDEFINITION003)
            ⋅     * biref[0] and biref[1] must have the same structure (VALIDDEFINITION004)
            ⋅         - "a_string.3.another_string.4-a_string.5.another_string.6" is OK
            ⋅         - "a_string.3.another_string.4-5.another_string.6" is not OK
            ⋅     * biref[0] and biref[1] must have the same strings (VALIDDEFINITION005)
            ⋅         - "title.1-title.2 is OK
            ⋅         - "another_title.1-title.2 is not OK
            ⋅     * as long as items are equal the values must be equal or increasing
            ⋅       (VALIDDEFINITION006)
            ⋅         - "title.3-title.4" is OK
            ⋅         - "title.33.h-title.36.b" is OK
            ⋅         - "title.4-title.3" is not OK
            ⋅         - "title.33.h-title.33.b" is not OK
            ⋅ * if strings_must_be_sorted is True,
            ⋅   for each string in the different biref: the strings must be sorted
            ⋅   (VALIDDEFINITION007)
            ⋅   - "another_title;title.3-title.4" is OK
            ⋅   - "title.3-title.4;another_title" is not OK
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)source_string
               (pimydoc)init string
               ⋅
               ⋅     o  [OK]        "title.3b"
               ⋅     o  [OK]        "title.4b"
               ⋅                 == "title.4.b"
               ⋅     o  [OK]        "title.33a-"
               ⋅                 == "title.33a"
               ⋅                 == "title.33a-a"
               ⋅                 == "title.33a-title.33a"
               ⋅     o  [OK]        "title.3a-4b"
               ⋅                 == "title.3a-title.4b"
               ⋅
               ⋅     o  [NOT OK] ""
               ⋅     o  [NOT OK] "-title.4"
               ⋅     o  [NOT OK] "title.5-title.4"
            o  (bool)strings_must_be_sorted, arg passed to .valid_definition()

            RETURNED VALUE: self
        """
        self.errors.clear()

        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be made of tuples without
        # ⋅ any list.
        # ⋅
        # ⋅ o  source string:  "title.3-title.4"
        # ⋅    .definition:    (
        # ⋅                     ((None, 'title'), ('int', 3)),
        # ⋅                     ((None, 'title'), ('int', 4))
        # ⋅                    )
        # ⋅
        # ⋅ o  source string:  "title.3-title.4;title.15-title.16"
        # ⋅    .definition:    (
        # ⋅                     (
        # ⋅                      ((None, 'title'), ('int', 3)),
        # ⋅                      ((None, 'title'), ('int', 4))
        # ⋅                     ),
        # ⋅                     (
        # ⋅                      (((None, 'title'), ('int', 15)),
        # ⋅                      ((None, 'title'), ('int', 16))),
        # ⋅                     )
        # ⋅                    )
        # ⋅
        # ⋅ Special syntax for monoref stored as a biref:
        # ⋅
        # ⋅ o  source string:  "title.3-"
        # ⋅    .definition:    (((None, 'title'), ('int', 3)), None)
        # ⋅                                                      ^
        # ⋅                                         special syntax here: we do not repeat
        # ⋅                                             ((None, 'title'), ('int', 3))
        self.definition = []

        # "A.III.6-A.III.8; A.IV.5" > ("A.III.6-A.III.8", "A.IV.5")
        for _ref_str in source_string.split(self._refs_separator):
            ref_str = ref_str = _ref_str.strip()

            if ref_str:
                self._init_from_str__add_mono_or_biref(ref_str)

        self.definition = __class__._multiref_as_tuples(self.definition)

        self.definition = self._get_reduced_definition(self.definition,
                                                       keep_iter_infos=keep_iter_infos)

        # (pimydoc)valid definition
        # ⋅ * empty .definition is forbidden (no "") (VALIDDEFINITION001)
        # ⋅ * for each biref[0], biref[1] in .definition:
        # ⋅     * biref[0] can't be empty (no "-mybook.3") (VALIDDEFINITION002a,
        # ⋅                                                 VALIDDEFINITION002b)
        # ⋅     * biref[0] and biref[1] can't be equal (no "mybook.3-mybook.3")
        # ⋅       (VALIDDEFINITION003)
        # ⋅     * biref[0] and biref[1] must have the same structure (VALIDDEFINITION004)
        # ⋅         - "a_string.3.another_string.4-a_string.5.another_string.6" is OK
        # ⋅         - "a_string.3.another_string.4-5.another_string.6" is not OK
        # ⋅     * biref[0] and biref[1] must have the same strings (VALIDDEFINITION005)
        # ⋅         - "title.1-title.2 is OK
        # ⋅         - "another_title.1-title.2 is not OK
        # ⋅     * as long as items are equal the values must be equal or increasing
        # ⋅       (VALIDDEFINITION006)
        # ⋅         - "title.3-title.4" is OK
        # ⋅         - "title.33.h-title.36.b" is OK
        # ⋅         - "title.4-title.3" is not OK
        # ⋅         - "title.33.h-title.33.b" is not OK
        # ⋅ * if strings_must_be_sorted is True,
        # ⋅   for each string in the different biref: the strings must be sorted
        # ⋅   (VALIDDEFINITION007)
        # ⋅   - "another_title;title.3-title.4" is OK
        # ⋅   - "title.3-title.4;another_title" is not OK
        self.is_valid = self.valid_definition(strings_must_be_sorted)

        if not self.is_valid:
            # (pimydoc)error::TEXTREF-ERRORID001
            # ⋅ An error occured while creating a TextRef* object : the object isn't valid.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID001"
            error.msg = "The TextRef* object has been checked and is invalid : " \
                f"Returned explanation is '{self.valid_definition(explicit=True)}'."
            self.errors.append(error)

        return self

    def is_empty(self):
        """
            TextRefBaseClass.is_empty()

            Return True if self.definition is empty.
        """
        return len(self.definition) == 0

    def is_equal(self,
                 textref2):
        """
            TextRefBaseClass.is_equal()

            Return True if self.definition is equal to textref2.

                Please notice that THE RESULTS MAY DIFFER WITH THOSE RETURNED BY
            self.__eq__().
                __eq__() is the fastest way to compare two definitions but this
            method will fail if tuples and lists are mixed - which should never
            be the case except in intermediate results.
                On the contrary .is_equal() is indifferent to such a mix.
            ___________________________________________________________________

            ARGUMENT:
            o  textref2: a TextRef* object to be compared with <self>.

            RETURNED VALUE: (bool) True if self.definition is equal to textref2
        """
        # (pimydoc)_cmp_multiref_vs_multiref:returned value
        # ⋅ An integer is returned by TextRefBaseClass._cmp_multiref_vs_multiref():
        # ⋅
        # ⋅ o  (#0) undefined        as in ("Odyssey.III.11" - "Odyssey.III.11"); compared to
        # ⋅                                ("Old Testament.III.11" - "Odyssey.III.11")
        # ⋅ o  (#1) equal            as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
        # ⋅                                ("Odyssey.III.11" - "Odyssey.III.11")
        # ⋅ o  (#2) inside           as in ("Odyssey.III.10" - "Odyssey.III.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        # ⋅ o  (#3) outside_before   as in ("Odyssey.II.10" - "Odyssey.II.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        # ⋅ o  (#4) outside_after    as in ("Odyssey.IV.10" - "Odyssey.IV.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        # ⋅ o  (#5) outside_overlap  as in ("Odyssey.III.10" - "Odyssey.IV.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        return self._cmp_multiref_vs_multiref(self.definition,
                                              textref2.definition) == 1

    def is_inside(self,
                  textref2):
        """
            TextRefBaseClass.is_inside()

            Return True if self.definition is inside textref2.
            ___________________________________________________________________

            ARGUMENT:
            o  textref2: a TextRef* object to be compared with <self>.

            RETURNED VALUE: (bool) True if self.definition is inside textref2
        """
        # (pimydoc)_cmp_multiref_vs_multiref:returned value
        # ⋅ An integer is returned by TextRefBaseClass._cmp_multiref_vs_multiref():
        # ⋅
        # ⋅ o  (#0) undefined        as in ("Odyssey.III.11" - "Odyssey.III.11"); compared to
        # ⋅                                ("Old Testament.III.11" - "Odyssey.III.11")
        # ⋅ o  (#1) equal            as in ("Odyssey.III.11" - "Odyssey.III.11") compared to
        # ⋅                                ("Odyssey.III.11" - "Odyssey.III.11")
        # ⋅ o  (#2) inside           as in ("Odyssey.III.10" - "Odyssey.III.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        # ⋅ o  (#3) outside_before   as in ("Odyssey.II.10" - "Odyssey.II.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        # ⋅ o  (#4) outside_after    as in ("Odyssey.IV.10" - "Odyssey.IV.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        # ⋅ o  (#5) outside_overlap  as in ("Odyssey.III.10" - "Odyssey.IV.11") compared to
        # ⋅                                ("Odyssey.III" - "Odyssey.III")
        return self._cmp_multiref_vs_multiref(self.definition,
                                              textref2.definition) == 2

    def valid_definition(self,
                         strings_must_be_sorted=False,
                         explicit=False):
        """
            TextRefBaseClass.valid_definition()

            Check if <self.definition> is a valid definition.

            You may complete these checks by rewriting .customized_valid_definition() .

            (pimydoc)valid definition
            ⋅ * empty .definition is forbidden (no "") (VALIDDEFINITION001)
            ⋅ * for each biref[0], biref[1] in .definition:
            ⋅     * biref[0] can't be empty (no "-mybook.3") (VALIDDEFINITION002a,
            ⋅                                                 VALIDDEFINITION002b)
            ⋅     * biref[0] and biref[1] can't be equal (no "mybook.3-mybook.3")
            ⋅       (VALIDDEFINITION003)
            ⋅     * biref[0] and biref[1] must have the same structure (VALIDDEFINITION004)
            ⋅         - "a_string.3.another_string.4-a_string.5.another_string.6" is OK
            ⋅         - "a_string.3.another_string.4-5.another_string.6" is not OK
            ⋅     * biref[0] and biref[1] must have the same strings (VALIDDEFINITION005)
            ⋅         - "title.1-title.2 is OK
            ⋅         - "another_title.1-title.2 is not OK
            ⋅     * as long as items are equal the values must be equal or increasing
            ⋅       (VALIDDEFINITION006)
            ⋅         - "title.3-title.4" is OK
            ⋅         - "title.33.h-title.36.b" is OK
            ⋅         - "title.4-title.3" is not OK
            ⋅         - "title.33.h-title.33.b" is not OK
            ⋅ * if strings_must_be_sorted is True,
            ⋅   for each string in the different biref: the strings must be sorted
            ⋅   (VALIDDEFINITION007)
            ⋅   - "another_title;title.3-title.4" is OK
            ⋅   - "title.3-title.4;another_title" is not OK

            ___________________________________________________________________

            ARGUMENTS:
            o  strings_must_be_sorted: (bool)if True, a special check verifies that
                                       strings are sorted in <self>:
                                        "another_title;title" is ok
                                        "title;another_title" is not ok

            o  explicit:               (bool)if True, return a string expliciting
                                       the validation

            RETURNED VALUE: if <explicit>:     (bool) True if self.definition is valid.
                            if not <explicit>: (str)A string expliciting the validation.
        """
        # I want the quickest method : as soon as a returned value has been found,
        # it is returned. I don't want to split this long method into several parts
        # for the same reason.
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-branches
        if not self.definition:
            # (VALIDDEFINITION001)
            return False if not explicit else "VALIDDEFINITION001/empty definition. " \
                f"This problem occured in {self.definition} (~ '{self.definition2str()}')."

        for biref in self.definition:
            if biref[0] is None:
                # (VALIDDEFINITION002)
                return False if not explicit else "VALIDDEFINITION002/biref[0] is None " \
                    "as in '-Beo.99' instead of 'Beo.98-Beo.99'. " \
                    f"This problem occured in {self.definition} (~ '{self.definition2str()}')."

            if biref[0] == () or biref[0] == []:
                # (VALIDDEFINITION002b)
                return False if not explicit else "VALIDDEFINITION002b/biref[0] is () " \
                    "as in '-Beo.99' instead of 'Beo.98-Beo.99'. " \
                    f"This problem occured in {self.definition} (~ '{self.definition2str()}')."

            if biref[0] == biref[1]:
                # (VALIDDEFINITION003)
                return False if not explicit else "VALIDDEFINITION003/biref[0]==biref[1]" \
                    "as in 'Beo.99-Beo.99' instead of 'Beo.98-Beo.99'. " \
                    f"This problem occured in {self.definition} (~ '{self.definition2str()}')."

            if biref[1] is not None:
                len_biref0 = len(biref[0])
                len_biref1 = len(biref[1])

                index = 0
                stop = False

                # (bool)partial_equality
                #
                #   True if biref[1] is None
                #        or if biref[0][index] == biref[1][index] for index in [0, ...]
                #
                #   Please notice that <partial_equality> is computed at the end of the loop:
                #   <partial_equality> is thus valid on biref[0|1][index-1] while the beginning
                #   of the loop deals with biref[0|1][index]
                partial_equality = True
                while not stop:

                    if index >= len_biref0:
                        stop = True
                        continue
                    if index >= len_biref1:
                        stop = True
                        continue

                    # (VALIDDEFINITION004)
                    if biref[1] and \
                       biref[0][index][0] != biref[1][index][0]:
                        return False if not explicit else \
                            "VALIDDEFINITION004/biref[0|1] " \
                            "haven't the same typevalue " \
                            "as in 'title.3-99.7' instead of 'title.3-title.7'. " \
                            f"This problem occured in {self.definition} " \
                            f"(~ '{self.definition2str()}') " \
                            f"for the biref {biref} ."

                    # (VALIDDEFINITION005)
                    if biref[1] and \
                       biref[0][index][0] is None and \
                       biref[0][index][1] != biref[1][index][1]:
                        return False if not explicit else \
                            "VALIDDEFINITION005/biref[0|1] " \
                            "aren't the same string " \
                            "as in 'title.3-another_title.7' instead of 'title.3-title.7'. " \
                            f"This problem occured in {self.definition} " \
                            f"(~ '{self.definition2str()}') " \
                            f"for the biref {biref} ."

                    # (VALIDDEFINITION006)
                    if biref[1] and \
                       partial_equality and \
                       biref[0][index][0] is not None and \
                       biref[0][index][1] > biref[1][index][1]:
                        return False if not explicit else \
                            "VALIDDEFINITION006/biref[0] > biref[1] " \
                            "as in 'title.3-title.2' instead of 'title.2-title.3'. " \
                            f"This problem occured in {self.definition} " \
                            f"(~ '{self.definition2str()}') " \
                            f"for the biref {biref} ."

                    if biref[1] and \
                       biref[0][index] != biref[1][index]:
                        partial_equality = False

                    index += 1

        # (VALIDDEFINITION007)
        if strings_must_be_sorted:
            depth = 0
            stop = False
            while not stop:
                last_read_string = None
                for biref in self.definition:

                    if depth < len(biref[0]):
                        if biref[0][depth][0] is None:
                            if last_read_string is not None:
                                if self._cmp_strs(last_read_string, biref[0][depth][1]) == +1:
                                    return False if not explicit else \
                                        "VALIDDEFINITION007/strings aren't sorted " \
                                        "as in 'titl.3;a_titl.2' instead of 'a_titl.2-titl.3'. " \
                                        f"This problem occured in {self.definition} " \
                                        f"(~ '{self.definition2str()}') " \
                                        f"for the biref {biref} ."
                            last_read_string = biref[0][depth][1]
                        else:
                            break

                    if biref[1] and depth < len(biref[1]):
                        if biref[1][depth][0] is None:
                            if last_read_string is not None and \
                               self._cmp_strs(last_read_string, biref[1][depth][1]) == +1:
                                return False if not explicit else \
                                    "VALIDDEFINITION007/strings aren't sorted " \
                                    "as in 'titl.3;a_titl.2' instead of 'a_titl.2-titl.3'. " \
                                    f"This problem occured in {self.definition} " \
                                    f"(~ '{self.definition2str()}') " \
                                    f"for the biref {biref} ."
                            last_read_string = biref[1][depth][1]
                        else:
                            break

                if last_read_string is None:
                    stop = True  # nothing has been read: reached max. depth.
                else:
                    depth += 1

        return self.customized_valid_definition(explicit)
