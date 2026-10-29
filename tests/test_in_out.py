from pathlib import Path

import numpy as np
import pytest

from research_tools.in_out import load, save


def test_save_wrapped_opt_round_trip(tmp_path: Path) -> None:
    """Wrapped JSON loads back to the same structure."""
    data = {'a': 1, 'b': {'c': [1.0, 2.0, 3.0]}}
    path = tmp_path / 'out.json'
    save(path, data=data, wrapped_opt=True)
    assert load(path) == data


def test_save_wrapped_opt_wraps_long_scalar_arrays(tmp_path: Path) -> None:
    """Long scalar arrays split across multiple lines near line_width."""
    line_width = 120
    data = {'value': list(range(200))}
    path = tmp_path / 'out.json'
    save(path, data=data, wrapped_opt=True, line_width=line_width)
    text = path.read_text(encoding='utf-8')
    array_lines = [
        line for line in text.splitlines()
        if line.startswith('    ') and line[0].isspace() and any(ch.isdigit() for ch in line)
    ]
    assert len(array_lines) > 1
    for line in array_lines:
        assert len(line) <= line_width + 1
    assert load(path) == data


def test_save_wrapped_opt_numpy_values(tmp_path: Path) -> None:
    """NumPy scalars and arrays are normalized like save()."""
    data = {'x': np.float64(1.5), 'y': np.array([1, 2, 3])}
    path = tmp_path / 'out.json'
    save(path, data=data, wrapped_opt=True)
    assert load(path) == {'x': 1.5, 'y': [1, 2, 3]}


def test_save_wrapped_opt_rejects_nested_arrays(tmp_path: Path) -> None:
    """Nested lists inside arrays are not supported."""
    path = tmp_path / 'out.json'
    with pytest.raises(TypeError, match='scalar arrays'):
        save(path, data={'bad': [[1, 2]]}, wrapped_opt=True)


def test_save_wrapped_opt_no_overwrite(tmp_path: Path) -> None:
    """overwrite=False raises when the file exists."""
    path = tmp_path / 'out.json'
    save(path, data={'a': 1}, wrapped_opt=True)
    with pytest.raises(FileExistsError):
        save(path, data={'a': 2}, wrapped_opt=True, overwrite=False)
