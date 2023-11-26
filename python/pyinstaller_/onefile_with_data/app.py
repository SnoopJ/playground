import sys
from pathlib import Path

HERE = Path(__file__).parent


print("Hello world!")
print(f"Running from {sys._MEIPASS = } ({HERE = })")


print(f"Running open(Path(HERE, 'data.txt'), 'r')")
with open(Path(HERE, 'data.txt'), 'r') as f:
    data = f.read()
    print(f"Read data: {data!r}")


print(f"Running open(Path(sys._MEIPASS, 'data.txt'), 'r')")
with open(Path(sys._MEIPASS, 'data.txt'), 'r') as f:
    data = f.read()
    print(f"Read data: {data!r}")
