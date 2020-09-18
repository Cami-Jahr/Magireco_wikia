import selenium.webdriver.support.ui as ui
from time import sleep
from selenium.common.exceptions import TimeoutException
from credentials import username, password
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Uploader:
    def __init__(self):
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        self.driver = webdriver.Chrome(desired_capabilities=capa)
        self.driver.set_page_load_timeout(3)
        self.wait = ui.WebDriverWait(self.driver, 5)

    def click_class(self, _class):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, _class)))
        self.driver.find_element_by_class_name(_class).click()

    def click_id(self, _id):
        self.wait.until(EC.presence_of_element_located((By.ID, _id)))
        self.driver.find_element_by_id(_id).click()

    def login(self, username, password):
        self.driver.get(
            "https://www.fandom.com/signin?redirect=http%3A%2F%2Fmagireco.fandom.com%2Fwiki%2FSpecial%3AImages&modal=1&forceLogin=0")
        self.wait.until(EC.presence_of_element_located((By.ID, "loginUsername")))
        elem = self.driver.find_element_by_id("loginUsername")
        elem.send_keys(username)
        elem = self.driver.find_element_by_id("loginPassword")
        elem.send_keys(password)
        self.driver.find_element_by_class_name("_2o0B8MF50eAK1jv60jldUQ").click()
        sleep(.5)
        elem.submit()
        sleep(60)
        sleep(1)

    def download_text(self, url):
        self.driver.get(
            "http://magireco.fandom.com/wiki/{}?action=edit".format(url.replace("?", "%3F")).replace(" ", "_"))
        sleep(.5)
        self.wait.until(EC.presence_of_element_located((By.ID, "wpTextbox1")))
        return self.driver.find_element_by_id("wpTextbox1").text

    def upload(self, url, text):
        self.driver.get(
            "http://magireco.fandom.com/wiki/{}?action=edit".format(url.replace("?", "%3F")).replace(" ", "_"))
        try:
            sleep(.5)
            self.click_id("template-classification-data")
            self.click_class("primary")
        except TimeoutException:
            pass
        self.wait.until(EC.presence_of_element_located((By.ID, "wpTextbox1")))
        elem = self.driver.find_element_by_id("wpTextbox1")
        if text == elem.text:
            return
        elem.clear()
        elem.send_keys(text)
        self.click_id("wpSave")
        try:
            self.wait.until(lambda driver: driver.find_element_by_id("ca-edit"))
        except TimeoutException:
            pass

    def end(self):
        self.driver.close()

    def trivia_section(self, char):
        text = "{{SideStory\n|Side Story Translation Link = \n|Side Story = \n}}\n\n==Trivia==\n*\n\n{{Videos}}"
        self.upload("/".join([char, "Trivia"]), text)
        self.upload("/".join([char, "Costumes"]), costume_base)
        self.upload("/".join([char, "Gallery"]), galley_base)

    def voice_section(self, char, text):
        self.upload("/".join([char, "Quotes"]), text)

    def upgrades_section(self, char, text):
        self.upload("Template:{}_Items".format(char), text)
        self.upload("{}/Upgrades".format(char), "{{" + """{} Items|Items""".format(char.replace("_", " ")) + "}}")

    def main_section(self, char, stats, text):
        self.upload("Template:" + char, stats)
        self.upload(char,
                    "{{" + char + "}}" + 
                    "\n\n{{Description\n| en = \n| na = \n| jp = " + text + "\n}}\n\n{{Tabs}}")

    def abilities_section(self, char, doppel_story):
        text = "{{" + char + "|Abilities}}"
        if doppel_story:
            text += "\n\n{{Description\n| en = \n| na = \n| jp = " + doppel_story + "\n}}"
        self.upload("/".join([char, "Abilities"]), text)


