# p1_helpers

Package with common helper functions we use all the time.
We use it to reduce code repeating and unify common processes.

```bash
$ tree p1_helpers/
p1_helpers/
├── dbg.py
├── io_.py
├── parser.py
├── printing.py
├── s3.py
└── system_interaction.py
```

## Package contents
- `dbg.py` - debugging wrappers, logging, assertion wrappers
- `io_.py` - input output, files/folders management
- `parser.py` - Argparse extends
- `printing.py` - printing helpers
- `s3.py` - AWS S3 interaction
- `system_interaction.py` - CLI wrappers


## Build package 
- Build
```bash
$ python -m build --no-isolation
```
Will create `dist/` folder with package.
- Test your package with local installation
## Upload package to pypi.org
### Test upload
Before upload on pypy.org try to upload using test.pypi.org server,
more info here [https://packaging.python.org/guides/using-testpypi/](https://packaging.python.org/guides/using-testpypi/).  
- Register separate account here [https://test.pypi.org/](https://test.pypi.org/)  
- Create token.  
- Update your `~/.pypirc`
```bash
[testpypi]
  username = __token__
  password = Your_token_from_test_pypi_org_here
```
- Check your upload
```bash
$ python -m twine upload --repository testpypi dist/*
```
### Production upload
- Generate token
[https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)

- Edit or create a `~/.pypirc` file with following structure:

```bash
[pypi]
  username = __token__
  password = Your_token_here
```

- Upload package using twine.
```bash
$ python -m twine upload --repository pypi dist/*
```