import os
import re
import sys

import yaml


def add_entry_to_manifests(installer_hash: str, version: str):
    outpath = f"../manifests/w/WandelbotsGmbH/NovaCLI/{version}"
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    # Configure YAML dumper to avoid quotes for strings
    yaml.SafeDumper.add_representer(
        str,
        lambda dumper, data: dumper.represent_scalar(
            "tag:yaml.org,2002:str", data, style=None
        ),
    )

    installer_url = f"https://github.com/wandelbotsgmbh/nova-cli/releases/download/{version}/novacli_win64-{version}.zip"
    installer_name = "WandelbotsGmbH.NovaCLI.installer.yaml"
    local_name = "WandelbotsGmbH.NovaCLI.locale.en-US.yaml"
    package_name = "WandelbotsGmbH.NovaCLI.yaml"

    with open(f"templates/{installer_name}", "r") as f:
        data = yaml.safe_load(f)
        data["Installers"][0]["InstallerSha256"] = installer_hash
        data["Installers"][0]["InstallerUrl"] = installer_url
        data["PackageVersion"] = version
        with open(f"{outpath}/{installer_name}", "x") as fy:
            fy.write(yaml.dump(data))

    with open(f"templates/{local_name}", "r") as f:
        data = yaml.safe_load(f)
        data["PackageVersion"] = version
        with open(f"{outpath}/{local_name}", "x") as fy:
            fy.write(yaml.dump(data))

    with open(f"templates/{package_name}", "r") as f:
        data = yaml.safe_load(f)
        data["PackageVersion"] = version
        with open(f"{outpath}/{package_name}", "x") as fy:
            fy.write(yaml.dump(data))

    merge_manifests(outpath)


def merge_manifests(path: str):
    for root, _, files in os.walk(path):
        if re.match(".*(?:[0-9]+\\.?){2,3}\\.[0-9]+$", root):
            merged_data = {}
            for file in files:
                if file.endswith(".yaml"):
                    filename = os.path.join(root, file)
                    with open(filename, "r") as stream:
                        try:
                            data = yaml.safe_load(stream)
                            if data:
                                # merges the data
                                merged_data = merged_data.copy()
                                merged_data.update(data)
                        except yaml.YAMLError as exc:
                            print(exc)
                            break
            merged_data["ManifestType"] = "merged"
            merged_name = "264a-" + merged_data["PackageIdentifier"] + ".yaml"
            output_file = os.path.join(root, merged_name)

            with open(output_file, "w") as f:
                f.write(yaml.dump(merged_data))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python 02-create-entry.py <version> <hash>")
        sys.exit(1)

    version = sys.argv[1]
    installer_hash = sys.argv[2]
    add_entry_to_manifests(installer_hash, version)
