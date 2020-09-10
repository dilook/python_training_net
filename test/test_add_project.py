from model.project import Project
from utils.string_utils import random_string


def test_add_project(app):
    old_list_project = app.project.get_project_list()
    new_project = Project(name=random_string("project", 10), description="desc")
    app.project.add_project(new_project)
    new_list_project = app.project.get_project_list()
    old_list_project.append(new_project)
    assert sorted(old_list_project, key=lambda x: x.name) == sorted(new_list_project, key=lambda x: x.name)
