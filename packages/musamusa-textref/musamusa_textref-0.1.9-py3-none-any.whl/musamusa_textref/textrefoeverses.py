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
   MusaMusa-TextRef project : musamusa_textref/textrefoeverses.py

   Text Reference for Old English Verses: TextRefOEVerses

   Beware ! TextRef* classes don't store the source string you may used to initialize
            such an object. You have to store this source string apart.


   Unit testing: see tests/textrefoeverses.py

   ____________________________________________________________________________

   class:

   o TextRefOEVerses class
"""
# TextRefOEVerses DOES have public methods, inherited from TextRefBaseClass.
# pylint: disable=too-few-public-methods

import re
from musamusa_textref.textrefbaseclass import TextRefBaseClass
from musamusa_textref.subref import SubRef


class TextRefOEVerses(TextRefBaseClass):
    """
        TextRefOEVerses class
        _______________________________________________________________________

        METHODS:
        o  _init_from_str__extract_def_from_src_mono(self, src)
        o  customized_valid_definition(self, explicit)
    """
    _refs_separator = ";"
    _ref2ref_separator = "-"
    _refsubpart_separator = "."

    # we use some tricks here to gently catch errors in strings intializing
    # a TextRefOEVerses object:
    #
    #  o  in order to catch Beo.23.c, we accept [a-z] in "a-z(1)"
    #  o  in order to catch Beo.23c, we accept [a-z] in "int+a-z(1)"
    #  o  the max limit is however 2 (not 26) to allow correct iterations
    _subrefs = {
              "a-z(1)": SubRef(re.compile(r"^[a-z]$"),
                               1,
                               2,
                               {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5,
                                "f": 6, "g": 7, "h": 8, "i": 9, "j": 10,
                                "k": 11, "l": 12, "m": 13, "n": 14, "o": 15,
                                "p": 16, "q": 17, "r": 18, "s": 19, "t": 20,
                                "u": 21, "v": 22, "w": 23, "x": 24, "y": 25,
                                "z": 26}),
              "int": SubRef(re.compile(r"^\d+$"),
                            1, 9999, {}),
              "int+a-z(1)": SubRef(re.compile(r"^(?P<subref0>\d+)(?P<subref1>[a-z])$"),
                                   None, None, {}),
              }

    def _init_from_str__extract_def_from_src_mono(self,
                                                  src):
        """
            TextRefOEVerses._init_from_str__extract_def_from_src_mono()

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

                # ---- a-z(1) -------------------------------------------------
                _subrefs_res = re.search(self._subrefs["a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("a-z(1)",
                         self._subrefs["a-z(1)"].char2int[subpart]))
                    continue

                res.append(
                    (None,
                     subpart))

        return res

    def customized_valid_definition(self,
                                    explicit):
        """
            TextRefOEVerses.customized_valid_definition()

            Additionnal check(s):

            o  customized_check001_monoref: "a-z(1)" integer must be 1 or 2 ('a' or 'b'),
                                            not a greater int. (no 'c', 'd'... 'z')
            ___________________________________________________________________

            ARGUMENT:
            o  explicit:               (bool)if True, return a string expliciting
                                       the validation

            RETURNED VALUE: if <explicit>:     (bool) True if self.definition is valid.
                            if not <explicit>: (str)A string expliciting the validation.
        """
        # ---- customized_check001_monoref ------------------------------------
        # "a-z(1)" integer must be 1 or 2 ('a' or 'b'), not a greater int. (no 'c', 'd'... 'z')
        def customized_check001_monoref(monoref):
            """
                customized_check001_monoref()

                Sub-method of TextRefOEVerses.customized_valid_definition().

                Perform the additionnal check "customized_check001_monoref" (see supra)
                on a <monoref>.
                _______________________________________________________________

                ARGUMENT:
                o  monoref: the monoref to be checked

                RETURNED VALUE: (bool) True if the test is ok
            """
            for index in range(1, len(monoref)):
                if monoref[index][0] == "a-z(1)" and monoref[index][1] > 2:
                    return False
            return True

        alright = True
        for biref in self.definition:
            monoref1, monoref2 = biref

            if not customized_check001_monoref(monoref1):
                alright = False
            if monoref2 and not customized_check001_monoref(monoref2):
                alright = False
            if not alright:
                return False if not explicit else "(customized_valid_definition) " \
                    "You can't use lower case letters representing numbers " \
                    "(like you would use them in 'Beowulf.23b', a random example) " \
                    "if these letters are not 'a' and 'b'. " \
                    f"This problem occured in {self.definition} (~ '{self.definition2str()}') " \
                    f"in the biref {biref}."

        return True if not explicit else "valid"
