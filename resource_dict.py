class GithubResource:
    @staticmethod
    def get_card_english(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/English/{0}.png'.format(str(id).zfill(3))

    @staticmethod
    def get_card_french(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/French/{0}.png'.format(str(id).zfill(3))

    @staticmethod
    def get_card_german(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/German/{0}.png'.format(str(id).zfill(3))

    @staticmethod
    def get_card_portuguese(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/Portuguese/{0}.png'.format(str(id).zfill(3))

    @staticmethod
    def get_card_russian(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/Russian/{0}.png'.format(str(id).zfill(3))

    @staticmethod
    def get_card_spanish(id):
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/Spanish/{0}.png'.format(str(id).zfill(3))

    @staticmethod
    def get_merlin_shortened_csv():
        return 'https://raw.githubusercontent.com/abrakam/Faeria_Cards/master/CardExport/merlin_shortened.csv'
