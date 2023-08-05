# Codescan

Codescan is a Python utility for checking codes for possible security credentials leaks that might be committed into a repository

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install codescan.

```bash
pip install codescan
```

## Usage

Scan the current directory that is git initialized.
```bash
python -m codescan
```
By default codescan checks the current working directory and look into the "git status" results for staged files. The staged files will then be scan for possible credential leaks.

To do a full scan specify a -f flag and -i [ignore file] option
```bash
python -m codescan -f -i .gitignore
```
The full scan will go through all the files in the current directory and checks for security leaks. an ignore file needs to be specify for codescan to skip scanning 3rd party directory such as vendor or node_modules. The .gitignore file can be used or a separate ignore file can be specified.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)