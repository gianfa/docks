"""
Extract mounts
"""

import re
from typing import List, Dict, Optional


def extract_mounts(dockerfile_path: str) -> List[Dict[str, Optional[str]]]:
    """
    Extracts mounts from the Dockerfile, including --mount options in RUN commands.

    Parameters
    ----------
    dockerfile_path : str
        Path to the Dockerfile.

    Returns
    -------
    List[Dict[str, Optional[str]]]
        A list of dictionaries with mount details:
        - type: Type of mount (e.g., 'secret', 'bind', 'cache').
        - id: Identifier for the mount (if applicable).
        - dst: Destination path in the container.
        - options: Additional options provided.
    """
    mounts = []
    mount_pattern = re.compile(r"--mount=type=(\w+),([^ ]+)")

    with open(dockerfile_path, "r") as file:
        for line in file:
            stripped = line.strip()

            # Match --mount in RUN commands
            matches = mount_pattern.findall(stripped)
            for match in matches:
                mount_type, options_str = match
                options = dict(re.findall(r"(\w+)=([^,]+)", options_str))
                mounts.append(
                    {
                        "type": mount_type,
                        "id": options.get("id"),
                        "dst": options.get("dst"),
                        "options": ", ".join(f"{k}={v}" for k, v in options.items()),
                    }
                )

    return mounts
