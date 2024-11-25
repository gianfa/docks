import re
from typing import Optional


def extract_files(dockerfile_path: str) -> list[dict[str, Optional[str]]]:
    """
    Extracts files copied or added in the Dockerfile with their sources and destinations.

    Parameters
    ----------
    dockerfile_path : str
        Path to the Dockerfile.

    Returns
    -------
    list[dict[str, str | None]]
        A list of dictionaries with file details:
        - command: Either 'COPY' or 'ADD'.
        - source: The source path of the file.
        - destination: The destination path in the container.
        - docstring: Description of the action (if available).
    """
    files = []
    comment_block = []
    with open(dockerfile_path, "r") as file:
        for line in file:
            stripped = line.strip()
            # Accumulate comments for potential docstring
            if stripped.startswith("#"):
                comment_block.append(stripped[1:].strip())
            elif stripped.startswith(("COPY", "ADD")):
                # Extract command, source, and destination
                parts = stripped.split(" ", 2)
                command = parts[0]
                paths = parts[1].split(" ", 1)
                source = paths[0].strip()
                destination = paths[1].strip() if len(paths) > 1 else None

                # Process comment block for docstring
                docstring = None
                if comment_block:
                    docstring = " ".join(comment_block)

                files.append(
                    {
                        "command": command,
                        "source": source,
                        "destination": destination,
                        "docstring": docstring,
                    }
                )
                # Clear comment block after processing
                comment_block = []
            else:
                # Reset comment block if a non-comment, non-file line is encountered
                comment_block = []
    return files
