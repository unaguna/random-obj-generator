## steps to build documents

1. `.\make.bat gettext`
2. `sphinx-intl update -p build/gettext -l ja`
3. update `*.po`s, the translation files
4. `.\make.bat doc`
   - `doc` is alias to build en and ja
