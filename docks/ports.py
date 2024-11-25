import re
from typing import Optional


def extract_exposed_ports(dockerfile_path: str) -> list[dict[str, Optional[str]]]:
    """
    Extracts exposed ports and their descriptions from a Dockerfile.

    Parameters
    ----------
    dockerfile_path : str
        Path to the Dockerfile.

    Returns
    -------
    list[dict[str, int | str | None]]
        A list of dictionaries with port details:
        - port: The exposed port as an integer.
        - docstring: Description of the port (if available).
    """
    ports = []
    comment_block = []
    with open(dockerfile_path, "r") as file:
        for line in file:
            stripped = line.strip()
            # Accumulate comments for potential docstring
            if stripped.startswith("#"):
                comment_block.append(stripped[1:].strip())
            elif stripped.startswith("EXPOSE"):
                # Extract the port number
                port_number = int(stripped.split(" ")[1].strip())
                docstring = None
                if comment_block:
                    # Join comments and match docstring convention
                    joined_comment = " ".join(comment_block)
                    port_match = re.match(rf"{port_number}:\s*(.+)", joined_comment)
                    if port_match:
                        docstring = port_match.group(1)
                ports.append({"port": port_number, "docstring": docstring})
                # Clear comment block after processing
                comment_block = []
            else:
                # Reset comment block if a non-comment, non-port line is encountered
                comment_block = []
    return ports
