import configparser
import csv
import datetime
import os
import re
import sys
import urllib.error
import urllib.request

import requests

import gamepedia_client
import gamepedia_generator as gg
import resource_dict as r


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
        with open('resources/merlin_shortened.csv', 'w') as f:
            f.write(req.text)
        with open('resources/merlin_shortened.csv') as f:
            csvreader = csv.DictReader(f,
                                       fieldnames=['card_id', 'card_color', 'card_name', 'card_type', 'gold', 'faeria',
                                                   'lake', 'forest', 'mountain', 'desert', 'power', 'life', 'desc',
                                                   'codex1', 'codex2', 'codex3', 'rarity'], delimiter=';',
                                       quotechar='"')
            for row in csvreader:
                row['rarity'] = self.fix_rarity(row['rarity'])
                row['desc'] = self.handle_english_description_links(row['desc'])
                row = self.handle_unupdated_cards(row)
                self.merlinlist.append(row)
        return self.merlinlist

    '''
    Convert dictionary to card-template string
    '''
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
        return self.cardlist

    '''
    Modify special cards to avoid name collision for cards which are played by AI (some have some special effects
    which are not available to the normal player)

    Can also be used to update single cards if the card dump is not updated.
    '''
    @staticmethod
    def handle_unupdated_cards(card):
        if card['card_id'] == '331':
            card['card_name'] = 'Wisdom (Special)'
        if card['card_id'] == '320':
            card['card_name'] = 'Twinsoul Spirit (Special)'
        return card

    '''
    Create new instance of GamepediaClient (required for name attribution and editing permissions)
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
        # self.update_one_language_images('french', r.GithubResource.get_card_french)
        # self.update_one_language_images('german', r.GithubResource.get_card_german)
        # self.update_one_language_images('portuguese', r.GithubResource.get_card_portuguese)
        # self.update_one_language_images('russian', r.GithubResource.get_card_russian)
        # self.update_one_language_images('spanish', r.GithubResource.get_card_spanish)

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
                                      card['card_name'], True)
            except urllib.error.HTTPError as e:
                print('{message}'.format(e.msg))

    '''
    Create action templates (Template:Haste, Template:Charge, etc)
    '''
    def create_action_templates(self):
        if self.gc is None:
            self.create_gamepedia_client()
        actions = [['ranged_attack', 'Ranged'], ['charge', 'Charge'], ['gift', 'Gift'], ['production', 'Production'],
                   ['combat', 'Combat'], ['protector', 'Protection'], ['taunt', 'Taunt'], ['haste', 'Haste'],
                   ['last_words', 'Last Words'], ['deathtouch', 'Deathtouch'], ['aquatic', 'Aquatic'], ['jump', 'Jump'],
                   ['flying', 'Flying'], ['activate', 'Activate'], ['options', 'Choose one:'], ['faeria', 'Faeria'],
                   ['random', 'random']]
        for action in actions:
            page = self.gc.read('Template:{0}'.format(action[0]))
            if page.text() == '':
                page.save('[[' + action[0] + '|' + action[1] + ' {{#if: {{{1|}}}|{{{1|}}} }}]]',
                          summary='Initialized with default configuration')

    '''
    Create/Update card on wiki
    Move conflicting old cards to '/{old card name}_(Historical)'
    '''
    def update_cards(self):
        if self.gc is None:
            self.create_gamepedia_client()
        for x in range(0, len(self.merlinlist) - 1):
            mc = self.merlinlist[x]
            card = self.cardlist[x]
            page = self.gc.read(mc['card_name'])
            text = page.text()
            if '{{Card infobox' in text:
                page = self.gc.read(mc['card_name'] + ' (Historical)')
                page.save('{{historical content}}\n' + text)

            page = self.gc.read(mc['card_name'])
            if '{{Card stats' in text:
                try:
                    uc = self.update_card(text, card)
                    page.save(uc)
                except ValueError:
                    print('ValueError on \n{text}'.format(text=text))
            else:
                page.save(card)

    '''
    Select and replace (=> update) the 'Card stats' template instance
    '''
    def update_card(self, text, card):
        if '== Changelog ==' not in text:
            text += '\n\n== Changelog ==\n{{changelog\n|height = 200\n|content = {{empty|DO NOT REMOVE OR EDIT THIS \
                    OTHERWISE CHANGELOG UPDATE BREAKS}}\n}}'
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
            print('******************')
            print(olddict['card_name'])
            print(changelog)
            return str(text).replace(oldtext, card).replace(
                '{{empty|DO NOT REMOVE OR EDIT THIS OTHERWISE CHANGELOG UPDATE BREAKS}}', changelog)
        return str(text).replace(oldtext, card)

    '''
    Generate changelog text based on attribute name
    '''
    @staticmethod
    def generate_changelogitem(key, oldvalue, newvalue):
        if oldvalue is None:
            oldvalue = ''
        if newvalue is None:
            newvalue = ''
        # changelogitem = '* {key} changed from "{old}" to "{new}"\n'
        if key == 'card_color':
            return '* {{cl_color|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'card_name':
            return '* {{cl_name|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'card_type':
            return '* {{cl_type|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'rarity':
            return '* {{cl_rarity|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'faeria':
            return '* {{cl_faeria|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'lake':
            return '* {{cl_lake|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'desert':
            return '* {{cl_desert|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'mountain':
            return '* {{cl_mountain|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'forest':
            return '* {{cl_forest|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'power':
            return '* {{cl_power|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'life':
            return '* {{cl_life|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'desc':
            return '* {{cl_desc|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'codexcode1':
            return '* {{cl_codexcode1|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'codexcode2':
            return '* {{cl_codexcode2|' + oldvalue + '|' + newvalue + '}}\n'
        elif key == 'codexcode3':
            return '* {{cl_codexcode3|' + oldvalue + '|' + newvalue + '}}\n'
        elif key not in ['ability1', 'ability2', 'ability3', 'ability4', 'ability5', 'illustration']:
            return '* {{cl_unknown|' + oldvalue + '|' + newvalue + '}}\n'
        else:
            return ''

    '''
    Converts a card from card-template form to dictionary
    '''
    @staticmethod
    def card2dict(card):
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

    '''
    Add one '{'/'}' to each '{'/'}' to make gamepedia link to the templates
    Change <b> </b> to [[ ]]
    Makes the word random an ability by changing random to {{random}}
    '''
    @staticmethod
    def change_desc_actions_to_templates(desc):
        desc = str(desc).replace('random', '{random}')
        return str(desc).replace('{', '{{').replace('}', '}}')

    '''
    Replaces referenced cards in description with actual mediawiki links
    '''
    @staticmethod
    def handle_english_description_links(description):
        resultlist = re.findall('<b>.*?</b>', description)
        for result in resultlist:
            extract = re.search('<b>(?P<extract>.*?)</b>', result).group('extract')
            try:
                replacement = r.DescriptionLinksResource.get_english_card_link(extract)
            except ValueError:
                continue
            description = description.replace(result, '[[{link}|{visual}]]'.format(link=replacement, visual=extract))
        return description

    '''
    Extract abilities from card description.
    This is useful for creating associations to the corresponding 'List of cards with X ability/effect'
    '''
    @staticmethod
    def extract_abilities(desc):
        actions = [['ranged_attack', 'Ranged'], ['charge', 'Charge'], ['gift', 'Gift'], ['production', 'Production'],
                   ['combat', 'Combat'], ['protection', 'Protection'], ['taunt', 'Taunt'], ['haste', 'Haste'],
                   ['last_words', 'Last Words'], ['deathtouch', 'Deathtouch'], ['aquatic', 'Aquatic'], ['jump', 'Jump'],
                   ['flying', 'Flying'], ['activate', 'Activate'], ['options', 'Choose one:'], ['faeria', 'Faeria'],
                   ['random', 'random']]
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
    # fwb.update_cards()
    fwb.update_all_images()
