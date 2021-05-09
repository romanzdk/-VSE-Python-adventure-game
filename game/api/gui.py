#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Definuje grafické uživatelské rozhraní pro hry vyhovující zadanému api.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from .gui_tools import gui_impl as gi



############################################################################

def load_adventure(factory, scenario_name=None):
    """Získá hru od zadaného továrního objektu a spustí GUI.
    Je-li zadán název použitého scénáře, spustí navíc řádící okno,
    které zjednoduší zadávání příkazu z tohoto scénáře.
    """
    gi.game = factory.game()
    if scenario_name is not None:
        from .scenario import SCENARIO_NAMES
        for i, name in enumerate(SCENARIO_NAMES):
            if name == scenario_name:
                scenario = factory.scenarios()[i]
                gi.GUI(True)
                return
        raise Exception("Scenario not found")
    else:
        gi.GUI()


print(f'načetl se modul {__name__}')
if __name__ == '__main__':
    """Při přímém spuštění nechá uživatele vybrat spouštěnou hru,
    kterou pak spustí v daném GUI.
    """
    print(f'Modul {__name__} se spustil')
    gi.Chooser()
    gi.GUI(True)



############################################################################
dbg.stop_mod (0, __name__)
