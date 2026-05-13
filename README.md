# research_tools

Small Python helpers for scientific workflows: unit conversions, I/O across common file formats, plotting utilities, progress feedback, and related utilities. The package favors sensible defaults so you can call functions with minimal configuration.

**Python:** 3.12 or newer (see [`pyproject.toml`](pyproject.toml)).

## Installation

From the repository root:

```bash
pip install .
```

With optional development dependencies (tests, coverage, Ruff):

```bash
pip install -e ".[dev]"
```

Runtime dependencies include NumPy, SciPy, pandas, Matplotlib, Seaborn, PyArrow, Rich, and libraries used for spreadsheets (OpenPyXL, xlrd, odfpy). The full list is in [`pyproject.toml`](pyproject.toml).

## Data I/O

Format is chosen from the file extension. Use [`research_tools/in_out.py`](research_tools/in_out.py) for `load` and `save`.

**Supported extensions:** `.json`, `.csv`, `.mat`, `.npy`, `.npz`, `.xlsx`, `.xls`, `.ods`, `.txt`, `.pickle`, `.pkl`, `.p` (pickle).

```python
from research_tools.in_out import load, save

data = load("path/to/config.json")
df = load("path/to/data.csv", downcast_type=True)
save("path/to/out.json", data)
save("path/to/out.csv", df)
```

## Package layout

| Module | Role |
| --- | --- |
| [`conversions.py`](research_tools/conversions.py) | Unit and signal conversions (e.g. linear ↔ dB, frequency ↔ wavelength). |
| [`constants.py`](research_tools/constants.py) | Shared constants. |
| [`dump_functions.py`](research_tools/dump_functions.py) | Lightweight helpers for debugging and inspection. |
| [`error_handling.py`](research_tools/error_handling.py) | File and folder error handling (including Windows read-only cases). |
| [`in_out.py`](research_tools/in_out.py) | Load/save, paths, and folder creation. |
| [`math.py`](research_tools/math.py) | Math helpers built on the conversions utilities. |
| [`parallelization.py`](research_tools/parallelization.py) | CPU parallelization helpers. |
| [`plot.py`](research_tools/plot.py) | Plotting and figure management. |
| [`progress_bar.py`](research_tools/progress_bar.py) | Progress display (Rich-based). |
| [`utils.py`](research_tools/utils.py) | General utilities (e.g. dict defaults, DataFrame size reduction). |

## Development

Run the test suite from the repository root:

```bash
python -m pytest
```

With coverage (requires the `dev` extra):

```bash
python -m pytest --cov=research_tools --cov-report=term-missing
```

Lint:

```bash
ruff check .
```
