import mwclient
import datetime


class GamepediaClient:
    mwc = None

    '''
    Login on creation
    '''

    def __init__(self, url='faeria.gamepedia.com', username=None, password=None):
        self.mwc = mwclient.Site(url, path='/')
        if username is not None and password is not None:
            self.mwc.login(username, password)

    '''
    Login to edit pages and get attribution
    '''

    def login(self, username, password):
        self.mwc.login(username, password)

    '''
    Return the text content of a page
    '''

    def read(self, pagename):
        return self.mwc.Pages[pagename].text()

    '''
    Overwrite whole page with text
    '''

    def write(self, pagename, text):
        page = self.mwc.Pages[pagename]
        page.save(text)

    '''
    Create action template which later link to tags in the card description.
    '''

    def create_action_templates(self):
        actions = [['ranged_attack', 'Ranged'], ['charge', 'Charge'], ['gift', 'Gift'], ['production', 'Production'],
                   ['combat', 'Combat'], ['protector', 'Protection'], ['taunt', 'Taunt'], ['haste', 'Haste'],
                   ['last_words', 'Last Words'], ['deathtouch', 'Deathtouch'], ['aquatic', 'Aquatic'], ['jump', 'Jump'],
                   ['flying', 'Flying'], ['activate', 'Activate'], ['options', 'Choose one:'], ['faeria', 'Faeria'], ['random', 'random']]
        for action in actions:
            page = self.mwc.Pages['Template:{0}'.format(action[0])]
            if page.text() == '':
                page.save('[[' + action[0] + '|' + action[1] + ' {{#if: {{{1|}}}|{{{1|}}} }}]]',
                          summary='Initialized with default configuration')

    '''
    Upload local image to wiki
    '''

    def upload_images(self, imagename, destination, description):
        self.mwc.upload(open(imagename, 'rb'), destination, description)

    '''
    Create/Update card on wiki
    Move conflicting old cards to '/{old card name}_(Historical)'
    '''

    def submit_card(self, mc, card):
        page = self.mwc.Pages[mc['card_name']]
        text = page.text()
        if '{{Card infobox' in text:
            page = self.mwc.Pages[mc['card_name'] + ' (Historical)']
            page.save('{{historical content}}\n' + text)

        page = self.mwc.Pages[mc['card_name']]
        if '{{Card stats' in text:
            try:
                uc = self.update_card(text, card)
                page.save(uc)
            except ValueError as e:
                print('ValueError on \n{text}'.format(text=text))
        else:
            page.save(card)

    '''
    Select and replace (=> update) the 'Card stats' template instance
    '''

    def update_card(self, text, card):
        if '== Changelog ==' not in text:
            text += '\n\n== Changelog ==\n{{changelog\n|height = 200\n|content = {{empty|DO NOT REMOVE OR EDIT THIS OTHERWISE CHANGELOG UPDATE BREAKS}}\n}}'
        start, end = self.textregion_selector(text, '{{Card stats', '{', '}')
        oldtext = text[start:end + 1]
        olddict = self.card2dict(oldtext)
        newdict = self.card2dict(card)
        changelog = '{{empty|DO NOT REMOVE OR EDIT THIS OTHERWISE CHANGELOG UPDATE BREAKS}}\n{{patch|' + str(
            datetime.date.today().isocalendar()[0]) + '|' + str(datetime.date.today().isocalendar()[1]) + '}}:\n'
        if olddict != newdict:
            for key in olddict.keys():
                try:
                    if olddict[key] != newdict[key]:
                        changelog += self.generate_changelogitem(key, olddict[key], newdict[key])
                except KeyError:
                    pass
            return str(text).replace(oldtext, card).replace(
               '{{empty|DO NOT REMOVE OR EDIT THIS OTHERWISE CHANGELOG UPDATE BREAKS}}', changelog)
        return str(text).replace(oldtext, card)

    def generate_changelogitem(self, key, oldvalue, newvalue):
        changelogitem = '* {key} changed from "{old}" to "{new}"\n'
        if key == 'card_color':
            return '* {{cl_color|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'card_name':
            return '* {{cl_name|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'card_type':
            return '* {{cl_type|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'rarity':
            return '* {{cl_rarity|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'faeria':
            return '* {{cl_faeria|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'lake':
            return '* {{cl_lake|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'desert':
            return '* {{cl_desert|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'mountain':
            return '* {{cl_mountain|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'forest':
            return '* {{cl_forest|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'power':
            return '* {{cl_power|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'life':
            return '* {{cl_life|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'desc':
            return '* {{cl_desc|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'codexcode1':
            return '* {{cl_codexcode1|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'codexcode2':
            return '* {{cl_codexcode2|' + oldvalue + '|' + newvalue + '}}'
        elif key == 'codexcode3':
            return '* {{cl_codexcode3|' + oldvalue + '|' + newvalue + '}}'
        elif key not in ['ability1', 'ability2', 'ability3', 'ability4', 'ability5', 'illustration']:
            return '* {{cl_unknown|' + oldvalue + '|' + newvalue + '}}'

    def card2dict(self, card):
        cardsplit = card.split('\n')
        carddict = {}
        for line in cardsplit:
            try:
                key, value = line.split('=', 1)
                key = key.split('|')[1]
                key = key.strip()
                value = value.strip()
                carddict[key] = value
            except ValueError:
                pass
        return carddict

    '''
    Select region of the 'Card stats' template which should get replaced with the updated card
    '''

    @staticmethod
    def textregion_selector(text, starttext, increase, decrease):
        text = str(text)
        startmarker = text.find(starttext)
        level = 0
        for x in range(startmarker, len(text)):
            if text[x] == increase:
                level += 1
            elif text[x] == decrease:
                level -= 1
                if level == 0:
                    return startmarker, x

        raise ValueError
