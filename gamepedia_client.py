import mwclient

class GamepediaClient:
    mwc = None

    def __init__(self, username=None, password=None):
        self.mwc = mwclient.Site('faeria.gamepedia.com', path='/')
        if username is not None and password is not None:
            self.mwc.login(username, password)

    def login(self, username, password):
        self.mwc.login(username, password)

    def create_action_templates(self):
        actions = [['ranged_attack', 'Ranged'], ['charge','Charge'], ['gift','Gift'], ['production','Production'], ['combat','Combat'], ['protector','Protection'], ['taunt','Taunt'], ['haste','Haste'], ['last_words','Last Words'], ['deathtouch','Deathtouch'], ['aquatic','Aquatic'], ['jump','Jump'], ['flying','Flying'], ['activate','Activate'], ['options','Choose one:'], ['faeria','Faeria']]
        for action in actions:
            page = self.mwc.Pages['Template:{0}'.format(action[0])]
            if page.text() == '':
                page.save('[[' + action[0] + '|' + action[1] + ' {{#if: {{{1|}}}|{{{1|}}} }}]]', summary='Initialized with default configuration')

    def upload_images(self, imagename, destination, description):
        self.mwc.upload(open(imagename, 'rb'), destination, description)

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

    def update_card(self, text, card):
        start, end = self.textregion_selector(text, '{{Card stats', '{', '}')
        return str(text).replace(text[start:end+1], card)


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


