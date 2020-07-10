import read_awaken_mats as awaken
import read_voice_text as voice
import read_trivia as story
import read_stats
import selenium.webdriver.support.ui as ui
from time import sleep
from selenium.common.exceptions import TimeoutException
from credentials import username, password
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from helpers import get_filenames, get_char_list

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

    def voice_section(self, char, text):
        self.upload("/".join([char, "Quotes"]), text)

    def upgrades_section(self, char, text):
        self.upload("Template:{}_Items".format(char), text)
        self.upload("{}/Upgrades".format(char),
                    "{{" + """{} Items|Items""".format(char.replace("_", " ")) + "}}")

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


if __name__ == '__main__':
    #S = Uploader()
    #S.login(username, password)
    up_chars = [
        1014, 3043, 1007
    ]
    #files = get_filenames()
    #print(files.__class__, len(files))
    # print("1-----", files[111])

    chars = get_char_list()
    #print(chars.__class__, len(chars))
    #print("2-----", chars[1001])

    #mat_list = awaken.read_mats_json()
    #print(mat_list.__class__)
    #print("3-----")

    #formated_mats = awaken.mats_formater(mat_list, files, chars)
    #print(formated_mats.__class__)
    #print("4-----", formated_mats[1001])

    #voice_lines = voice.read_lines_json()
    #print(voice_lines.__class__, len(voice_lines))
    #print("5-----")

    #formated_voice = voice.mats_sender(voice_lines)
    #print(formated_voice.__class__, len(formated_voice))
    #print("6-----", formated_voice[1001])
    
    #trivia = story.read_trivia_json()
    #print(trivia.__class__)
    #print("7-----", trivia[1001])

    #formated_trivia = story.story_formater(trivia)
    #print(formated_trivia.__class__)
    #print("8-----", formated_trivia[1001])

    for i in list(chars):
        s = chars[i].replace(" ", "_")
        print(i, chars[i], f"https://magireco.fandom.com/wiki/Template:{s}?action=edit")
        out = read_stats.format_info(i)
        #print(out)
        with open(f"stats/{s}.txt", "w", encoding="utf-8-sig") as f:
            f.write(out)
    """
    for _id in up_chars:
        S.main_section(chars[_id], read_stats.format_info(_id), formated_trivia[_id][0])
        S.upgrades_section(chars[_id], formated_mats[_id])
        S.trivia_section(chars[_id])
        S.voice_section(chars[_id], formated_voice[_id])
        S.abilities_section(chars[_id], formated_trivia[_id][1])
        print(_id, "done")
    S.end()
    """