# pythonnet-poc

POC demonstrating how to use [pythonnet](http://pythonnet.github.io/)

## Requirements

- [.NET SDK](https://dotnet.microsoft.com/en-us/download)
- [pythonnet-stub-generator](https://github.com/MHDante/pythonnet-stub-generator)
- [Python 3.11](https://www.python.org/downloads/)


## 1. Install poetry and set up the Python venv

```
pip install poetry
poetry install
```

## 2. Compile the DLL and generate the type stubs

In src/CalcTestLib execute

```
dotnet publish -c Release
```

The type stubs can be used out-of-the-box in VS Code to get auto-completion.

## 3. Load the DLL and use it like a native Python library

In src/pythonnet_poc execute

```
python poc.py
```
