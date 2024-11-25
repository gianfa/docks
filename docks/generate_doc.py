"""
"""

from .base_image import extract_base_images
from .files import extract_files
from .ports import extract_exposed_ports
from .variables import extract_variables


def generate_markdown(
    dockerfile_path: str, output_path: str = "dockerfile-doc.md", verbose: str = True
) -> None:
    """
    Generates Markdown documentation for the given Dockerfile.
    """
    base_images = extract_base_images(dockerfile_path)
    variables = extract_variables(dockerfile_path)
    ports = extract_exposed_ports(dockerfile_path)
    files = extract_files(dockerfile_path)

    with open(output_path, "w") as md_file:
        md_file.write("# Dockerfile Documentation\n\n")

        # Base images
        md_file.write("## Base Images\n\n")
        for image in base_images:
            md_file.write(f"- `{image['image']}` (Alias: {image['alias']})\n")

        # Variables
        md_file.write("\n## Variables\n\n")
        # ARG variables
        md_file.write("### ARG Variables\n\n")
        for var in variables:
            if var["type"] == "ARG":
                md_file.write(
                    f"- `{var['name']}`: Defaults to `{var['value'] or ' '}`."
                )
                if var["docstring"]:
                    md_file.write(f" {var['docstring']}")
                if var["reference"]:
                    md_file.write(f"  - [Reference]({var['reference']})")
                md_file.write("\n")
        # ENV variables
        md_file.write("\n### ENV Variables\n\n")
        for var in variables:
            if var["type"] == "ENV":
                md_file.write(
                    f"- `{var['name']}`: Defaults to `{var['value'] or ' '}`."
                )
                if var["docstring"]:
                    md_file.write(f"  - {var['docstring']}")
                if var["reference"]:
                    md_file.write(f"  - [Reference]({var['reference']})")
                md_file.write("\n")

        # Ports
        md_file.write("\n## Exposed Ports\n\n")
        if len(ports) > 0:
            for port in ports:
                md_file.write(
                    f"- **{port['port']}**: {port['docstring'] or 'No description'}\n"
                )
        else:
            md_file.write("None.")
        md_file.write("\n")

        # Files
        md_file.write("\n## Files Copied/Added\n\n")
        if len(files) > 0:
            for file in files:
                md_file.write(
                    f"- `{file['command']}`: `{file['source']}` -> `{file['destination'] or 'N/A'}`\n"
                )
                if file["docstring"]:
                    md_file.write(f"  - {file['docstring']}\n")
        else:
            md_file.write("None.")
        md_file.write("\n")

    if verbose:
        print(f"Documentation generated at {output_path}")
