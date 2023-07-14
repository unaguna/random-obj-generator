## setup environment for spinx

1. Prepare python >= 3.8 environment by venv or other means. For example: `python -m venv .venv_sphinx`.
2. Activate above environment.
3. Install modules by command `pip install -r requirements_sphinx.txt`.

## steps to build documents

1. Activate above environment.
2. `.\make.bat gettext`
3. `sphinx-intl update -p build/gettext -l ja`
4. update `*.po`s, the translation files
5. `.\make.bat doc`
   - `doc` is alias to build en and ja
