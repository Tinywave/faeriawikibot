import mwclient

class GamepediaClient:
    mwc = None
    def __init__(self):
        self.mwc = mwclient.Site('faeria.gamepedia.com', path='/')

    def login(self, username, password):
        self.mwc.login(username, password)

    def create_action_templates(self):
        actions = [['ranged_attack', 'Ranged'], ['charge','Charge'], ['gift','Gift'], ['production','Production'], ['combat','Combat'], ['protector','Protection'], ['taunt','Taunt'], ['haste','Haste'], ['last_words','Last Words'], ['deathtouch','Deathtouch'], ['aquatic','Aquatic'], ['jump','Jump'], ['flying','Flying'], ['activate','Activate'], ['options','Choose one:'], ['faeria','Faeria']]
        for action in actions:
            page = self.mwc.Pages['Template:{0}'.format(action[0])]
            page.save('[[' + action[0] + '|' + action[1] + ' {{#if: {{{1|}}}|{{{1|}}} }}]]', summary='Initialized with default configuration')

    def upload_images(self, imagename, destination, description):
        print(imagename)
        print(destination)
        print(description + '\n')
        self.mwc.upload(open(imagename, 'rb'), destination, description)

    def submit_card(self, mc, card):
        page = self.mwc.Pages[mc['card_name']]
        text = page.text()
        if '{{Card infobox' in text:
            page = self.mwc.Pages[mc['card_name'] + ' (Historical)']
            page.save('{{historical content}}\n' + text)
        page = self.mwc.Pages[mc['card_name']]
        page.save(card)
