from pywikibot import family
from pywikibot.tools import deprecated


class Family(family.Family):

    name = 'magireco'
    langs = {
        'en': 'magireco.fandom.com'
    }

    def scriptpath(self, code):
        return ""

    @deprecated('APISite.version()')
    def version(self, code):
        return '1.31.2'

    def protocol(self, code):
        return 'HTTPS'
