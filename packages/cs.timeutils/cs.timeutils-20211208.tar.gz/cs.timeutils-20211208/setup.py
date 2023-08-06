#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.timeutils',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20211208',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'convenience routines for times and timing',
  long_description =
    ('Convenience routines for timing.\n'    
 '\n'    
 '*Latest release 20211208*:\n'    
 'Move the TimeoutError definiton to cs.gimmicks.\n'    
 '\n'    
 '## Function `ISOtime(gmtime)`\n'    
 '\n'    
 'Produce an ISO8601 timestamp string from a UNIX time.\n'    
 '\n'    
 '## Function `sleep(delay)`\n'    
 '\n'    
 'time.sleep() sometimes sleeps significantly less that requested.\n'    
 'This function calls time.sleep() until at least `delay` seconds have\n'    
 'elapsed, trying to be precise.\n'    
 '\n'    
 '## Function `time_from_ISO(isodate, islocaltime=False)`\n'    
 '\n'    
 'Parse an ISO8601 date string and return seconds since the epoch.\n'    
 'If islocaltime is true convert using localtime(tm) otherwise use\n'    
 'gmtime(tm).\n'    
 '\n'    
 '## Function `time_func(func, *args, **kw)`\n'    
 '\n'    
 'Run the supplied function and arguments.\n'    
 "Return a the elapsed time in seconds and the function's own return value.\n"    
 '\n'    
 '## Function `tm_from_ISO(isodate)`\n'    
 '\n'    
 'Parse an ISO8601 date string and return a struct_time.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20211208*:\n'    
 'Move the TimeoutError definiton to cs.gimmicks.\n'    
 '\n'    
 '*Release 20190220*:\n'    
 'Backport for older Pythons.\n'    
 '\n'    
 '*Release 20190101*:\n'    
 'Define TimeoutError only if missing.\n'    
 '\n'    
 '*Release 20170608*:\n'    
 'Trivial changes, nothing semantic.\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'PyPI initial prep.'),
  install_requires = [],
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.timeutils'],
)
