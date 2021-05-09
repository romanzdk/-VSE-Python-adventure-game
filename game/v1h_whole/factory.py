#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Modul funguje jako tovární objekt definující tovární funkce,
prostřednictvím nichž testovací program získá klíčové objekty dané aplikace.
V této etapě je vedle scénářů k dispozici i odkaz
na hru kompletně realizující zadání.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from ..api.game_types import AGame
from ..api.scenario   import Scenario

from .scenarios import SCENARIOS


############################################################################

def scenarios() -> tuple[Scenario]:
    """Vrátí n-tici definovaných scénářů.
    """
    return SCENARIOS


def game() -> 'AGame':
    """Vrátí odkaz na objekt reprezentující hru.
    """
    from . import game
    return game


def authorID() -> str:
    """Vrátí identifikační řetězec autora/autorky programu
    zapsaný VELKÝMI PÍSMENY.
    Tímto řetězcem bývá login do informačního systému školy.
    """
    return 'V1H'


def authorName() -> str:
    """Vrátí jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
    tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
    u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
    Má-li autor programu více křestních jmen, může je uvést všechna.
    """
    return 'WHOLE'



############################################################################
dbg.stop_mod (0, __name__)
