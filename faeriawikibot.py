import requests
import urllib.request
import urllib.error
import csv
import resource_dict as r
import gamepedia_generator as gg
import gamepedia_client
import os, sys
import configparser


class Faeriawikibot:
    merlinlist = []
    cardlist = []
    gc = None

    def __init__(self):
        self.merlinlist = []
        self.cardlist = []

    '''
    Parse csv dump of cards into python dictionaries
    '''
    def parse_merlin(self):
        req = requests.get(r.GithubResource.get_merlin_shortened_csv())
        self.merlinlist = []
        #with open('resources/merlin_shortened.csv', 'w') as f:
        #    f.write(req.text)
        with open('resources/merlin_shortened.csv') as f:
            csvreader = csv.DictReader(f,
                                       fieldnames=['card_id', 'card_color', 'card_name', 'card_type', 'gold', 'faeria',
                                                   'lake', 'forest', 'mountain', 'desert', 'power', 'life', 'desc',
                                                   'codex1', 'codex2', 'codex3', 'rarity'], delimiter=';',
                                       quotechar='"')
            for row in csvreader:
                row['rarity'] = self.fix_rarity(row['rarity'])
                self.merlinlist.append(row)
        return self.merlinlist

    def merlin2cardinfo(self, merlinlist=''):
        if merlinlist == '':
            merlinlist = self.merlinlist

        ggen = gg.GamepediaGenerator()

        for mc in merlinlist:
            abilitylist = self.extract_abilities(self.change_desc_actions_to_templates(mc['desc']))
            card = ggen.generate_card(card_id=mc['card_id'],
                                      illustration='{lang}_{card_id}.png'.format(lang='english', card_id=mc['card_id']),
                                      card_color=self.fix_case(mc['card_color']), card_name=mc['card_name'],
                                      card_type=self.fix_case(mc['card_type']), rarity=self.fix_case(mc['rarity']),
                                      gold=mc['gold'], faeria=mc['faeria'], lake=mc['lake'], mountain=mc['mountain'],
                                      desert=mc['desert'], forest=mc['forest'], power=mc['power'], life=mc['life'],
                                      desc=self.change_desc_actions_to_templates(mc['desc']), codex1=mc['codex1'],
                                      codex2=mc['codex2'], codex3=mc['codex3'], ability1=abilitylist[0],
                                      ability2=abilitylist[1], ability3=abilitylist[2], ability4=abilitylist[3],
                                      ability5=abilitylist[4])
            self.cardlist.append(card)
            print(card)
        return self.cardlist

    '''
    Create new instance of GamepediaClient (required for name attribution)
    '''
    def create_gamepedia_client(self, username=None, password=None):
        global cfg_file
        if username is None:
            username = cfg_file['account']['username']
        if password is None:
            password = cfg_file['account']['password']
        self.gc = gamepedia_client.GamepediaClient(username=username, password=password)

    '''
    Update all images from all languages
    '''
    def update_all_images(self):
        self.update_one_language_images('english', r.GithubResource.get_card_english)
        self.update_one_language_images('french', r.GithubResource.get_card_french)
        self.update_one_language_images('german', r.GithubResource.get_card_german)
        self.update_one_language_images('portuguese', r.GithubResource.get_card_portuguese)
        self.update_one_language_images('russian', r.GithubResource.get_card_russian)
        self.update_one_language_images('spanish', r.GithubResource.get_card_spanish)

    '''
    Update all images from one language
    '''
    def update_one_language_images(self, language, resource):
        if self.gc is None:
            self.create_gamepedia_client()
        for card in self.merlinlist:
            try:
                with urllib.request.urlopen(resource(id=card['card_id'])) as resp, open(
                        'resources/{lang}_cards/{id}.png'.format(lang=language, id=card['card_id']), 'wb') as f:
                    data = resp.read()
                    f.write(data)
                self.gc.upload_images('resources/{lang}_cards/{id}.png'.format(lang=language, id=card['card_id']),
                                      '{lang}_{card_id}.png'.format(lang=language, card_id=card['card_id']),
                                      card['card_name'])
            except urllib.error.HTTPError as e:
                print('{message}'.format(e.msg))

    '''
    Create action templates (Template:Haste, Template:Charge, etc)
    '''
    def create_action_templates(self):
        if self.gc is None:
            self.create_gamepedia_client()
        self.gc.create_action_templates()

    '''
    Update cards
    '''
    def update_cards(self):
        if self.gc is None:
            self.create_gamepedia_client()
        for x in range(0, len(self.merlinlist) - 1):
            self.gc.submit_card(self.merlinlist[x], self.cardlist[x])

    '''
    Add one '{'/'}' to each '{'/'}' to make gamepedia link to the templates
    '''
    @staticmethod
    def change_desc_actions_to_templates(desc):
        return str(desc).replace('{', '{{').replace('}', '}}')

    '''
    Extract abilities from card description.
    This is useful for creating associations to the corresponding 'List of cards with X ability/effect'
    '''
    @staticmethod
    def extract_abilities(desc):
        actions = [['ranged_attack', 'Ranged'], ['charge', 'Charge'], ['gift', 'Gift'], ['production', 'Production'],
                   ['combat', 'Combat'], ['protection', 'Protection'], ['taunt', 'Taunt'], ['haste', 'Haste'],
                   ['last_words', 'Last Words'], ['deathtouch', 'Deathtouch'], ['aquatic', 'Aquatic'], ['jump', 'Jump'],
                   ['flying', 'Flying'], ['activate', 'Activate'], ['options', 'Choose one:'], ['faeria', 'Faeria']]
        result = ['', '', '', '', '']
        if len(desc) > 0:
            for action in actions:
                if ('{{' + action[0]) in str(desc) and action[0] not in result:
                    for i in range(0, len(result) - 1):
                        if result[i] == '':
                            result[i] = action[0]
                            break
        return result

    '''
    Change strings to be capitalized.

    '''

    @staticmethod
    def fix_case(string):
        if string is None:
            return
        if len(string) > 0:
            return str(string).capitalize()

    '''
    Fix rarity
    Rare (Pink) got renamed to Epic
    Exceptional (Blue) got renamed to Rare
    Changes were only visual and not in the datasets, so I need to adjust them here.
    '''
    @staticmethod
    def fix_rarity(string):
        if string == 'RARE':
            return 'EPIC'
        elif string == 'EXCEPTIONAL':
            return 'RARE'
        else:
            return string


if __name__ == '__main__':
    global cfg_file
    cfg_file = configparser.ConfigParser()
    path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
    path_to_cfg = os.path.join(path_to_cfg, 'faeriawikibot.conf')
    cfg_file.read(path_to_cfg)

    fwb = Faeriawikibot()
    fwb.parse_merlin()
    fwb.merlin2cardinfo()
    fwb.update_cards()
    # fwb.update_all_images()
