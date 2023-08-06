# schemdule-extensions-simplegui

![](https://github.com/StardustDL/schemdule/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/schemdule.svg) [![](https://img.shields.io/pypi/v/schemdule-extensions-simplegui.svg?logo=pypi)](https://pypi.org/project/schemdule-extensions-simplegui/) [![Downloads](https://pepy.tech/badge/schemdule-extensions-simplegui)](https://pepy.tech/project/schemdule-extensions-simplegui)

A simple GUI extension for 
[Schemdule](https://github.com/StardustDL/schemdule).

- Platform ![](https://img.shields.io/badge/Linux-yes-success?logo=linux) ![](https://img.shields.io/badge/Windows-yes-success?logo=windows) ![](https://img.shields.io/badge/MacOS-yes-success?logo=apple) ![](https://img.shields.io/badge/BSD-yes-success?logo=freebsd)
- Python ![](https://img.shields.io/pypi/implementation/schemdule.svg?logo=pypi) ![](https://img.shields.io/pypi/pyversions/schemdule.svg?logo=pypi) ![](https://img.shields.io/pypi/wheel/schemdule.svg?logo=pypi)
- [All extensions](https://pypi.org/search/?q=schemdule)

## Install

```sh
$ pip install schemdule-extensions-simplegui
```

## Usage

This extension provide a `MessageBoxPrompter` and add the following extension methods on `PrompterConfiger`.

```python
class PrompterConfiger:
    def useMessageBox(self, final: bool = False, auto_close: bool = False) -> "PrompterConfiger":
        ...
```

Use the extension in the schema script.

```python
# schema.py
ext("simplegui")

prompter.useMessageBox()
```

