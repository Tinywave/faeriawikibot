class GamepediaGenerator:
    template_cardinfobox_old = '{{Card infobox| id = {id}\n' \
                           '| illustration = {illustration}\n' \
                           '| color = {color}\n' \
                           '| type = {type}\n' \
                           '| rarity = {rarity}\n' \
                           '| gold = {gold}\n' \
                           '| faeria = {faeria}\n' \
                           '| land = {land}\n' \
                           '| power = {power}\n' \
                           '| life = {life}\n' \
                           '| desc = {desc}\n' \
                           '| ability1 = {ability1}\n' \
                           '| starter = {starter}\n' \
                           '| deck1 = {deck1}\n' \
                           '| deckq1 = {deckq1}\n}}'
    template_cardinfobox = '{{Card stats| card_id = {card_id}\n' \
                           '| illustration = {illustration}\n' \
                           '| card_color = {card_color}\n' \
                           '| card_name = {card_name}\n' \
                           '| card_type = {card_type}\n' \
                           '| rarity = {rarity}\n' \
                           '| gold = {gold}\n' \
                           '| faeria = {faeria}\n' \
                           '| lake = {lake}\n' \
                           '| forest = {forest}\n' \
                           '| mountain = {mountain}\n' \
                           '| desert = {desert}\n' \
                           '| power = {power}\n' \
                           '| life = {life}\n' \
                           '| desc = {desc}\n' \
                           '| codex1 = {codex1}\n' \
                           '| codex2 = {codex2}\n' \
                           '| codex3= {codex3}\n}}'

    def generate_card_old(self, id='', illustration='', color='', type='', rarity='', gold='', faeria='', land='', power='', life='', desc='', ability1 = '', starter='', deck1='', deckq1 = ''):
        return '{' + self.template_cardinfobox_old.format(id=id, illustration=illustration, color=color, type=type, rarity=rarity, gold=gold, faeria=faeria, land=land, power=power, life=life, desc=desc, ability1=ability1, starter=starter, deck1=deck1, deckq1=deckq1) + '}'

    def generate_card(self, card_id='', illustration='', card_color='', card_name='', card_type='', rarity='', gold='', faeria='', lake='', mountain='', desert='', forest='', power='', life='', desc='', codex1 = '', codex2='', codex3=''):
        return '{' + self.template_cardinfobox.format(card_id=card_id, illustration=illustration, card_color=card_color, card_name=card_name, card_type=card_type, rarity=rarity, gold=gold, faeria=faeria, lake=lake, mountain=mountain, desert=desert, forest=forest, power=power, life=life, desc=desc, codex1=codex1, codex2=codex2, codex3=codex3) + '}'


