import argparse
import requests
import xml.etree.ElementTree as ET
from termcolor import colored, cprint

version="1.0"

def fetch_pom_file(package_name, repository_url):
    group_id, artifact_id, version = package_name.split(":")
    url = f"{repository_url}/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    try:
        response = requests.get(url, timeout=30)
    except:
        pass
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_dependencies(pom_content):
    dependencies = []
    root = ET.fromstring(pom_content)
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    for dependency in root.findall(".//m:dependency", namespaces=ns):
        group_id = dependency.find("m:groupId", namespaces=ns).text
        artifact_id = dependency.find("m:artifactId", namespaces=ns).text
        version_elem = dependency.find("m:version", namespaces=ns)
        version = version_elem.text if version_elem is not None else "unknown"
        dependencies.append(f"{group_id}:{artifact_id}:{version}")
    return dependencies

def get_dependencies(package_name, repository_url, visited=None):
    if visited is None:
        visited = set()
    dependencies = []
    if package_name in visited:
        return dependencies
    visited.add(package_name)
    pom_content = fetch_pom_file(package_name, repository_url)
    if pom_content:
        direct_dependencies = parse_dependencies(pom_content)
        dependencies.extend(direct_dependencies)
        for dep in direct_dependencies:
            dependencies.extend(
                get_dependencies(dep, repository_url, visited))
    return dependencies

def generate_mermaid_code(package_name, dependencies):
    mermaid_code = "graph TD\n"
    mermaid_code += f"    {package_name}\n"
    for dep in dependencies:
        mermaid_code += f"    {package_name} --> {dep}\n"
    return mermaid_code

def ultra_parser(package_name, repository_url, output_file):
    cprint("Processing...", "yellow", attrs=["bold"])
    dependencies = get_dependencies(package_name, repository_url)
    mermaid_code = generate_mermaid_code(package_name, dependencies)
    with open(output_file, 'w') as file:
        file.write(mermaid_code)
    print(mermaid_code)
    cprint("Done!", "green", attrs=["bold"])

def flag_checker():
    parser = argparse.ArgumentParser(description="MavenGraphViz")
    parser.add_argument("package_name")
    parser.add_argument("output_file")
    parser.add_argument("rep_url")
    args = parser.parse_args()
    cprint("Flags has been checked", "green")
    ultra_parser(package_name=args.package_name, repository_url=args.rep_url, output_file=args.output_file)

def main():
    cprint("Created by Soup-o-Stat", 'red')
    print()
    flag_checker()

if __name__ == "__main__":
    main()
