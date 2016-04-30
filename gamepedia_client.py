import mwclient


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
    Return the text content of a site
    '''

    def read(self, pagename):
        return self.mwc.Pages[pagename].text()

    '''
    Create action template which later link to tags in the card description.
    '''

    def create_action_templates(self):
        actions = [['ranged_attack', 'Ranged'], ['charge', 'Charge'], ['gift', 'Gift'], ['production', 'Production'],
                   ['combat', 'Combat'], ['protector', 'Protection'], ['taunt', 'Taunt'], ['haste', 'Haste'],
                   ['last_words', 'Last Words'], ['deathtouch', 'Deathtouch'], ['aquatic', 'Aquatic'], ['jump', 'Jump'],
                   ['flying', 'Flying'], ['activate', 'Activate'], ['options', 'Choose one:'], ['faeria', 'Faeria']]
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
        start, end = self.textregion_selector(text, '{{Card stats', '{', '}')
        return str(text).replace(text[start:end + 1], card)

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
