from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from os import listdir
from upload_char import Uploader
from credentials import username, password


class ImageUploader(Uploader):
    def upload(self, files, dummy):
        self.driver.get("http://magireco.wikia.com/wiki/Special:MultipleUpload")
        sleep(5)  # Give some time for the html to load, can be modified freely
        for i in range(len(files)):
            self.wait.until(EC.presence_of_element_located((By.ID, "wpUploadFile" + str(i))))
            self.driver.find_element_by_id("wpUploadFile" + str(i)).send_keys(
                "C:/Users/Joachim/Downloads/" + files[i])
        self.driver.execute_script("window.scrollTo(0, 1500);")
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mw-htmlform-submit")))
        self.driver.find_element_by_class_name("mw-htmlform-submit").click()
        sleep(30)  # Give some time for the upload to finish, can be modified freely


def chunks(l):
    for i in range(0, len(l), 20):
        yield l[i:i + 20]


if __name__ == '__main__':
    S = ImageUploader()
    S.login(username, password)
    _files = listdir(r"C:\Users\Joachim\Downloads")
    for sub_files in chunks(_files):
        S.upload(sub_files, None)
    S.end()
