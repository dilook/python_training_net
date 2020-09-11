import re

from model.project import Project


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def get_project_list(self):
        wd = self.app.wd
        self.open_projects_page()
        project_table = wd.find_element_by_css_selector("table")
        rows = project_table.find_elements_by_tag_name("tbody tr")
        projects_list = []
        for row in rows:
            cells = row.find_elements_by_tag_name("td")
            name = cells[0].text
            desc = cells[4].text
            id_text = cells[0].find_element_by_tag_name("a").get_attribute("href")
            match = re.match(".*project_id=(.*)", id_text)
            id = match.group(1)
            projects_list.append(Project(id=id, name=name, description=desc))
        return list(projects_list)

    def open_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_page.php"):
            wd.get(self.app.base_url + "/manage_proj_page.php")

    def add_project(self, project):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_create_page.php"):
            self.open_projects_page()
            wd.find_element_by_css_selector("[action='manage_proj_create_page.php']").click()
        wd.find_element_by_id("project-name").send_keys(project.name)
        wd.find_element_by_id("project-description").send_keys(project.description)
        wd.find_element_by_css_selector("input[value='Добавить проект']").click()

    def delete_project(self, project):
        wd = self.app.wd
        self.open_projects_page()
        self.edit_project(project)
        wd.find_element_by_css_selector("input[value='Удалить проект']").click()
        wd.find_element_by_css_selector(".alert input[value='Удалить проект']").click()

    def edit_project(self, project):
        wd = self.app.wd
        wd.find_element_by_link_text(project.name).click()
