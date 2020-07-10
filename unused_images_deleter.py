from time import sleep
from credentials import username, password
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui


class Uploader:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = ui.WebDriverWait(self.driver, 20)

    def login(self, username, password):
        self.driver.get(
            "https://www.wikia.com/signin?redirect=http%3A%2F%2Fmagireco.wikia.com%2Fwiki%2FSpecial%3AImages&modal=1&forceLogin=0")
        elem = self.driver.find_element_by_id("loginUsername")
        elem.send_keys(username)
        elem = self.driver.find_element_by_id("loginPassword")
        elem.send_keys(password)
        sleep(.5)
        elem.submit()
        sleep(1)

    def deleter(self):
        self.driver.get("https://magireco.wikia.com/wiki/Special:UnusedVideos?limit=500&offset=0")
        elems = self.driver.find_elements_by_class_name("gallerytext")
        urls = []
        for elem in elems:
            urls.append(elem.find_element_by_css_selector("a").get_attribute("href"))
        for url in urls:
            self.driver.get(url + "?action=delete")
            try:
                self.driver.find_element_by_id("mw-filedelete-submit").click()
            except NoSuchElementException:
                pass

    def deleter2(self):
        self.driver.get("https://magireco.wikia.com/wiki/Special:UnusedTemplates?limit=500&offset=0")
        elems = self.driver.find_elements_by_class_name("special")
        urls = []
        for elem in elems:
            urls.append(elem.find_element_by_css_selector("a").get_attribute("href"))
        for url in urls:
            self.driver.get(url + "?action=delete")
            try:
                self.driver.find_element_by_id("mw-filedelete-submit").click()
            except NoSuchElementException:
                pass

    def end(self):
        self.driver.close()


if __name__ == '__main__':
    S = Uploader()
    S.login(username, password)
    S.deleter2()
    S.end()
