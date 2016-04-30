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
            # card = ggen.generate_card_old(id=mc['card_id'], illustration='{lang}_{card_id}.png'.format(lang='english',card_id=mc['card_id']), color=mc['card_color'], type=mc['card_type'], rarity=mc['rarity'], gold='', faeria=mc['faeria'], land='1', power=mc['power'], life=mc['life'], desc=mc['desc'], ability1 = '', starter='', deck1='', deckq1 = '')
            card = ggen.generate_card(card_id=mc['card_id'], illustration='{lang}_{card_id}.png'.format(lang='english',card_id=mc['card_id']), card_color=mc['card_color'], card_name=mc['card_name'], card_type=mc['card_type'], rarity=mc['rarity'], gold=mc['gold'], faeria=mc['faeria'], lake=mc['lake'], mountain=mc['mountain'], desert=mc['desert'], forest=mc['forest'], power=mc['power'], life=mc['life'], desc=self.change_desc_actions_to_templates(mc['desc']), codex1 = mc['codex1'], codex2=mc['codex2'], codex3=mc['codex3'])
            self.cardlist.append(card)
            print(card)
        return self.cardlist

    def change_desc_actions_to_templates(self, desc):
        return str(desc).replace('{','{{').replace('}', '}}')


if __name__ == '__main__':
    fwb = Faeriawikibot()
    merlincards = fwb.parse_merlin()
    templatecards = fwb.merlin2cardinfo()

    gc = gamepedia_client.GamepediaClient()
    #gc.create_action_templates()
    for card in merlincards:
        with urllib.request.urlopen(r.GithubResource.get_card_english(id=card['card_id'])) as resp, open('resources/english_cards/{0}.png'.format(card['card_id']), 'wb') as f:
            data = resp.read()
            f.write(data)
        gc.upload_images('resources/english_cards/{0}.png'.format(card['card_id']),'{lang}_{card_id}.png'.format(lang='english',card_id=card['card_id']), card['card_name'])
        #break
