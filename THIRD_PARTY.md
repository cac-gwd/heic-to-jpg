# Third-party software in the Windows release

The application source remains MIT-licensed (see LICENSE). Each bundled
third-party component retains its own license. The binary package is not
licensed solely under MIT.

## Components

| Component | Version | License / included notice |
| --- | --- | --- |
| Python | 3.12.14 | PSF / Python-LICENSE.txt |
| Tcl / Tk | 8.6.12 | Tcl/Tk BSD-style notices |
| Pillow | 11.3.0 | HPND and bundled library notices in licenses/Pillow/LICENSE |
| pi-heif | 1.4.0 | BSD-3-Clause source; LGPLv3 native libraries |
| libheif | 1.23.0 | LGPL-3.0; licenses/libheif-COPYING.txt |
| libde265 | 1.1.1 | LGPL-3.0; licenses/LGPL-3.0.txt |
| MinGW GCC runtimes | wheel-provided builds | GPL with GCC Runtime Library Exception; GCC-COPYING* |
| winpthreads | wheel-provided build | Winpthreads-COPYING.txt |
| PyInstaller bootloader | 6.22.3 | GPL with bootloader exception; PyInstaller-COPYING.txt |

The pi-heif wheel's original LICENSES_bundled.txt is preserved in licenses/pi-heif/.
Its upstream version links are outdated; the libheif and libde265 versions above
were read from the actual library at runtime. The release does not bundle x265.
Pillow's license file also contains notices for its bundled imaging libraries.
Additional notices for Python's native dependencies are in licenses/.

## Corresponding source and build information

[Release v1.0.0](https://github.com/cac-gwd/heic-to-jpg/releases/tag/v1.0.0)
provides HEIC-to-JPG-v1.0.0-sources.zip alongside the Windows binary ZIP.
It contains the application source, the unmodified pi-heif 1.4.0 source
distribution (including its Windows build recipes), the matching libheif
1.23.0 and libde265 1.1.1 source archives, license texts, build instructions,
and hashes of the source archives. Sources can be downloaded at no charge.

Native DLLs from the pi-heif wheel were copied without modification.
The application is packaged with PyInstaller in folder mode, leaving these
libraries as separate files in _internal. Users may modify and replace these
LGPL libraries with interface-compatible versions. No restriction is imposed
on reverse engineering for debugging modifications to those libraries.

The source archive includes REBUILD_NATIVE.md explaining the build configuration
and replacement of the hashed DLL filenames. The application build is scripted
in scripts/build_release.py; bundled source/heic_to_jpg.py can also be run with
a separately installed Python environment and replacement libraries.

For future redistributions, preserve these notices and provide the matching
library sources and build information for the versions you distribute.
