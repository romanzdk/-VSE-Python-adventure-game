#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Sada tříd a funkcí pro otestování korektnosti definic továrních objektů.
"""
import dbg
dbg.start_mod(0, __name__, '')
############################################################################

import traceback

from datetime   import datetime
from enum       import Enum

from ..api.game_types   import AFactory

# from .common.errors     import clear_err_msgs, add_err_msg, get_err_msgs

# Budou-li se testovat scénáře
# from .test_scenario import test_scenarios_from

# Bude-li se testovat hra
# from .test_game import test_game_from



############################################################################

from collections import namedtuple
LIMITS = (namedtuple('Limits', 'minSteps minPlaces minVisited minNSActions')
          (12,  # Minimální počet kroků scénáře HAPPY
            6,  # Minimální počet prostorů
            4,  # Minimální počet navštívených prostorů
            4)) # Minimální počet vlastních (= nestandardních) akcí



############################################################################
class Level(Enum):
    """Hladiny podrobností testů.
    """
    HAPPY      = 0  # Očekává se jen šťastný scénář definovaný jako n-tice
    MISTAKE    = 1  # Scénáře jsou definované jako instance třídy Scenario,
                    # testuje se šťastný a chybový scénář
    MISTAKE_NS = 2  # Otestuje i chybový scénář rozšiřujících akcí
    GAME       = 3  # Otestuje hru podle základních scénářů
    EXTENDED   = 4  # Otestuje hru podle všech definovaných scénářů



############################################################################


def ERROR(message:str):
    """Vypíše chybovou zprávu a vyhodí výjimku
    """
    from .common.texts import N_BEFORE_N, N_AFTER_N
    print(f'{N_BEFORE_N}{message}{N_AFTER_N}')
    raise Exception()




############################################################################

def pre_import():
    """Sada akcí, které se musí udělat před tím,
    než se importuje další testovaný modul.
    """
    from ..api.scenario import Scenario
    Scenario.count = 0


def test(factory: AFactory, level:Level, scen_lst:list[int]=[3]) -> bool:
    """Otestuje zadaný tovární objekt do zadané hloubky.
    Ověří, že zadaná továrna poskytne podklady pro identifikaci autora,
    poskytuje počet scénářů požadovaných argumentem level
    a následně nechá tento počet scénářů otestovat.
    Zprávu o testu tiskne na standardní výstup a pro informace získané
    v průběhu testování vytvoří objekt typu ScenariosSummary,
    který uloží jako globální atribut.
    """
    global _factory
    _factory    = factory
    _start_time = datetime.now()
    errors = False
    try:
        _verify_author()
        _verify_package()
        happy_steps = (factory.happy_scenario() if level == Level.HAPPY.value
                  else factory.scenarios()[0].steps)
        invitation = happy_steps[0].message
        prolog = (f'Autor:   {_autor_both}\n'
                  f'Balíček: {factory.__package__}\n'
                  f'########## START: {_start_time}\n'
                  f'{_H60}\n{invitation}\n{_E60}')
        epilog = (f'{_H60}\n'
                  f'########## KONEC testu autora {_autor_both}\n'
                  f'{_H60}\n')
        print(prolog)
        if level >= Level.HAPPY.value:
            # Budou se testovat scénáře
            from .test_scenario import test_scenarios_from
            global result
            result = test_scenarios_from(factory, level)
        if level >= Level.GAME.value:
            # Bude se testovat hra
            # from .test_game import test_game_from
            # test_game_from(factory, level)
            # factory.scenarios()[3].test(factory.game())
            g  = factory.game()
            ss = factory.scenarios()
            for i in scen_lst:
                ss[i].test(g)
    except Exception as ex:
        result = f'Výjimka: {ex}'
        traceback.print_exc()
    finally:
        print(epilog)
        # if errors:
        #     print('Testovaný program vyhodil výjimku:')
        # else:
        #     print('Testovaný program prošel')
    print(f'Výsledek: {result}')
    return result



############################################################################

def _verify_author():
    """Ověří že testovaný tovární objekt umí dodat autora a jeho ID
    a že dodané stringy vyhovují požadavkům.
    """
    global _author_name, _author_ID, _autor_both
    try:
        _author_name = _factory.authorName()
        _author_ID   = _factory.authorID()
    except Exception as ex:
        ERROR('Tovární objekt neposkytuje jméno a/nebo '
              'identifikační string autora')
    if _author_ID != _author_ID.upper():
        ERROR('Identifikační string autora není velkými písmeny: '
             + _author_ID )
    _autor_both = _author_ID + ' - ' + _author_name
    # words   = _author_name.split()
    # surname = words[0]
    # TODO Dodělat



def _verify_package():
    """Zjistí, v jakém balíčku se tovární objekt nachází a ověří,
    že název balíčku je správně odvozen z ID a jména autora.
    """
    return
    # TODO Dodělat test korektnosti názvu balíčku
    global _package
    # Objekt musí být buď modul, nebo instancí třídy definované v modulu
    if _factory.__class__.__name__ == 'module':
        _package = _factory.__class__.__package__
    else:
        _package = _factory.__class__.__module__.__package__



############################################################################

_H60: str = 60 * '#'
_E60: str = 60 * '='

_factory:AFactory       # Odkaz na testovaný tovární objekt
_author_name:str        # Jméno autora
_author_ID:str          # Identifikační string autora
_autor_both:str         # ID autora následované jeho jménem
_package:str            # Název balíčku, v němž je tovární třída
_start_time:datetime    # Čas spuštění testu


############################################################################
dbg.stop_mod (0, __name__)
