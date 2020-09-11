import random
import string

from model.project import Project
from utils.string_utils import random_string


def test_del_project(app):
    if app.soap.get_project_list() == 0:
        app.project.add_project(Project(name=random_string("pr", 10, string.ascii_letters), description="TESCO"))
    old_list_project = app.soap.get_project_list()
    rnd_project = random.choice(old_list_project)
    app.project.delete_project(rnd_project)
    new_list_project = app.soap.get_project_list()
    old_list_project.remove(rnd_project)
    assert sorted(old_list_project) == sorted(new_list_project)
