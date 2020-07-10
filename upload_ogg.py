from time import sleep
from credentials import username, password
from upload_char import Uploader
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


class ImageUploader(Uploader):
    def upload(self, files, dummy):
        self.driver.get("http://magireco.wikia.com/wiki/Special:MultipleUpload")
        sleep(1)
        for i in range(len(files)):
            self.wait.until(EC.presence_of_element_located((By.ID, "wpUploadFile" + str(i))))
            try:
                self.driver.find_element_by_id("wpUploadFile" + str(i)).send_keys(
                    "D:/OneDrive - NTNU/Private projects/Reverse Engineer/Sound/voice/" + files[i])
            except WebDriverException:
                pass
        self.driver.execute_script("window.scrollTo(0, 1500);")
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mw-htmlform-submit")))
        self.driver.find_element_by_class_name("mw-htmlform-submit").click()
        sleep(20)


def chunks(l):
    for i in range(0, len(l), 20):
        yield l[i:i + 20]


if __name__ == '__main__':
    S = ImageUploader()
    S.login(username, password)
    to_do = [
        (3043, 00, 1, 75),
        (1208, 00, 53, 75),
        (1014, 00, 1, 75),
        (1007, 00, 1, 75),
    ]

    done = []
    files = []
    for char, nr, start, end in to_do:
        files += ["vo_char_{:04}_{:02}_{:02}.ogg".format(char, nr, i) for i in range(start, end + 1)]
    for sub_files in chunks(files):
        S.upload(sub_files, False)
    S.end()
