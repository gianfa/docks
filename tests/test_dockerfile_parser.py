import pytest

from docks.variables import extract_docstring, extract_variables


def test_extract_docstring_single_line():
    comment_block = ["PACKAGE_TO_ADD_NAME: This is a test variable."]
    identifier = "PACKAGE_TO_ADD_NAME"
    docstring, reference = extract_docstring(comment_block, identifier)
    assert docstring == "This is a test variable."
    assert reference is None


def test_extract_docstring_multiline():
    comment_block = [
        "PACKAGE_TO_ADD_NAME: This is a test variable, used for",
        "testing multiline docstring extraction.",
        "@ref: https://example.com/docs",
    ]
    identifier = "PACKAGE_TO_ADD_NAME"
    docstring, reference = extract_docstring(comment_block, identifier)
    assert (
        docstring
        == "This is a test variable, used for testing multiline docstring extraction."
    )
    assert reference == "https://example.com/docs"


def test_extract_docstring_no_match():
    comment_block = ["Some unrelated comment."]
    identifier = "PACKAGE_TO_ADD_NAME"
    docstring, reference = extract_docstring(comment_block, identifier)
    assert docstring is None
    assert reference is None


def test_extract_variables(tmp_path):
    # Create a temporary Dockerfile
    dockerfile_content = """
    # PACKAGE_TO_ADD_NAME: Name the python package to add in the image, from which
    #   to then build the virtual environment. It must be available in repositories
    #   Pypi or SecondRepo.
    #   If it is not specified, the default venv from ZZ will be the one available.
    ARG PACKAGE_TO_ADD_NAME=""

    # APP_PORT: The port for the application.
    # @ref: https://example.com/app-port
    ENV APP_PORT=8080
    """
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(dockerfile_content)

    # Run the function
    variables = extract_variables(str(dockerfile))

    # Validate the output
    assert len(variables) == 2

    assert variables[0]["name"] == "PACKAGE_TO_ADD_NAME"
    assert variables[0]["type"] == "ARG"
    assert variables[0]["value"] == '""'
    assert variables[0]["docstring"] == (
        "Name the python package to add in the image, from which to then "
        "build the virtual environment. It must be available in repositories "
        "Pypi or SecondRepo. If it is not specified, the default venv from ZZ "
        "will be the one available."
    )
    assert variables[0]["reference"] is None

    assert variables[1]["name"] == "APP_PORT"
    assert variables[1]["type"] == "ENV"
    assert variables[1]["value"] == "8080"
    assert variables[1]["docstring"] == "The port for the application."
    assert variables[1]["reference"] == "https://example.com/app-port"
