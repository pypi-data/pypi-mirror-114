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
   MusaMusa-TextRef project : musamusa_textref/semisortedtextrefsdict.py

   Use SemiSortedTextRefsDict to store (textref, data) where textref is
   a TextRef* like object.

   "semi sorted" means that the internal storage (.textref2data) isn't sorted
   but that you may iterate over a SemiSortedTextRefsDict and get sorted output
   thanks to the .sorted_textrefs attribute.
   ____________________________________________________________________________

   o  SemiSortedTextRefsDict class
"""
from iaswn.iaswn import Iaswn
from musamusa_errors.error_messages import ListOfErrorMessages, MusaMusaError
from musamusa_textref.textrefdefault import TextRefDefault


class SemiSortedTextRefsDict(Iaswn):
    """
        SemiSortedTextRefsDict class

        ATTRIBUTES:
        o  (ListOfErrorMessages) .errors
        o  (dict: textref>data)  .textref2data
        o  (TextRef* object)     .sorted_textrefs

        METHODS:
        o  __eq__(self, other)
        o  __init__(self, textrefclass=TextRefDefault)
        o  __iter__(self)
        o  __repr__(self)
        o  add(self, textref, data)
        o  improved_str(self)
        o  is_empty(self)
    """
    def __eq__(self,
               other):
        """
            SemiSortedTextRefsDict.__eq__()
            ___________________________________________________________________

            ARGUMENT: <other>, a SemiSortedTextRefsDict object.

            RETURNED VALUE: True if <self> and <other> are equal, False otherwise.
        """
        return self.errors == other.errors and \
            self.textref2data == other.textref2data and \
            self.sorted_textrefs == other.sorted_textrefs

    def __init__(self,
                 textrefclass=TextRefDefault):
        """
            SemiSortedTextRefsDict.__init__()
            ___________________________________________________________________

            ARGUMENT:
            o  (type)textrefclass: TextRef* type to be used.
        """
        self.errors = ListOfErrorMessages()
        self.textref2data = dict()
        self.sorted_textrefs = textrefclass(force_validity=True)

    def __iter__(self):
        """
            SemiSortedTextRefsDict.__iter__()
            ___________________________________________________________________

            This method yields TextRef* objects stored self.sorted_textrefs
        """
        for obj in self.sorted_textrefs:
            yield obj

    def __repr__(self):
        """
            SemiSortedTextRefsDict.__repr__()
        """
        return f"{self.errors=}; {self.textref2data=}; {str(self.sorted_textrefs)=}"

    def add(self,
            textref,
            data):
        """
            SemiSortedTextRefsDict.add()

            Add a pair of (textref: data) to self.

            NO ERROR IS ADDED to .errors if textref is already (partially or not)
            in <self>.
            ___________________________________________________________________

            ARGUMENTS:
            o  (TextRef*) textref used as a key.
            o  (any type) data used as a value.

            RETURNED VALUE: (bool)success
        """
        if not hasattr(textref, "errors"):
            # (pimydoc)error::TEXTREF-ERRORID005
            # ⋅ SemiSortedTextRefsDict.add() got an argument for the <textref> argument
            # ⋅ but this object doesn't seem to be a TextRef* like object.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID005"
            error.msg = "SemiSortedTextRefsDict.add() got an argument for <textref> " \
                "but this object doesn't seem to be a TextRef* like object. " \
                f"textref='{textref}' (type={type(textref)})  ."
            self.errors.append(error)
            return False

        if not self.errors.zero_error_or_warning():
            # (pimydoc)error::TEXTREF-ERRORID002
            # ⋅ You can't use SemiSortedTextRefsDict.add() with SemiSortedTextRefsDict object
            # ⋅ that already contains an error.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID002"
            error.msg = "You can't add anything to a SemiSortedTextRefsDict that already " \
                "contains an error."
            self.errors.append(error)
            return False

        if not textref.errors.zero_error_or_warning():
            # (pimydoc)error::TEXTREF-ERRORID003
            # ⋅ You can't add a TextRef* object to a SemiSortedTextRefsDict
            # ⋅ if the TextRef* already contains an error.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID003"
            error.msg = "You can't add a TextRef* object to a SemiSortedTextRefsDict " \
                "if the TextRef* contains an error."
            error.suberrors = textref.errors
            self.errors.append(error)
            return False

        if not self.sorted_textrefs.add_and_sort(textref2=textref,
                                                 keep_iter_infos=True):
            return False

        self.textref2data[textref] = data

        return True

    def improved_str(self):
        """
            SemiSortedTextRefsDict.improved_str()
            ___________________________________________________________________

            RETURNED VALUE: (str) a string describing the object.
        """
        res = []

        if self.errors:
            res.append("ERROR/WARNINGS:")
            for error in self.errors:
                res.append("* "+str(error.improved_str()))

        if self.sorted_textrefs.is_empty():
            res.append("No textref.")
        else:
            res.append(
                f"textrefs="
                "{self.sorted_textrefs.definition2str()} "
                "(reduced="
                f"{self.sorted_textrefs.definition2str(reduced=True, keep_iter_infos=False)})")

            for textref in self.sorted_textrefs:
                res.append(f"*  {textref.definition2str()} : {self.textref2data[textref]}")

        return "\n".join(res)

    def is_empty(self):
        """
            SemiSortedTextRefsDict.is_empty()
            ___________________________________________________________________

            RETURNED VALUE: (bool) True if no TextRef stored in self.textref2data
        """
        return len(self.textref2data) == 0
