#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Balíček definující společné API všech her.¤
Obsahuje moduly definující společně používané objekty
a vedle nich i moduly definující povinné atributy
jejich ekvivalentů v odevzdaných semestrálních pracech.

Moduly:
    game_types  - Potenciální rodičovské typy tříd objektů hry;
                  Mají hlavně definovat požadované atributy
    scen_types  - Typy scénářů a jejich kroků
    scenarios   - Třídy kroků scénáře a scénářů
    gui         - Grafické uživatelské rozhraní pro hry dodržující api

"""
import dbg
dbg.start_pkg(0, __name__, __doc__)
