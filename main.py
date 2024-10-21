import argparse
import requests
import xml.etree.ElementTree as ET

def get_dep(package_name, repository_url):
    parts = package_name.split(":")
    if len(parts) != 3:
        print("Неправильный формат имени пакета. Используйте 'groupId:artifactId:version'.")
        return ""
    group_id, artifact_id, version = parts
    pom_url = f"{repository_url}/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"

    try:
        response = requests.get(pom_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка получения POM: {e}")
        return ""
    print("Содержимое POM-файла:")
    print(response.content.decode("utf-8"))
    dependencies = []
    try:
        root = ET.fromstring(response.content)
        namespace = {'m': 'http://maven.apache.org/POM/4.0.0'}
        for dependency in root.findall(".//m:dependency", namespaces=namespace):
            dep_group_id = dependency.find("m:groupId", namespaces=namespace).text
            dep_artifact_id = dependency.find("m:artifactId", namespaces=namespace).text
            dep_version = dependency.find("m:version", namespaces=namespace).text if dependency.find("m:version", namespaces=namespace) is not None else "unknown"
            dependencies.append(f"{dep_group_id}:{dep_artifact_id}:{dep_version}")
    except ET.ParseError as e:
        print(f"Ошибка парсинга POM: {e}")
        return ""
    print("Найденные зависимости:")
    print(dependencies)
    if not dependencies:
        return "graph TD\n    Нет зависимостей."
    graph = "graph TD\n"
    for dep in dependencies:
        graph += f"    {package_name} --> {dep}\n"
    return graph

def get_args():
    parser = argparse.ArgumentParser(description="MavenGraphViz")
    parser.add_argument("path", help="Path to the program")
    parser.add_argument("package_name", help="Analyzed package name")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("repository_url", help="URL of the repository")
    args = parser.parse_args()
    mermaid_graph = get_dep(args.package_name, args.repository_url)
    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(mermaid_graph)
    print(mermaid_graph)

def main():
    try:
        get_args()
    except Exception as ex:
        print("Error!")
        print(ex)
        exit()

if __name__ == "__main__":
    main()
