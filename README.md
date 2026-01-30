# Set of tools to be used in scientific research projects.

This project provides several functions with default parameters to use in scientific manipulation, data management, 
plot functions, among other features.

## Data I/O

Data format is inferred from the file extension. Use [research_tools/in_out.py](research_tools/in_out.py) for loading and saving common formats (JSON, CSV, Excel, MATLAB, NumPy, text, pickle).

```python
from research_tools.in_out import load, save

data = load('path_to_folder/config.json')
df = load('path_to_folder/data.csv', downcast_type=True)
save('path_to_folder/out.json', data)
save('path_to_folder/out.csv', df)
```

## Modules

- **conversions.py**: Functions for units conversion (e.g., linear to dB).
- **dump_functions.py**: Simple functions for debugging purposes.
- **error_handling.py**: Functions for handling file/folder errors, especially on Windows.
- **in_out.py**: Functions for data input/output, folder creation, and path management.
- **math.py**: Functions for mathematical operations and calculations.
- **parallelization.py**: Tools for managing CPU core parallelization.
- **plot.py**: Functions for plotting and figure management.
- **progress_bar.py**: Functions for creating and managing progress bars.
- **utils.py**: Utility functions for data manipulation.
