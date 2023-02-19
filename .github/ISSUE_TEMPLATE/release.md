---
name: Release
about: package release operations
title: ''
labels: ''
assignees: ''

---

- [ ] create branch `release` and checkout it
- [ ] increment version number of `./randog/__init__.py`
- [ ] build sphinx document
- [ ] pull request `release` into `develop` branch
- [ ] wait for merge
- [ ] checkout `develop` and build package
- [ ] publish to test.pypi
- [ ] publish to pypi
- [ ] pull request `develop` into `main` branch
- [ ] wait for merge
- [ ] create release
