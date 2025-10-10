from typing import Dict, List
from .mounts import extract_mounts
from .ports import extract_exposed_ports


def extract_dockerfile_details(dockerfile_path: str) -> Dict[str, List[str]]:
    """
    Extracts ARG, ENV, mounts, and ports from the Dockerfile.
    """
    details = {"args": [], "envs": [], "mounts": [], "ports": []}

    # Extract from Dockerfile
    with open(dockerfile_path, "r") as file:
        for line in file:
            stripped = line.strip()
            if stripped.startswith("ARG"):
                arg = stripped.split(" ")[1].split("=")[0].strip()
                details["args"].append(arg)
            elif stripped.startswith("ENV"):
                env = stripped.split(" ")[1].split("=")[0].strip()
                details["envs"].append(env)

    # Extract mounts and ports separately
    details["mounts"] = extract_mounts(dockerfile_path)
    details["ports"] = extract_exposed_ports(dockerfile_path)  # FIX!

    return details


def generate_docker_build_markdown(
    details: Dict[str, List[str]], image_name: str = "my-image", version: str = "1.0.0"
) -> str:
    """
    Generates a markdown block with the Docker build command.
    """
    tag = f"{image_name}:{version}"

    # Build args
    build_args = " \\\n    ".join(
        [f'--build-arg {arg}="${{{arg}}}"' for arg in details["args"]]
    )

    # Port mapping (EXPOSE)
    ports = " \\\n    ".join(
        [
            f'-p {port["port"]}:{port["port"]}'
            for port in details["ports"]
            if "port" in port
        ]
    )

    # Separate handling for secrets vs mounts
    secrets = []
    mounts = []
    for mount in details["mounts"]:
        if mount["type"] == "secret" and "id" in mount:
            secrets.append(f'--secret id={mount["id"]}')
        elif "type" in mount and "dst" in mount:  # Ensure "dst" exists
            source = mount.get("src", "")  # Use empty string if "src" is missing
            mounts.append(
                f'--mount type={mount["type"]},source={source},target={mount["dst"]}'
            )

    # Join secrets and mounts
    secret_flags = " \\\n    ".join(secrets)
    mount_flags = " \\\n    ".join(mounts)

    # Combine everything in the correct order
    docker_command = (
        "```bash\n"
        f'tag="{tag}"\n'
        "docker build -f Dockerfile \\\n"
        + " \\\n    ".join(
            [
                x
                for x in [ports, secret_flags, mount_flags, build_args]
                if x  # Avoid adding empty lines
            ]
        )
        + " \\\n    .\n"
        "```\n"
    )

    return docker_command
