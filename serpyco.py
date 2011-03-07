#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Renames photography files chronologically according to date in EXIF metadata.

Requires pyexiv2 (python-pyexiv2 package in Debian/Ubuntu).

Options:

 * `-d, --date-as-filename`: use dates as filenames.
 * `-i, --ignore-errors`: do the renaming even if errors occurred.
 * `-n, --dry-run`: print a simulation of the changes, but do no real change.
 * `-p, --prefix`: use a custom prefix for all new filenames.

Copyright (C) 2011 Fidel Ramos Sañudo <fidelramos@gmail.com>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from datetime import datetime
import math
import operator
import optparse
import os
import pyexiv2
import sys


class ExifError(Exception):
    """Error ocurred when parsing EXIF metadata"""
    pass


def extract_date_from_exif(filepath):
    """Extract image date from the EXIF metadata."""
    metadata = pyexiv2.ImageMetadata(filepath)
    metadata.read()
    try:
        date = metadata['Exif.Image.DateTime'].value
    except KeyError:
        date = None
        raise ExifError('%s: Error reading date from EXIF metadata' % filepath)
    if date is None:
        raise ExifError('%s: Empty date' % filepath)
    if not isinstance(date, datetime):
        raise ExifError('%s: Incorrect date %s' % (filepath, date))
    return date


def generate_rename_plan(files_and_dates, prefix, date_as_filename=False):
    """Generator that creates a rename plan for the given files and dates.

    The new file names will begin with the given prefix, and an incremental
    number left-padded with zeroes (e.g. DSC_001, DSC_002, ..., DSC_999).
    However, if date_as_filename is True, then each photo will be renamed to
    their date, in the format "YYYY-MM-DD HH.MM.SS".

    """
    digits_for_counter = int(math.ceil(math.log10(len(files_and_dates))))
    formatspec = '%%s/%%s%%0%dd%%s' % digits_for_counter
    files_and_dates.sort(key=operator.itemgetter(1))
    previous_date = None
    counter = 0
    for i, filename_and_date in enumerate(files_and_dates):
        filename, date = filename_and_date
        name, ext = os.path.splitext(filename)
        path = os.path.dirname(name) or '.' # empty paths raises errors later
        if date_as_filename:
            date_str = date.strftime('%Y-%M-%d %H.%M.%S')
            if date == previous_date:   # detect photos with the same date up
                counter += 1            # to the second, their new filenames
            else:                       # would clash
                counter = 0
            if counter != 0:
                new_name = '%s/%s-%s%s' % (path, date_str, counter, ext)
            else:
                new_name = '%s/%s%s' % (path, date_str, ext)
            previous_date = date
        else:
            new_name = formatspec % (path, prefix, i, ext)
        yield (filename, new_name)


def rename_files(rename_plan, dry_run=False):
    """Rename files according to the given rename plan.

    The rename plan is a sequence of tuples (current_name, new_name).

    If dry_run is True, no actual renaming will take place, it will only print
    the plan to stdout.

    """
    for original_name, new_name in rename_plan:
        print "%s ---> %s" % (original_name, new_name)
        if not dry_run:
            os.rename(original_name, new_name)


if __name__ == '__main__':
    parser = optparse.OptionParser("Usage: %prog [options] file1 file2...")
    parser.add_option("-d", "--date-as-filename", dest="date_as_filename",
                      default=False, action="store_true",
                      help="Use each photo's date as destination filename")
    parser.add_option("-i", "--ignore-errors", dest="ignore_errors",
                      default=False, action="store_true",
                      help="Rename files even if errors occurred")
    parser.add_option("-n", "--dry-run", dest="dry_run",
                      default=False, action="store_true",
                      help="Simulate and print what changes would be made")
    parser.add_option("-p", "--prefix", dest="prefix",
                      default="DSC_", action="store", type="string",
                      help="Prefix for renamed files (default \"DSC_\")")
    (options, args) = parser.parse_args()
    date_as_filename = options.date_as_filename
    ignore_errors = options.ignore_errors
    dry_run = options.dry_run
    prefix = options.prefix

    error = False
    if len(args) < 1:
        parser.error("incorrect number of arguments")
    files_and_dates = []
    files_iter = iter(args)
    for filepath in files_iter:
        try:
            files_and_dates.append([filepath, extract_date_from_exif(filepath)])
        except ExifError, e:
            sys.stderr.write(str(e))
            sys.stderr.write(os.linesep)
            sys.stderr.write("%s will be ignored" % filepath)
            sys.stderr.write(os.linesep)
            error = True
    rename_plan = generate_rename_plan(files_and_dates, prefix, date_as_filename)
    if dry_run:
        rename_files(rename_plan, dry_run=dry_run or error)
    if error:
        if ignore_errors and not dry_run:
            msg = """
One or more errors have occurred. Problematic files have been ignored,
and the rest have been renamed.%(ls)s"""
        else:
            msg = """
One or more errors have occurred, no change has been made.%(ls)s
If you want to rename the files anyway use the -i option (without -n).%(ls)s"""
        sys.stderr.write(msg % {'ls': os.linesep})
        sys.exit(100)
