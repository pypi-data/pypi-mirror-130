#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.ndjson',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20211208',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'utilities for working with newline delimited JSON (NDJSON) files',
  long_description =
    ('Utilities for working with newline delimited JSON (NDJSON) files.\n'    
 '\n'    
 '*Latest release 20211208*:\n'    
 'Initial PyPI release.\n'    
 '\n'    
 '## Function `append_ndjson(arg, *a, **kw)`\n'    
 '\n'    
 'Append an iterable of objects to a file as newline delimited JSON.\n'    
 '\n'    
 '## Function `scan_ndjson(arg, *a, **kw)`\n'    
 '\n'    
 'Read a newline delimited JSON file, yield instances of `dictclass`\n'    
 '(default `dict`, otherwise a class which can be instantiated\n'    
 'by `dictclass(a_dict)`).\n'    
 '\n'    
 '`error_list` is an optional list to accrue `(lineno,exception)` tuples\n'    
 'for errors encountered during the scan.\n'    
 '\n'    
 '## Class '    
 '`UUIDNDJSONMapping(cs.obj.SingletonMixin,cs.mappings.IndexedSetMixin)`\n'    
 '\n'    
 'A subclass of `IndexedSetMixin` which maintains records\n'    
 'from a newline delimited JSON file.\n'    
 '\n'    
 '### Method `UUIDNDJSONMapping.__init__(self, filename, dictclass=<class '    
 "'cs.mappings.UUIDedDict'>, create=False)`\n"    
 '\n'    
 'Initialise the mapping.\n'    
 '\n'    
 'Parameters:\n'    
 '* `filename`: the file containing the newline delimited JSON data;\n'    
 '  this need not yet exist\n'    
 '* `dictclass`: a optional `dict` subclass to hold each record,\n'    
 '  default `UUIDedDict`\n'    
 '* `create`: if true, ensure the file exists\n'    
 '  by transiently opening it for append if it is missing;\n'    
 '  default `False`\n'    
 '\n'    
 '### Method `UUIDNDJSONMapping.add_backend(self, record)`\n'    
 '\n'    
 'Append `record` to the backing file.\n'    
 '\n'    
 '### Method `UUIDNDJSONMapping.rewrite_backend(self)`\n'    
 '\n'    
 'Rewrite the backing file.\n'    
 '\n'    
 'Because the record updates are normally written in append mode,\n'    
 'a rewrite will be required every so often.\n'    
 '\n'    
 '### Method `UUIDNDJSONMapping.scan(self)`\n'    
 '\n'    
 'Scan the backing file, yield records.\n'    
 '\n'    
 '## Function `write_ndjson(arg, *a, **kw)`\n'    
 '\n'    
 'Transcribe an iterable of objects to a file as newline delimited JSON.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20211208*:\n'    
 'Initial PyPI release.'),
  install_requires = ['cs.deco', 'cs.fileutils>=20211208', 'cs.logutils', 'cs.mappings', 'cs.obj', 'cs.pfx'],
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.ndjson'],
)
