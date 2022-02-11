# `sphere_mesh` _ChRIS_ Plugin Wrapper

[![Version](https://img.shields.io/docker/v/fnndsc/ep-sphere_mesh?sort=semver)](https://hub.docker.com/r/fnndsc/ep-sphere_mesh)
[![MIT License](https://img.shields.io/github/license/fnndsc/ep-sphere_mesh)](https://github.com/FNNDSC/ep-sphere_mesh/blob/main/LICENSE)
[![Build](https://github.com/FNNDSC/ep-sphere_mesh/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/ep-sphere_mesh/actions)

`ep-sphere_mesh` is a _ChRIS_ _ds_ plugin that runs the `sphere_mesh` program
(implementation of marching-cubes in CIVET for brain surface extraction) on
brain hemisphere masks from its input directory, creating surface `.obj` files
in its output directory.

Hemisphere side (left or right) can be inferred from the input file path name.
