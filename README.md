# Pyads Console

Super basic Qt application with an embedded console to interact with TwinCAT ADS.

This is made with [`pyads`](https://github.com/stlehmann/pyads), [`PySide6`](https://wiki.qt.io/Qt_for_Python) and [`qtconsole`](https://github.com/pyqtconsole/pyqtconsole).

![Application screenshot](screenshot.jpg)

## Features

- Use the `plc` variable for the local ADS connection.
- Returned symbols are patched with respect to the `pyads` default: there is a `__getattr__` implementation to automatically retrieve child symbols.  
  E.g.:  
  ```python
  var = plc.get_symbol("GVL_Main.fbBlock")
  sub_var = va.fOutput  # The PLC field `fOutput` must exist
  sub_var.read()  # Ends up reading "GVL_Main.fbBlock.fOutput"
  ``` 

## How to use

### How to install

Perform a user-wide install with [pipx](https://pipx.pypa.io/stable/) through:
```
pipx install git+https://github.com/RobertoRoos/pyads-console@main 
```

Or clone and then install with `uv` (preferred over Pip):
```
uv sync
```

Or with Pip directly:
```
pip install .
```

### How to run

Start the application through `uv` (which will automatically handle dependencies):
```
uv run pyads-console
```

Or start the application from Python with:
```
python -m pyads_console
```

Or use the executable directly:
```
pyads-console.exe
```
