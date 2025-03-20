---
name: Release
about: package release operations
title: Release vx.x.x
labels: ''
assignees: ''

---

- [ ] Run workflow ['Create Release Branch'](https://github.com/unaguna/random-obj-generator/actions/workflows/release_branch.yml)
  - create branch `release/vx.x.x` and checkout it
  - increment version number of `./randog/__init__.py`
  - increment version number of `./README.md`
  - build sphinx document
  - pull request `release` into `develop` branch
- [ ] wait for merge
- [ ] publish to test.pypi by GitHub Action
- [ ] pull request `develop` into `main` branch
- [ ] wait for merge
- [ ] create release
- [ ] inspect content published by GitHub Action
