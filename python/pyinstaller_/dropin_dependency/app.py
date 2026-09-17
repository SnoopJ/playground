import sys
from pathlib import Path


HERE = Path(__file__).parent


if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    vendor_pth = Path(sys.executable).parent.joinpath("vendor")
    print(f"Inserting vendor path on sys.path: {vendor_pth!r}")
    sys.path.insert(0, str(vendor_pth))


def main():
    try:
        import acme
        print(f"Loaded acme from {acme.__file__!r}")
        acme.bark()
    except ImportError as exc:
        sys.exit(exc)


if __name__ == "__main__":
    main()

