import pywikibot as pwb


class Uploader:
    def __init__(self):
        self.site = pwb.Site()
        self.site.login()

    def download_text(self, url):
        return pwb.Page(self.site, url).text

    def download_parsed_page(self, url):
        return pwb.Page(self.site, url).get_parsed_page()

    def upload(self, url, text):
        page = pwb.Page(self.site, url)
        page.text = text
        page.save()


uploader = Uploader()
