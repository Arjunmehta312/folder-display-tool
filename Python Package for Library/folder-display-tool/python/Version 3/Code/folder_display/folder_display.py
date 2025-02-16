import os
from typing import List, Optional, Set
from .exporters import HTMLExporter, JSONExporter, TextExporter

class FolderDisplay:
    def __init__(self):
        self.excluded_folders: Set[str] = set()
        self.include_hidden: bool = False
        
    def set_excluded_folders(self, folders: List[str]) -> None:
        """Set folders to exclude from display"""
        self.excluded_folders = set(folders)
    
    def set_include_hidden(self, include: bool) -> None:
        """Set whether to include hidden files and folders"""
        self.include_hidden = include
    
    def get_structure(self, path: str) -> dict:
        """Get folder structure as a dictionary"""
        structure = {}
        
        for item in os.listdir(path):
            # Skip hidden files if not included
            if not self.include_hidden and item.startswith('.'):
                continue
                
            # Skip excluded folders
            if item in self.excluded_folders:
                continue
                
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                structure[item] = self.get_structure(full_path)
            else:
                structure[item] = None
                
        return structure
    
    def display(self, path: str, indent: str = "    ") -> str:
        """Display folder structure as formatted string"""
        structure = self.get_structure(path)
        return self._format_structure(structure, indent)
    
    def _format_structure(self, structure: dict, indent: str, level: int = 0) -> str:
        """Format structure dictionary as string with proper indentation"""
        output = []
        for name, contents in structure.items():
            output.append(indent * level + "├── " + name)
            if contents:  # If it's a directory
                output.append(self._format_structure(contents, indent, level + 1))
        return "\n".join(output)
    
    def export_html(self, path: str, output_file: str) -> None:
        """Export structure as HTML"""
        structure = self.get_structure(path)
        HTMLExporter.export(structure, output_file)
    
    def export_json(self, path: str, output_file: str) -> None:
        """Export structure as JSON"""
        structure = self.get_structure(path)
        JSONExporter.export(structure, output_file)
    
    def export_text(self, path: str, output_file: str) -> None:
        """Export structure as text file"""
        structure = self.get_structure(path)
        TextExporter.export(structure, output_file) 