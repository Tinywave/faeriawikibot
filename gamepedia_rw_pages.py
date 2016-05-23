import os, sys
import configparser
import gamepedia_client


class GamepediaPagesRW:
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
    '''
    Write text from local file to page
    '''
    def upload(self, path, page):
        if self.gc is None:
            self.create_gamepedia_client()

        with open(path, 'r') as f:
            res = f.read()
        self.gc.write(page, res)

    '''
    Backup selection of pages
    '''
    def backup(self):
        self.backup_galleries_cards()

    '''
    Archivate selection of pages
    '''
    def archivate(self):
        self.download('setup/Template/Card_stats', 'Template:Card_stats')
        self.download('setup/Template/Cardlist', 'Template:Cardlist')
        self.download('setup/Template/Card_nav', 'Template:Card_nav')
        self.download('setup/Template/Codexcontentlist', 'Template:Codexcontentlist')

        self.download('setup/Lore/The_world', 'The_world')
        self.download('setup/Lore/Factions', 'Factions')
        self.download('setup/Lore/The_player,_the_orbs,_the_memoria', 'The_player,_the_orbs,_the_memoria')
        self.download('setup/Lore/The_Faëria', 'The_Faëria')

        self.download('setup/Template/Lake', 'Template:Lake')
        self.download('setup/Template/Mountain', 'Template:Mountain')
        self.download('setup/Template/Forest', 'Template:Forest')
        self.download('setup/Template/Desert', 'Template:Desert')

        self.download('setup/Template/Dpl_lake', 'Template:dpl_lake')
        self.download('setup/Template/Dpl_mountain', 'Template:dpl_mountain')
        self.download('setup/Template/Dpl_forest', 'Template:dpl_forest')
        self.download('setup/Template/Dpl_desert', 'Template:dpl_desert')
        self.download('setup/Template/Dpl_life', 'Template:Lif')
        self.download('setup/Template/Dpl_power', 'Template:Pow')
        self.download('setup/Template/Dpl_name', 'Template:dpl_name')
        self.download('setup/Template/Dpl_display', 'Template:dpl_display')

        self.download('setup/Template/Rarity', 'Template:Rarity')
        self.download('setup/Template/Common', 'Template:Common')
        self.download('setup/Template/Rare', 'Template:Rare')
        self.download('setup/Template/Epic', 'Template:Epic')
        self.download('setup/Template/Legendary', 'Template:Legendary')

        self.download('setup/List/List_of_Cards', 'List_of_Cards')
        self.download('setup/List/List_of_Blue_cards', 'List_of_Blue_cards')
        self.download('setup/List/List_of_Green_cards', 'List_of_Green_cards')
        self.download('setup/List/List_of_Red_cards', 'List_of_Red_cards')
        self.download('setup/List/List_of_Yellow_cards', 'List_of_Yellow_cards')
        self.download('setup/List/List_of_Human_cards', 'List_of_Human_cards')

        self.download('setup/List/List_of_Common_cards', 'List_of_Common_cards')
        self.download('setup/List/List_of_Rare_cards', 'List_of_Rare_cards')
        self.download('setup/List/List_of_Epic_cards', 'List_of_Epic_cards')
        self.download('setup/List/List_of_Legendary_cards', 'List_of_Legendary_cards')

        self.download('setup/List/List_of_Creature_cards', 'List_of_Creature_cards')
        self.download('setup/List/List_of_Structure_cards', 'List_of_Structure_cards')
        self.download('setup/List/List_of_Event_cards', 'List_of_Event_Cards')

        self.download('setup/List/List_of_Charge_X_cards', 'List_of_Charge_X_cards')
        self.download('setup/List/List_of_Faeria_X_cards', 'List_of_Faeria_X_cards')
        self.download('setup/List/List_of_Options_cards', 'List_of_Options_cards')
        self.download('setup/List/List_of_Ranged_cards', 'List_of_Ranged_cards')
        self.download('setup/List/List_of_Production_cards', 'List_of_Production_cards')
        self.download('setup/List/List_of_Combat_cards', 'List_of_Combat_cards')
        self.download('setup/List/List_of_Protection_cards', 'List_of_Protection_cards')
        self.download('setup/List/List_of_Taunt_cards', 'List_of_Taund_cards')
        self.download('setup/List/List_of_Haste_cards', 'List_of_Haste_cards')
        self.download('setup/List/List_of_Last_Words_cards', 'List_of_Last_Words_cards')
        self.download('setup/List/List_of_Deathtouch_cards', 'List_of_Deathtouch_cards')
        self.download('setup/List/List_of_Flying_cards', 'List_of_Flying_cards')
        self.download('setup/List/List_of_Jump_cards', 'List_of_Jump_cards')
        self.download('setup/List/List_of_Aquatic_cards', 'List_of_Aquatic_cards')
        self.download('setup/List/List_of_Activate_cards', 'List_of_Activate_cards')
        self.download('setup/List/List_of_Gift_cards', 'List_of_Gift_cards')

        self.download('setup/Cards/By Color/Human', 'Human')
        self.download('setup/Cards/By Color/Blue', 'Blue')
        self.download('setup/Cards/By Color/Green', 'Green')
        self.download('setup/Cards/By Color/Red', 'Red')
        self.download('setup/Cards/By Color/Yellow', 'Yellow')

        self.download('setup/Cards/By Type/Creature', 'Creature')
        self.download('setup/Cards/By Type/Event', 'Event')
        self.download('setup/Cards/By Type/Structure', 'Structure')

        self.download('setup/Cards/By Rarity/Common', 'Common')
        self.download('setup/Cards/By Rarity/Rare', 'Rare')
        self.download('setup/Cards/By Rarity/Epic', 'Epic')
        self.download('setup/Cards/By Rarity/Legendary', 'Legendary')

        self.download('setup/Gallery/Gallery_of_Blue_cards', 'Gallery_of_Blue_cards')
        self.download('setup/Gallery/Gallery_of_Green_cards', 'Gallery_of_Green_cards')
        self.download('setup/Gallery/Gallery_of_Human_cards', 'Gallery_of_Human_cards')
        self.download('setup/Gallery/Gallery_of_Red_cards', 'Gallery_of_Red_cards')
        self.download('setup/Gallery/Gallery_of_Yellow_cards', 'Gallery_of_Yellow_cards')


    '''
    Restore selection of default pages
    '''
    def restore(self):
        self.restore_cards_by()
        self.restore_galleries_cards()

    '''
    Restore Cards By-X
    '''
    def restore_cards_by(self):
        self.upload('setup/Cards/By Color/Human', 'Human')
        self.upload('setup/Cards/By Color/Blue', 'Blue')
        self.upload('setup/Cards/By Color/Green', 'Green')
        self.upload('setup/Cards/By Color/Red', 'Red')
        self.upload('setup/Cards/By Color/Yellow', 'Yellow')

        self.upload('setup/Cards/By Type/Creature', 'Creature')
        self.upload('setup/Cards/By Type/Event', 'Event')
        self.upload('setup/Cards/By Type/Structure', 'Structure')

        self.upload('setup/Cards/By Rarity/Common', 'Common')
        self.upload('setup/Cards/By Rarity/Rare', 'Rare')
        self.upload('setup/Cards/By Rarity/Epic', 'Epic')
        self.upload('setup/Cards/By Rarity/Legendary', 'Legendary')

    '''
    Restore Changelog Templates
    '''
    def restore_templates_changelog(self):
        self.upload('setup/Template/Changelog/Cl_codexcode1', 'Template:Cl_codexcode1')
        self.upload('setup/Template/Changelog/Cl_codexcode2', 'Template:Cl_codexcode2')
        self.upload('setup/Template/Changelog/Cl_codexcode3', 'Template:Cl_codexcode3')
        self.upload('setup/Template/Changelog/Cl_color', 'Template:Cl_color')
        self.upload('setup/Template/Changelog/Cl_desc', 'Template:Cl_desc')
        self.upload('setup/Template/Changelog/Cl_desert', 'Template:Cl_desert')
        self.upload('setup/Template/Changelog/Cl_faeria', 'Template:Cl_faeria')
        self.upload('setup/Template/Changelog/Cl_forest', 'Template:Cl_forest')
        self.upload('setup/Template/Changelog/Cl_lake', 'Template:Cl_lake')
        self.upload('setup/Template/Changelog/Cl_life', 'Template:Cl_life')
        self.upload('setup/Template/Changelog/Cl_mountain', 'Template:Cl_mountain')
        self.upload('setup/Template/Changelog/Cl_name', 'Template:Cl_name')
        self.upload('setup/Template/Changelog/Cl_power', 'Template:Cl_power')
        self.upload('setup/Template/Changelog/Cl_rarity', 'Template:Cl_rarity')
        self.upload('setup/Template/Changelog/Cl_type', 'Template:Cl_type')
        self.upload('setup/Template/Changelog/Cl_unknown', 'Template:Cl_unknown')
        self.upload('setup/Template/Changelog/Cl_info', 'Template:Cl_info')

    '''
    Restore Card Galleries
    '''
    def restore_galleries_cards(self):
        self.upload('setup/Gallery/Gallery_of_Blue_cards', 'Gallery_of_Blue_cards')
        self.upload('setup/Gallery/Gallery_of_Green_cards', 'Gallery_of_Green_cards')
        self.upload('setup/Gallery/Gallery_of_Human_cards', 'Gallery_of_Human_cards')
        self.upload('setup/Gallery/Gallery_of_Red_cards', 'Gallery_of_Red_cards')
        self.upload('setup/Gallery/Gallery_of_Yellow_cards', 'Gallery_of_Yellow_cards')

        self.upload('setup/Gallery/Gallery_of_Creature_cards', 'Gallery_of_Creature_cards')
        self.upload('setup/Gallery/Gallery_of_Structure_cards', 'Gallery_of_Structure_cards')
        self.upload('setup/Gallery/Gallery_of_Event_cards', 'Gallery_of_Event_cards')

        self.upload('setup/Gallery/Gallery_of_Common_cards', 'Gallery_of_Common_cards')
        self.upload('setup/Gallery/Gallery_of_Rare_cards', 'Gallery_of_Rare_cards')
        self.upload('setup/Gallery/Gallery_of_Epic_cards', 'Gallery_of_Epic_cards')
        self.upload('setup/Gallery/Gallery_of_Legendary_cards', 'Gallery_of_Legendary_cards')

    '''
    Restore Lists of (effect) cards
    '''
    def restore_lists_effects(self):
        self.download('setup/List/List_of_Charge_X_cards', 'List_of_Charge_X_cards')
        self.download('setup/List/List_of_Faeria_X_cards', 'List_of_Faeria_X_cards')
        self.download('setup/List/List_of_Options_cards', 'List_of_Options_cards')
        self.download('setup/List/List_of_Ranged_cards', 'List_of_Ranged_cards')
        self.download('setup/List/List_of_Production_cards', 'List_of_Production_cards')
        self.download('setup/List/List_of_Combat_cards', 'List_of_Combat_cards')
        self.download('setup/List/List_of_Protection_cards', 'List_of_Protection_cards')
        self.download('setup/List/List_of_Taunt_cards', 'List_of_Taund_cards')
        self.download('setup/List/List_of_Haste_cards', 'List_of_Haste_cards')
        self.download('setup/List/List_of_Last_Words_cards', 'List_of_Last_Words_cards')
        self.download('setup/List/List_of_Deathtouch_cards', 'List_of_Deathtouch_cards')
        self.download('setup/List/List_of_Flying_cards', 'List_of_Flying_cards')
        self.download('setup/List/List_of_Jump_cards', 'List_of_Jump_cards')
        self.download('setup/List/List_of_Aquatic_cards', 'List_of_Aquatic_cards')
        self.download('setup/List/List_of_Activate_cards', 'List_of_Activate_cards')
        self.download('setup/List/List_of_Gift_cards', 'List_of_Gift_cards')
        self.download('setup/List/List_of_Random_cards', 'List_of_Random_cards')

        '''
    Restore Card Galleries
    '''

    '''
    Backup Card Galleries
    '''
    def backup_galleries_cards(self):
        self.download('setup/Gallery/Gallery_of_Blue_cards', 'Gallery_of_Blue_cards')
        self.download('setup/Gallery/Gallery_of_Green_cards', 'Gallery_of_Green_cards')
        self.download('setup/Gallery/Gallery_of_Human_cards', 'Gallery_of_Human_cards')
        self.download('setup/Gallery/Gallery_of_Red_cards', 'Gallery_of_Red_cards')
        self.download('setup/Gallery/Gallery_of_Yellow_cards', 'Gallery_of_Yellow_cards')

        self.download('setup/Gallery/Gallery_of_Creature_cards', 'Gallery_of_Creature_cards')
        self.download('setup/Gallery/Gallery_of_Structure_cards', 'Gallery_of_Structure_cards')
        self.download('setup/Gallery/Gallery_of_Event_cards', 'Gallery_of_Event_cards')

        self.download('setup/Gallery/Gallery_of_Common_cards', 'Gallery_of_Common_cards')
        self.download('setup/Gallery/Gallery_of_Rare_cards', 'Gallery_of_Rare_cards')
        self.download('setup/Gallery/Gallery_of_Epic_cards', 'Gallery_of_Epic_cards')
        self.download('setup/Gallery/Gallery_of_Legendary_cards', 'Gallery_of_Legendary_cards')

if __name__ == '__main__':
    gr = GamepediaPagesRW()
    global cfg_file
    cfg_file = configparser.ConfigParser()
    path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
    path_to_cfg = os.path.join(path_to_cfg, 'faeriawikibot.conf')
    cfg_file.read(path_to_cfg)
    gr.restore()

