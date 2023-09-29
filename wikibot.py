import pywikibot as pwb


class WikiBot:
    def __init__(self):
        self.site = pwb.Site()
        self.site.login()

    def download_text(self, url):
        return pwb.Page(self.site, url).text

    def download_parsed_page(self, url):
        return pwb.Page(self.site, url).get_parsed_page()

    def image_usage(self, filename, namespaces=None):
        file = pwb.FilePage(self.site, filename)
        return list(file.using_pages(namespaces=namespaces))

    def upload(self, url, text):
        page = pwb.Page(self.site, url)
        page.text = text
        page.save()


wikibot = WikiBot()
