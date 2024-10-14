#!/bin/python3

from config_object import ConfObj
from project import ProjectConfig

class WorkspaceConfig(ConfObj):
    def __init__(self, workspace: dict):
        super().__init__(workspace, "Workspace")
        
    def get_project(self, proj_name: str) -> ProjectConfig:
        return ProjectConfig(self.get_property(proj_name))

