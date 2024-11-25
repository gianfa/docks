import re
from typing import Optional

from docks.utils import extract_docstring


def extract_variables(dockerfile_path: str) -> list[dict[str, Optional[str]]]:
    """
    Extracts ARG and ENV variables with their values and docstring information.
    """
    variables = []
    comment_block = []
    with open(dockerfile_path, "r") as file:
        for line in file:
            stripped = line.strip()
            if stripped.startswith("#"):
                comment_block.append(stripped[1:].strip())
            elif stripped.startswith(("ARG", "ENV")):
                parts = stripped.split(" ", 1)
                var_type = parts[0]
                var_def = parts[1].split("=", 1)
                var_name = var_def[0].strip()
                var_value = var_def[1].strip() if len(var_def) > 1 else None

                # Use abstracted function for docstring extraction
                docstring, reference = extract_docstring(comment_block, var_name)

                variables.append(
                    {
                        "name": var_name,
                        "type": var_type,
                        "value": var_value,
                        "docstring": docstring,
                        "reference": reference,
                    }
                )
                comment_block = []
            else:
                comment_block = []
    return variables
