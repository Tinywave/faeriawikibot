class GithubResource:
    @staticmethod
    def get_card_english(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/English/{0}.png'.format(
            str(id).zfill(3))

    @staticmethod
    def get_card_french(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/French/{0}.png'.format(
            str(id).zfill(3))

    @staticmethod
    def get_card_german(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/German/{0}.png'.format(
            str(id).zfill(3))

    @staticmethod
    def get_card_portuguese(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/Portuguese/{0}.png'.format(
            str(id).zfill(3))

    @staticmethod
    def get_card_russian(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/Russian/{0}.png'.format(
            str(id).zfill(3))

    @staticmethod
    def get_card_spanish(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/Spanish/{0}.png'.format(
            str(id).zfill(3))

    @staticmethod
    def get_merlin_shortened_csv():
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/merlin_shortened.csv'


class GamepediaResource:
    @property
    def get_wiki(self):
        return 'faeria.gamepedia.com'

    @property
    def get_english_wiki(self):
        return 'faeria.gamepedia.com'

    @property
    def get_french_wiki(self):
        return 'faeria-fr.gamepedia.com'

    @property
    def get_german_wiki(self):
        return 'faeria-de.gamepedia.com'

    @property
    def get_portuguese_wiki(self):
        return 'faeria-pt.gamepedia.com'

    @property
    def get_russian_wiki(self):
        return 'faeri-ru.gamepedia.com'

    @property
    def get_spanish_wiki(self):
        return 'faeria-es.gamepedia.com'


class DescriptionLinksResource:
    @staticmethod
    def get_english_card_link(searchterm):
        links = {
            'Imperial Guards': 'Imperial Guard',
            'Angry Yaks': 'Angry Yak',
            'Safeguard': 'Safeguard',
            'Punishment': 'Punishment',
            'Campfire': 'Campfire',
            'Mirror Phantasm': 'Mirror Phantasm',
            'Triton Banquet': 'Triton Banquet',
            'Frog': 'Frog',
            'Ruby Fish': 'Ruby Fish',
            'Frogs': 'Frog',
            "Khalim's Follower": "Khalim's Follower",
            'Slaughtering Shadow': 'Slaughtering Shadow',
            'Demon Wing': 'Demon Wing',
            'Oblivion Knight': 'Oblivion Knight'
        }
        if searchterm in links.keys():
            return links[searchterm]
        else:
            raise ValueError
