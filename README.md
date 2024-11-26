<!-- markdownlint-disable MD024 -->
# Docks: Easy Dockerfile Documentation Generator 📜🐳

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
<!-- TODO: add Pypi version -->
![publish workflow](https://github.com/gianfa/docks/actions/workflows/publish.yml/badge.svg?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**docks** is a Python framework designed to generate Markdown documentation for your Dockerfiles. It extracts key elements such as base images, `ARG`/`ENV` variables, exposed ports, and copied/added files, producing clear, structured documentation.

- [Features ✨](#features-)
- [Installation 🚀](#installation-)
  - [Using Poetry](#using-poetry)
  - [Using Pip](#using-pip)
- [Usage 🛠️](#usage-️)
  - [Via CLI](#via-cli)
    - [CLI Arguments](#cli-arguments)
  - [Via Python](#via-python)
    - [Example: Generate Documentation from a Dockerfile](#example-generate-documentation-from-a-dockerfile)
- [Dockerfile Docstring Convention 📝](#dockerfile-docstring-convention-)
  - [ARG/ENV Variables](#argenv-variables)
    - [Example](#example)
  - [EXPOSE Ports](#expose-ports)
    - [Example](#example-1)
  - [COPY/ADD Files](#copyadd-files)
    - [Example](#example-2)
- [Testing ✅](#testing-)
- [Contributing 🤝](#contributing-)

## Features ✨

- Extracts:
  - **Base Images** (`FROM`)
  - **ARG/ENV Variables** with optional docstrings and references
  - **Exposed Ports** with descriptions
  - **Copied/Added Files** (`COPY`/`ADD`) with context
- Outputs clean **Markdown documentation** for your Dockerfiles.
- Easy to use, modular, and extensible.

## Installation 🚀

Install **docks** via [Poetry](https://python-poetry.org/) or pip:

### Using Poetry

```bash
poetry add docks
```

### Using Pip

```bash
pip install docks
```

## Usage 🛠️

### Via CLI

The `docks` CLI allows you to quickly generate Markdown documentation for a Dockerfile without writing code.

Here is all you have to do in order to generate the documentation.

```bash
docks <dockerfile> <output>
# e.g.
# docks myproject/Dockerfile myproject/dockerfile-doc.md
```

#### CLI Arguments

- `dockerfile`: Path to the Dockerfile to document.
- `output`: Path to save the generated Markdown documentation.

### Via Python

You can also easily create the documentation programmatically via Python.

#### Example: Generate Documentation from a Dockerfile

1. Ensure you have a valid Dockerfile in your project.
2. Run the following Python script

```python
from docks.generate_doc import generate_markdown

# Path to your Dockerfile
dockerfile_path = "Dockerfile"

# Output Markdown file
output_path = "README.md"

# Generate documentation
generate_markdown(dockerfile_path, output_path)
```

## Dockerfile Docstring Convention 📝

### ARG/ENV Variables

- Include a block comment directly above the variable.
- Start the comment with the variable name followed by `:` for docstring extraction.
- Optionally include a reference using `@ref:`.

#### Example

```Dockerfile
# MY_VAR: Description of the variable.
# @ref: https://example.com/docs
ARG MY_VAR=default
```

### EXPOSE Ports

Include a comment directly above the `EXPOSE` command.
Start with the port number followed by `:` for the description.

#### Example

```Dockerfile
# 8080: Main HTTP server port
EXPOSE 8080
```

### COPY/ADD Files

Add a comment directly above the `COPY` or `ADD` command for context.

#### Example

```Dockerfile
# Copy application code to the container
COPY src/ /app/
```

## Testing ✅

Run tests with pytest:

```bash
pytest tests/
```

## Contributing 🤝

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/<FEATURE_NAME>`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push the branch: `git push origin feature/<FEATURE_NAME>`.
5. Open a pull request.
