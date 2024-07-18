import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "DLLs"))

import clr

clr.AddReference("CalcTest") # type: ignore

from CalcTest import Calculator

print(Calculator.Add(1, 1))
