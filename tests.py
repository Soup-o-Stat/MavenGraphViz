import unittest
from unittest.mock import patch, MagicMock
import mavengraphviz

class TestMavenGraphViz(unittest.TestCase):

	def test_fetch_pom_file(self):
		with patch("mavengraphviz.requests.get") as mock_get:
			mock_response = MagicMock()
			mock_response.status_code = 200
			mock_response.text = "<project>...</project>"
			mock_get.return_value = mock_response

			content = mavengraphviz.fetch_pom_file("com.example:demo:1.0", "https://repo.maven.apache.org/maven2")
			self.assertIsNotNone(content)
			mock_get.assert_called_once()

	def test_parse_dependencies(self):
		pom_content = '''
		<project xmlns="http://maven.apache.org/POM/4.0.0">
			<dependencies>
				<dependency>
					<groupId>com.example</groupId>
					<artifactId>example-lib</artifactId>
					<version>1.0</version>
				</dependency>
			</dependencies>
		</project>
		'''
		dependencies = mavengraphviz.parse_dependencies(pom_content)
		self.assertEqual(dependencies, ["com.example:example-lib:1.0"])

	def test_get_dependencies(self):
		with patch("mavengraphviz.fetch_pom_file") as mock_fetch:
			mock_fetch.side_effect = [
				"<project>...</project>",
				"<project>...</project>"
			]
			dependencies = mavengraphviz.get_dependencies("com.example:demo:1.0", "https://repo.maven.apache.org/maven2")
			self.assertIsInstance(dependencies, list)

	def test_generate_mermaid_code(self):
		package_name = "com.example:demo:1.0"
		dependencies = ["com.example:example-lib:1.0"]
		mermaid_code = mavengraphviz.generate_mermaid_code(package_name, dependencies)
		self.assertIn("com.example:demo:1.0 --> com.example:example-lib:1.0", mermaid_code)

	def test_ultra_parser(self):
		with patch("mavengraphviz.get_dependencies", return_value=["com.example:example-lib:1.0"]):
			with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
				mavengraphviz.ultra_parser("com.example:demo:1.0", "https://repo.maven.apache.org/maven2", "output.md")
				mock_file.assert_called_once_with("output.md", 'w')
				mock_file().write.assert_called()

if __name__ == '__main__':
	unittest.main()
