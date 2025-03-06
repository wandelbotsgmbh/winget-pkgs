
import os
import yaml
import sys


def add_entry_to_manifests(installer_hash: str, version: str):
    outpath = f"../manifests/w/WandelbotsGmbH/NovaCLI/{version}"
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    # Configure YAML dumper to avoid quotes for strings
    yaml.SafeDumper.add_representer(
        str,
        lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style=None)
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
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python 02-create-entry.py <version> <hash>")
        sys.exit(1)
    
    version = sys.argv[1]
    installer_hash = sys.argv[2]
    add_entry_to_manifests(installer_hash, version)