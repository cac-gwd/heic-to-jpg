"""Build an offline Windows ZIP. Run with the Python used for the build."""
import argparse
import hashlib
from importlib import metadata
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="1.0.0")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("Build on 64-bit Windows with 64-bit Python and Tcl/Tk installed.")
    if not args.version or any(c not in "0123456789.-abcdefghijklmnopqrstuvwxyz" for c in args.version):
        parser.error("Invalid version")
    subprocess.run([
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--onedir", "--windowed", "--name", "HEIC-to-JPG",
        "--collect-all", "pi_heif", "--exclude-module", "numpy",
        "--distpath", str(ROOT / "dist"), "--workpath", str(ROOT / "build"),
        "--specpath", str(ROOT / "build"), str(ROOT / "heic_to_jpg.py")
    ], check=True, cwd=ROOT)
    bundle = ROOT / "dist" / "HEIC-to-JPG"
    for name in ("LICENSE", "THIRD_PARTY.md", "START_HERE.txt"):
        shutil.copy2(ROOT / name, bundle / name)
    shutil.copytree(ROOT / "third_party" / "licenses", bundle / "licenses", dirs_exist_ok=True)
    for package in ("Pillow", "pi-heif", "PyInstaller"):
        distribution = metadata.distribution(package)
        for item in distribution.files or []:
            path = str(item).replace("\\", "/")
            if ".dist-info/" in path and ("/licenses/" in path or item.name.lower().startswith(("license", "copying"))):
                destination = bundle / "licenses" / package / item.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(distribution.locate_file(item), destination)
    python_license = Path(sys.base_prefix) / "LICENSE.txt"
    if not python_license.exists():
        raise FileNotFoundError("Python LICENSE.txt is required in the Python installation")
    shutil.copy2(python_license, bundle / "licenses" / "Python-LICENSE.txt")
    source = bundle / "source"
    source.mkdir(exist_ok=True)
    for name in ("heic_to_jpg.py", "requirements.txt", "requirements-build.txt"):
        shutil.copy2(ROOT / name, source / name)
    (bundle / "BUILD_INFO.txt").write_text(
        f"HEIC-to-JPG {args.version}\nPython {sys.version}\n"
        + "\n".join(f"{name}=={metadata.version(name)}" for name in ("Pillow", "pi-heif", "PyInstaller"))
        + "\nWindows x64, PyInstaller onedir; external DLL replacement supported.\n",
        encoding="utf-8")
    archive = shutil.make_archive(str(ROOT / "dist" / f"HEIC-to-JPG-v{args.version}-windows-x64"), "zip", bundle.parent, bundle.name)
    digest = hashlib.sha256(Path(archive).read_bytes()).hexdigest()
    print(f"Created {archive}\nSHA256 {digest}")


if __name__ == "__main__":
    main()
