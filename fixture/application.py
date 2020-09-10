from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager

from fixture.project import ProjectHelper
from fixture.session import SessionHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif browser == "chrome":
            self.wd = webdriver.Chrome(ChromeDriverManager().install())
        elif browser == "ie":
            self.wd = webdriver.Ie(IEDriverManager(os_type="win32").install())
        elif browser == "edge":
            self.wd = webdriver.Edge(EdgeChromiumDriverManager().install())
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(2)
        self.wd.maximize_window()
        self.base_url = base_url
        self.project = ProjectHelper(self)
        self.session = SessionHelper(self)

    def open_home_page(self):
        wd = self.wd
        if "index.php" not in wd.current_url:
            wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False