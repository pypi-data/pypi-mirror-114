# Introduction 

Eze example plugin, provides a starter project for extending the capabilities of Eze, by adding new security tools or report types.

# Getting Started

- Eze Cli and it's sub-repos are powered by python and docker, make sure you have the latest versions installed
- Have you read the [Contributing Guide](CONTRIBUTING.md)?
- Have you read the [Code Of Conduct](CODE_OF_CONDUCT.md)?
- Check out the [existing issues](https://github.com/https://github.com/RiverSafeUK/eze-example-plugin/issues) to see if any issues you're interested in have already been raised

# Build and Test

## Install Locally (via make)

```bash
make plugin-install
```

## Install Locally (Manual via pip)

```bash
rm dist/eze-example-plugin-*.tar.gz
python setup.py sdist
pip install dist/eze-example-plugin-*.tar.gz
```

## Test installed correctly

```bash
eze tools list
eze reporters list
```

# Contribute

See [CONTRIBUTING GUIDE](CONTRIBUTING.md)