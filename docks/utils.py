"""
"""

import re
from typing import List, Optional, Tuple


def extract_docstring(
    comment_block: List[str], identifier: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts the docstring and reference from a block of comments.

    Parameters
    ----------
    comment_block : List[str]
        The lines of comments immediately preceding a Dockerfile instruction.
    identifier : str
        The identifier being documented (e.g., variable name or port number).

    Returns
    -------
    Tuple[Optional[str], Optional[str]]
        A tuple containing:
        - docstring: The extracted description (if available).
        - reference: The extracted reference URL (if available).
    """
    if not comment_block:
        return None, None

    # Normalize and join the comment block into a single string with proper spacing
    joined_comment = " ".join(line.strip() for line in comment_block)

    # Match docstring convention: starts with identifier:
    docstring = None
    reference = None
    docstring_match = re.match(rf"^{re.escape(identifier)}:\s*(.+)", joined_comment)
    if docstring_match:
        docstring = docstring_match.group(1)

        # Extract @ref tag if present
        ref_match = re.search(r"@ref:\s*(\S+)", docstring)
        if ref_match:
            reference = ref_match.group(1)
            docstring = re.sub(r"@ref:\s*\S+", "", docstring).strip()

    return docstring, reference
