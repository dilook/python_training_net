from suds.client import Client

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def get_project_list(self):
        config = self.app.config["webadmin"]
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php?wsdl")
        projects = client.service.mc_projects_get_user_accessible(config["username"], config["password"])
        return list(map(convert_soap_to_model, projects))


def convert_soap_to_model(project):
    return Project(id=project.id, name=project.name, description=project.description)
