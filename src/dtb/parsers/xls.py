#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from os import devnull

# External compatibility dependencies

from builtins import range

# External dependencies

import xlrd

# Package dependencies

from ..formats.xls import XlsFormat
from .base import Parser

# Classes


class XlsParser(Parser):
    '''XLS parser class.'''

    # Parser format
    _format = XlsFormat

    def __init__(self, base, logger):
        '''Constructor.

        :param base: a territorial base instance to parse
        :param logger: a logger instance to log
        '''
        super(self.__class__, self).__init__(base, logger)

        self._book = xlrd.open_workbook(file_contents=self._base.rawdata,
                                        encoding_override='utf-8',
                                        logfile=open(devnull, 'w'),
                                        on_demand=True)
        self._sheet = self._book.sheet_by_name(self._base.sheet)

    def parseColumns(self):
        '''Parses the XLS database columns.'''
        self._logger.debug('Parsing database cols...')

        return self._data._cols[:self._sheet.ncols]

    def parseRows(self):
        '''Parses the XLS database rows.'''
        self._logger.debug('Parsing database rows...')

        rows = []

        for row_id in range(self._sheet.nrows):
            # Skip headers
            if row_id == 0:
                continue

            row_data = [unicode(col) for col in self._sheet.row_values(row_id)]
            rows.append(self.parseRow(row_data))

        return rows

    def parseRow(self, row_data):
        '''Parses the database row.'''
        from ..core.entities import TerritorialDatabaseRow

        row = TerritorialDatabaseRow()
        base = int(self._base.year)

        # 12 cols
        if base in [2003, 2005, 2006, 2007, 2008, 2009, 2013]:
            row.id_uf, row.nome_uf, \
            row.id_mesorregiao, row.nome_mesorregiao, \
            row.id_microrregiao, row.nome_microrregiao, \
            row.id_municipio, row.nome_municipio, \
            row.id_distrito, row.nome_distrito, \
            row.id_subdistrito, row.nome_subdistrito = row_data
        # 8 cols
        elif base in [2010, 2011, 2012]:
            row.id_uf, row.nome_uf, \
            row.id_mesorregiao, row.nome_mesorregiao, \
            row.id_microrregiao, row.nome_microrregiao, \
            row.id_municipio, row.nome_municipio = row_data
        # 15 cols
        elif base == 2014:
            row.id_uf, row.nome_uf, \
            row.id_mesorregiao, row.nome_mesorregiao, \
            row.id_microrregiao, row.nome_microrregiao = row_data[:6]
            row.id_municipio, row.nome_municipio = row_data[7:9]
            row.id_distrito, row.nome_distrito = row_data[10:12]
            row.id_subdistrito, row.nome_subdistrito = row_data[13:15]

        row.normalize()

        return row
