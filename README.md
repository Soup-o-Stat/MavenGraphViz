# MavenGraphViz

## What is it?
MavenGraphViz is a cmd tool for visualizing a dependency graph. Dependencies are defined by the name of the Java language package (Maven). The Mermaid representation is used to describe the dependency graph. The visualizer displays the result on the screen in the form of a code.

## Flags
**cmd flags are set:**
- The path to the graph visualization program.
- The name of the package being analyzed.
- The path to the result file in the form of a code.
- URL of the repository

## Example

```
python mavengraphviz.py junit:junit:4.12 output_file.mmd https://repo1.maven.org/maven2
```
or
```
mavengraphviz.py junit:junit:4.12 output_file.mmd https://repo1.maven.org/maven2
```

## Downloading Python packages
You will most likely need to install libraries such as [requests](https://pypi.org/project/requests/) and [termcolor](https://pypi.org/project/termcolor/)

```
pip install requests
```
```
pip install termcolor
```

## If you don't have pip installed
If you don't have pip installed, follow the steps below:

**Download PIP get-pip.py**
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
**Installing PIP on Windows**
```
python get-pip.py
```
**Verify Installation**
```
python -m pip help
```

For more information visit this [site](https://phoenixnap.com/kb/install-pip-windows)
