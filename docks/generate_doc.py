"""
Generates Dockerfile documentation with a Docker build example.
"""

from .base_image import extract_base_images
from .files import extract_files
from .ports import extract_exposed_ports
from .variables import extract_variables
from .generate_example import extract_dockerfile_details, generate_docker_build_markdown
from .mounts import extract_mounts


def generate_markdown(
    dockerfile_path: str,
    output_path: str = "dockerfile-doc.md",
    title="Dockerfile Documentation",
    verbose: bool = True,
) -> None:
    """
    Generates Markdown documentation for the given Dockerfile.

    Parameters
    ----------
    dockerfile_path : str
        Path to the Dockerfile.
    output_path : str, optional
        Path to save the generated Markdown documentation (default: "dockerfile-doc.md").
    verbose : bool, optional
        If True, prints a message when done (default: True).
    """
    base_images = extract_base_images(dockerfile_path)
    variables = extract_variables(dockerfile_path)
    ports = extract_exposed_ports(dockerfile_path)
    files = extract_files(dockerfile_path)
    mounts = extract_mounts(dockerfile_path)
    docker_details = extract_dockerfile_details(
        dockerfile_path
    )  # Extract details for the example
    docker_example = generate_docker_build_markdown(
        docker_details
    )  # Create docker build example

    with open(output_path, "w") as md_file:
        md_file.write(f"# {title}\n\n")

        # Base images
        md_file.write("## Base Images\n\n")
        for image in base_images:
            md_file.write(f"- `{image['image']}` (Alias: {image['alias']})\n")

        # Secret Mounts
        md_file.write("\n## Mounted Volumes\n\n")
        mounts = extract_mounts(dockerfile_path)
        if mounts:
            for mount in mounts:
                md_file.write(
                    f"- **Type:** `{mount['type']}`\n"
                    f"  - **ID:** `{mount['id'] or 'N/A'}`\n"
                    f"  - **Destination:** `{mount['dst'] or 'N/A'}`\n"
                )
        else:
            md_file.write("(No mounts declared)\n")

        # Variables
        md_file.write("\n## Variables\n\n")

        # ARG variables
        md_file.write("### ARG Variables\n\n")
        arg_vars = [var for var in variables if var["type"] == "ARG"]
        if arg_vars:
            for var in arg_vars:
                md_file.write(
                    f"- `{var['name']}`: Defaults to `{var['value'] or ' '}`."
                )
                if var["docstring"]:
                    md_file.write(f" {var['docstring']}")
                if var["reference"]:
                    md_file.write(f"  - [Reference]({var['reference']})")
                md_file.write("\n")
        else:
            md_file.write("(None)\n")

        # ENV variables
        md_file.write("\n### ENV Variables\n\n")
        env_vars = [var for var in variables if var["type"] == "ENV"]
        if env_vars:
            for var in env_vars:
                md_file.write(
                    f"- `{var['name']}`: Defaults to `{var['value'] or ' '}`."
                )
                if var["docstring"]:
                    md_file.write(f"  - {var['docstring']}")
                if var["reference"]:
                    md_file.write(f"  - [Reference]({var['reference']})")
                md_file.write("\n")
        else:
            md_file.write("(None)\n")

        # Ports
        md_file.write("\n## Exposed Ports\n\n")
        if ports:
            for port in ports:
                md_file.write(
                    f"- **{port['port']}**: {port['docstring'] or 'No description'}\n"
                )
        else:
            md_file.write("(None)\n")

        # Files
        md_file.write("\n## Files Copied/Added\n\n")
        if files:
            for file in files:
                md_file.write(
                    f"- `{file['command']}`: `{file['source']}` -> `{file['destination'] or 'N/A'}`\n"
                )
                if file["docstring"]:
                    md_file.write(f"  - {file['docstring']}\n")
        else:
            md_file.write("(None)\n")

        # Docker Build Example
        md_file.write("\n## Docker Build Command Example\n\n")
        md_file.write(docker_example)

    if verbose:
        print(f"Documentation generated at {output_path}")
