#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-Fal Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-Fal.
#    MusaMusa-Fal is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-Fal is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-Fal.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    MusaMusa-Fal project : musamusa_fal/musamusa_fal/fal.py

    Use this package to store a filename and a line number.

    ___________________________________________________________________________

    o FileAndLine class
"""
from dataclasses import dataclass

from iaswn.iaswn import Iaswn


@dataclass
class FileAndLine(Iaswn):
    """
        FileAndLine class

        Use this store to store a filename and a line number into this file.

        !!! Beware, lineindex is greater or equal to 1 !!!
        _______________________________________________________________________

        ATTRIBUTES:
        o  filename: (str) path to the read source file
        o  lineinde: (int) the read line (>=1, first read line is line number 1 !)

        METHODS:
        o  __repr__(self)
        o  improved_str(self)
        o  _from_jsondict(json_dict)
        o  _to_jsondict(obj)
    """
    filename: str = ""
    lineindex: int = 1

    def __repr__(self):
        """
            FileAndLine.__repr__()
        """
        res = "{filename}#{lineindex}"
        return res.format(filename=self.filename,
                          lineindex=self.lineindex)

    def improved_str(self):
        """
            FileAndLine.improved_str()

            Give a nice representation of <self> using the `rich` package.
            __________________________________________________________________

            RETURNED VALUE : a (str)representation of <self>.
        """
        return f"[bold]'{self.filename}'[/bold] at [italic]#{self.lineindex}[/italic]"
