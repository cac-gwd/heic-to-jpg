# Third-party software

This repository contains the application's own source code and documentation.
It does not vendor Python packages, native libraries, or a compiled executable.
The MIT license in LICENSE applies to the application's source code and documentation.

Dependencies are downloaded separately by pip:

- [Pillow 11.3.0](https://github.com/python-pillow/Pillow/tree/11.3.0):
  see the upstream LICENSE and the notices shipped with its wheel.
- [pillow-heif 1.1.1](https://github.com/bigcat88/pillow_heif/tree/v1.1.1):
  its Python source is BSD-3-Clause. Prebuilt wheels also contain native codecs
  with different licenses. See the wheel's LICENSE.txt and LICENSES_bundled.txt.
- [PyInstaller 6.22.3](https://github.com/pyinstaller/pyinstaller/tree/v6.22.3)
  (build only): see its COPYING.txt and bootloader exception.
- [Python](https://www.python.org/) and its bundled Tcl/Tk:
  see the licenses accompanying the Python installation used for the build.

## Compiled executables

PyInstaller bundles dependencies into the generated executable. In particular,
the pillow-heif 1.1.1 Windows wheel includes libheif, libde265, and x265;
its bundled-license notice describes LGPL/GPL-covered components. That bundled
notice should be checked against the actual versions in the wheel.

An executable built from this project must not be described as containing only
MIT-licensed code. Before redistributing a compiled package, include the applicable
license texts, copyright notices, and corresponding source/build materials for the
specific bundled libraries as required by their licenses.

The source-only publication of this repository does not include a compiled release.
