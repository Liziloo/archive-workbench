import pathlib
from app.core.config import settings

def check():
    sources = [
        ("RAW", settings.PATH_RAW),
        ("EDITED", settings.PATH_EDITED),
        ("CARL", settings.PATH_CARL),
    ]

    print("\n🔍 PATH DIAGNOSTIC")
    print("="*50)

    for label, path_str in sources:
        path = pathlib.Path(path_str)
        exists = path.exists()
        status = "✅ EXISTS" if exists else "❌ NOT FOUND"

        print(f"{label:<10} | {status}")
        print(f"Path:      [{path_str}]")

        if exists:
            # Count images
            valid_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}
            count = len([f for f in path.rglob("*") if f.suffix.lower() in valid_exts])
            print(f"Contents:  {count} archival files found")
        print("-" * 50)

if __name__ == "__main__":
    check()