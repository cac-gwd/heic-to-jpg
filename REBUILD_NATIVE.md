# Native library sources and replacement

The Windows release uses the unmodified Windows x64 pi-heif 1.4.0 wheel.
At runtime it reports libheif 1.23.0 and libde265 1.1.1. No x265 library is
included. The original pi-heif bundled-license notice links to older sources;
the source archives attached to this release match the reported runtime versions.

## Source archive contents

- application/: this application's source and Windows ZIP build script.
- pi_heif-1.4.0.tar.gz: the Python binding, C extension, setup.py, and native
  build recipes. See libheif/windows/mingw-w64-libheif/PKGBUILD inside it.
- libheif-1.23.0.tar.gz and libde265-1.1.1.tar.gz: native library sources,
  CMake/Autotools configuration, public headers, and license texts.
- manifest.json: upstream download URLs and SHA-256 hashes.

The source archives are unchanged. The pi-heif wheel itself was not rebuilt
for this release. The application's build was tested; the native rebuild
instructions below are for developers and were not used to build this wheel.

## Build configuration

Use a Windows x64 MSYS2/MinGW64 C/C++ toolchain with CMake and Ninja.
Build and install libde265 1.1.1 as a shared library to a writable prefix using
its supplied CMake build (BUILD_SHARED_LIBS=ON). Build libheif 1.23.0 against
that prefix using the pi-heif source distribution's Windows PKGBUILD as the
configuration reference. It enables shared libraries and libde265, and disables
x265, AOM, other optional codecs, plugin loading, examples, and tests. Use the
provided 1.23.0 source archive. The libde265 source archive supplied here is
1.1.1, matching the distributed DLL; any older libde265 URL in the upstream
build scripts should be replaced with this archive.

To rebuild the Python binding, use the same Python ABI (CPython 3.12 x64 for
this release), install a matching compiler, point MSYS2_PREFIX/LIBHEIF_ROOT
at the prefix containing the rebuilt library and headers, and build a wheel
from the supplied pi-heif source. setup.py contains the supported Windows
compiler/linking configuration. The upstream README and native build recipes
are included in the source distribution.

## Use modified libraries

The Windows ZIP uses PyInstaller folder mode. Native libraries and the Python
extension remain separate files in HEIC-to-JPG/_internal. They are not encrypted
or protected by signature checks. Close the app before replacing them.

The shipped pi-heif wheel uses these DLL basenames:

- libheif-75127e764628a95f6db9f5070bfc87cb.dll
- libde265-0-aa0625e0aec56a9d4310a2447674dd8a.dll

An ABI-compatible rebuilt library may be installed under the same imported
basename, together with its own dependencies. A rebuilt DLL may instead import
the original, unhashed dependency names: include those additional dependencies
under their imported names in the same directory. If the ABI changes, rebuild
and replace the _pi_heif CPython extension as well, or run the included Python
application source with a Python environment containing the modified binding.
There is no requirement to preserve the wheel's original file hashes.

To rebuild the app's full Windows ZIP from the modified environment, install
the application build dependencies and run scripts/build_release.py. The
PyInstaller build command, package license collection, and ZIP creation are
all in that script. For redistributions, provide the source and build information
for the specific modified versions that you ship.
