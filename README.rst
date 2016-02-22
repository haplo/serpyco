Serpyco
=======

**Serpyco** is a simple EXIF renamer, it takes a bunch of unorganized
photographs and renames them chronologically according to their EXIF
metadata. This can be useful in several use cases, such as combining
photos from different cameras and still have them properly sorted.

The name comes from "Simple Exif Renamer in Python". The -co suffix is only
there to make it a tribute to Serpico, a character in the Berserk manga series
(one of the best mangas ever written, definitely recommended!).

Serpyco is free software licensed under the GNU GPL v3 or any later
version. See COPYING or http://www.gnu.org/licenses/ for a copy of the
license.

Go to http://github.com/haplo/serpyco for the latest version of the
code or to report any issue you may find.

Usage
-----

Just run the script passing a list of image files::

  python serpyco.py /path/to/file1.jpg /path/to/file2.jpg ...

Usually, you'll want to use wildcards to include several files::

  python serpyco.py /path/to/photos/*.jpg

You can process files in multiple directories in one call. Each file will be
kept in their original directory, but they will be processed and renamed
together, not per-directory::

  python serpyco.py /path/to/photos/*.jpg /path/to/more/photos/*.jpg

There's a bunch of available options:

 * `-d, --date-as-filename`: use dates as filenames instead of a prefix and an
   incremental counter. It can manage multiple photos with the same date. This
   option supersedes `-p`.

 * `-i, --ignore-errors`: rename files even if errors occurred. Files with
   errors will be ignored and not taken into account at all.

 * `-n, --dry-run`: print a simulation of the changes, but do no real change.

 * `-p, --prefix`: use a custom prefix for all new filenames. The default prefix
   is *DSC_*. This option has no effect if `-d` is also active.

All errors are printed to the standard error stream, and the renaming plan is
printed to standard output. To create a text file with the renaming plan
information, use::

  python serpyco.py -n files*.jpg > renaming_plan.txt

Remove the -n switch when you are ready to execute the plan.

Dependencies
------------

 * Python 2.7, 3.3 or 3.4 (it may work in 2.6 and 3.2 or previous
   versions, but it's untested and unsupported)
 * pyexiv2 (*python-pyexiv2* package in Debian/Ubuntu systems)

Acknowledgements
----------------

Test images were borrowed from pyexiv2.
