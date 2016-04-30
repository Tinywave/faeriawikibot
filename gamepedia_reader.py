import os, sys
import configparser
import gamepedia_client


class GamepediaReader:
    gc = None
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
    Download and save page.
    '''

    def download(self, path, page):
        if self.gc is None:
            self.create_gamepedia_client()
        res = self.gc.read(page)
        with open(path, 'w') as f:
            f.write(res)


if __name__ == '__main__':
    gr = GamepediaReader()
    global cfg_file
    cfg_file = configparser.ConfigParser()
    path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
    path_to_cfg = os.path.join(path_to_cfg, 'faeriawikibot.conf')
    cfg_file.read(path_to_cfg)

    gr.download('setup/Template/Card_stats', 'Template:Card_stats')

    gr.download('setup/Template/Lake', 'Template:Lake')
    gr.download('setup/Template/Mountain', 'Template:Mountain')
    gr.download('setup/Template/Forest', 'Template:Forest')
    gr.download('setup/Template/Desert', 'Template:Desert')

    gr.download('setup/Template/Dpl_lake', 'Template:dpl_lake')
    gr.download('setup/Template/Dpl_mountain', 'Template:dpl_mountain')
    gr.download('setup/Template/Dpl_forest', 'Template:dpl_forest')
    gr.download('setup/Template/Dpl_desert', 'Template:dpl_desert')
    gr.download('setup/Template/Dpl_life', 'Template:Lif')
    gr.download('setup/Template/Dpl_power', 'Template:Pow')
    gr.download('setup/Template/Dpl_name', 'Template:dpl_name')
    gr.download('setup/Template/Dpl_display', 'Template:dpl_display')

    gr.download('setup/Template/Rarity', 'Template:Rarity')
    gr.download('setup/Template/Common', 'Template:Common')
    gr.download('setup/Template/Rare', 'Template:Rare')
    gr.download('setup/Template/Epic', 'Template:Epic')
    gr.download('setup/Template/Legendary', 'Template:Legendary')

    gr.download('setup/List/List_of_Cards', 'List_of_Cards')
    gr.download('setup/List/List_of_Blue_cards', 'List_of_Blue_cards')
    gr.download('setup/List/List_of_Green_cards', 'List_of_Greem_cards')
    gr.download('setup/List/List_of_Red_cards', 'List_of_Red_cards')
    gr.download('setup/List/List_of_Yellow_cards', 'List_of_Yellow_cards')
    gr.download('setup/List/List_of_Human_cards', 'List_of_Human_cards')

    gr.download('setup/List/List_of_Common_cards', 'List_of_Common_cards')
    gr.download('setup/List/List_of_Rare_cards', 'List_of_Rare_cards')
    gr.download('setup/List/List_of_Epic_cards', 'List_of_Epic_cards')
    gr.download('setup/List/List_of_Legendary_cards', 'List_of_Legendary_cards')

    gr.download('setup/List/List_of_Creature_cards', 'List_of_Creature_cards')
    gr.download('setup/List/List_of_Structure_cards', 'List_of_Structure_cards')
    gr.download('setup/List/List_of_Event_cards', 'List_of_Event_Cards')

    gr.download('setup/List/List_of_Charge_X_cards', 'List_of_Charge_X_cards')
    gr.download('setup/List/List_of_Faeria_X_cards', 'List_of_Faeria_X_cards')
    gr.download('setup/List/List_of_Options_cards', 'List_of_Options_cards')
    gr.download('setup/List/List_of_Ranged_cards', 'List_of_Ranged_cards')
    gr.download('setup/List/List_of_Production_cards', 'List_of_Production_cards')
    gr.download('setup/List/List_of_Combat_cards', 'List_of_Combat_cards')
    gr.download('setup/List/List_of_Protection_cards', 'List_of_Protection_cards')
    gr.download('setup/List/List_of_Taunt_cards', 'List_of_Taund_cards')
    gr.download('setup/List/List_of_Haste_cards', 'List_of_Haste_cards')
    gr.download('setup/List/List_of_Last_Words_cards', 'List_of_Last_Words_cards')
    gr.download('setup/List/List_of_Deathtouch_cards', 'List_of_Deathtouch_cards')
    gr.download('setup/List/List_of_Flying_cards', 'List_of_Flying_cards')
    gr.download('setup/List/List_of_Jump_cards', 'List_of_Jump_cards')
    gr.download('setup/List/List_of_Aquatic_cards', 'List_of_Aquatic_cards')
    gr.download('setup/List/List_of_Activate_cards', 'List_of_Activate_cards')
    gr.download('setup/List/List_of_Gift_cards', 'List_of_Gift_cards')
