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
            projects_list.append(Project(name=name, description=desc))
        return list(projects_list)

    def add_project(self, project):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_create_page.php"):
            self.open_projects_page()
            wd.find_element_by_css_selector("[action='manage_proj_create_page.php']").click()
        wd.find_element_by_id("project-name").send_keys(project.name)
        wd.find_element_by_id("project-description").send_keys(project.description)
        wd.find_element_by_css_selector("input[value='Добавить проект']").click()

    def open_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_page.php"):
            wd.get(self.app.base_url + "/manage_proj_page.php")