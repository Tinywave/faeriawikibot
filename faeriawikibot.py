import requests
import urllib.request
import csv
import resource_dict as r
import gamepedia_generator as gg
import gamepedia_client
import pprint


class Faeriawikibot:
    merlinlist = []
    cardlist = []

    def __init__(self):
        self.merlinlist = []

    def parse_merlin(self):
        req = requests.get(r.GithubResource.get_merlin_shortened_csv())
        self.merlinlist = []
        with open('resources/merlin_shortened.csv', 'w') as f:
            f.write(req.text)
        with open('resources/merlin_shortened.csv') as f:
            csvreader = csv.DictReader(f, fieldnames=['card_id', 'card_color', 'card_name', 'card_type', 'gold', 'faeria', 'lake', 'forest', 'mountain', 'desert', 'power', 'life', 'desc', 'codex1', 'codex2', 'codex3', 'rarity'], delimiter=';', quotechar='"')
            for row in csvreader:
                self.merlinlist.append(row)
        return self.merlinlist

    def merlin2cardinfo(self, merlinlist = ''):
        if merlinlist == '':
            merlinlist = self.merlinlist

        ggen = gg.GamepediaGenerator()

        for mc in merlinlist:
            abilitylist = self.extract_abilities(self.change_desc_actions_to_templates(mc['desc']))
            card = ggen.generate_card(card_id=mc['card_id'], illustration='{lang}_{card_id}.png'.format(lang='english',card_id=mc['card_id']), card_color=self.fix_case(mc['card_color']), card_name=mc['card_name'], card_type=self.fix_case(mc['card_type']), rarity=self.fix_case(mc['rarity']), gold=mc['gold'], faeria=mc['faeria'], lake=mc['lake'], mountain=mc['mountain'], desert=mc['desert'], forest=mc['forest'], power=mc['power'], life=mc['life'], desc=self.change_desc_actions_to_templates(mc['desc']), codex1 = mc['codex1'], codex2=mc['codex2'], codex3=mc['codex3'], ability1=abilitylist[0], ability2=abilitylist[1], ability3=abilitylist[2], ability4=abilitylist[3], ability5=abilitylist[4])
            self.cardlist.append(card)
            print(card)
        return self.cardlist

    @staticmethod
    def change_desc_actions_to_templates(desc):
        return str(desc).replace('{','{{').replace('}', '}}')

    @staticmethod
    def extract_abilities(desc):
        actions = [['ranged_attack', 'Ranged'], ['charge','Charge'], ['gift','Gift'], ['production','Production'], ['combat','Combat'], ['protector','Protection'], ['taunt','Taunt'], ['haste','Haste'], ['last_words','Last Words'], ['deathtouch','Deathtouch'], ['aquatic','Aquatic'], ['jump','Jump'], ['flying','Flying'], ['activate','Activate'], ['options','Choose one:'], ['faeria','Faeria']]
        result = ['', '', '', '', '']
        if len(desc) > 0:
            for action in actions:
                if ('{{' + action[0]) in str(desc):
                    if action[0] not in result:
                        for x in range(0, len(result)-1):
                            if result[x] == '':
                                result[x] = action[0]
                                break
        return result

    @staticmethod
    def fix_case(string):
        string = str(string)
        if len(string) > 0:
            return string.capitalize()


if __name__ == '__main__':
    fwb = Faeriawikibot()
    merlincards = fwb.parse_merlin()
    templatecards = fwb.merlin2cardinfo()

    gc = gamepedia_client.GamepediaClient()

    gc.login(username=username,password=password)
    #gc.create_action_templates()
    for card in merlincards:
        with urllib.request.urlopen(r.GithubResource.get_card_english(id=card['card_id'])) as resp, open('resources/english_cards/{0}.png'.format(card['card_id']), 'wb') as f:
            data = resp.read()
            f.write(data)
        gc.upload_images('resources/english_cards/{0}.png'.format(card['card_id']),'{lang}_{card_id}.png'.format(lang='english',card_id=card['card_id']), card['card_name'])

        #break
    #for x in range(0, len(merlincards)-1):
    #    gc.submit_card(merlincards[x], templatecards[x])
