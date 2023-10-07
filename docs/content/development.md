# Development

### slap-cli

Slap ([slap-cli](https://niklasrosenstein.github.io/slap/)) is the Python package 
management and release tool that makes this package possible.

```shell
# Create a new venv "elasticsearch-kibana-cli" to work within
$ slap venv -cg elasticsearch-kibana-cli

# Activate the "elasticsearch-kibana-cli" venv
$ slap venv -ag elasticsearch-kibana-cli

# Install the requirements for the "elasticsearch-kibana-cli" development venv
$ slap install --upgrade --link

# Update code formatting
$ slap run format

# Run a local docs server
$ slap run docs-server

# Test the package (pytest, black, isort, flake8, safety)
$ slap test

# Write a "feature" changelog entry
$ slap changelog add -t "feature" -d "<changelog message>" [--issue <issue_url>]

# Bump the package version at the "patch" semver level
$ slap release patch --dry
$ slap release patch --tag --push

# Build a package
$ slap publish --build-directory build --dry

# Publish a package
$ slap publish
```
