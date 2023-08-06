# Namespace for Redesigning Psychiatry packages

This project represents the implicit namespace `redesign` in the names of
packages from the
[Redesigning Psychiatry](https://github.com/redesigningpsychiatry)
programme (such as `redesign.health`).

Note that this project is not a dependency of such packages. It exists merely
to indicate that an explicit module named `redesign` would cause a namespace
conflict with these packages. Installing this package will add a
`redesign.info` module that attaches a docstring to the `redesign` namespace
when imported.