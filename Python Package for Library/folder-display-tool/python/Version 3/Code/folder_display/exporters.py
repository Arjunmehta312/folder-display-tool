import json
from typing import Dict

class HTMLExporter:
    @staticmethod
    def export(structure: Dict, output_file: str) -> None:
        html = """
        <html>
        <head>
            <style>
                .tree ul {
                    margin-left: 20px;
                    padding-left: 0;
                }
                .tree li {
                    list-style-type: none;
                    margin: 10px;
                    position: relative;
                }
                .tree li::before {
                    content: "├── ";
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <div class="tree">
        """
        html += HTMLExporter._structure_to_html(structure)
        html += """
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    @staticmethod
    def _structure_to_html(structure: Dict) -> str:
        html = "<ul>"
        for name, contents in structure.items():
            html += f"<li>{name}"
            if contents:  # If it's a directory
                html += HTMLExporter._structure_to_html(contents)
            html += "</li>"
        html += "</ul>"
        return html

class JSONExporter:
    @staticmethod
    def export(structure: Dict, output_file: str) -> None:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2)

class TextExporter:
    @staticmethod
    def export(structure: Dict, output_file: str) -> None:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(TextExporter._structure_to_text(structure))
    
    @staticmethod
    def _structure_to_text(structure: Dict, level: int = 0) -> str:
        text = ""
        indent = "    " * level
        for name, contents in structure.items():
            text += f"{indent}├── {name}\n"
            if contents:  # If it's a directory
                text += TextExporter._structure_to_text(contents, level + 1)
        return text 