import re


def extract_base_images(dockerfile_path: str) -> list[dict[str, str]]:
    """
    Extracts all base images used in a multistage Dockerfile.

    Parameters
    ----------
    dockerfile_path : str
        Path to the Dockerfile.

    Returns
    -------
    list[dict[str, str]]
        A list of dictionaries containing the base image and optional stage alias.
        Example: [{'image': 'python:3.10-slim', 'alias': 'builder'}, ...]
    """
    base_images = []
    with open(dockerfile_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("FROM"):
                parts = line.split(" ", 2)
                base_image = parts[1]  # Extract the image
                alias = parts[2] if len(parts) > 2 else None  # Optional alias
                base_images.append({"image": base_image, "alias": alias or "No alias"})
    return base_images
