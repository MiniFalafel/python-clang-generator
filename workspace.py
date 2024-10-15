#!/bin/python3

from config_object import ConfObj
from project import ProjectConfig
from stat_paths import Paths

class WorkspaceConfig(ConfObj):
    def __init__(self, workspace: dict):
        super().__init__(workspace, "wks", "Workspace")
        # Set PATHS.WKS_DIR to be equal to the workspace location
        location = self.get_property("location")
        Paths.PATHS["WKS_DIR"] = location
        
        # setup projects
        self.projects = self.__setup_projects()
        
    def get_project(self, proj_name: str) -> ProjectConfig:
        return self.projects[proj_name]
    
    def get_projects(self) -> list[ProjectConfig]:
        return self.projects.values()
    
    def __setup_projects(self):
        # Get names
        project_names = self.get_property("projects")
        # Create ProjectConfig objects and return
        projects = {}
        for name in project_names:
            projects[name] = ProjectConfig(self.get_property(name), name)
        return projects

