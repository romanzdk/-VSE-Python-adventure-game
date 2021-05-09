#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#Q:/65_PGM/65_PYT/game/game_v1a/game.py
"""
Modul reprezentuje hru.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from ..api.game_types import *

from . import actions, world as wrld


############################################################################

def isAlive() -> bool:
    """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return actions.is_active()


def all_actions() -> tuple[AAction]:
    """Vrátí n-tici všech akcí použitelných ve hře.
    """
    return tuple(actions._NAME_2_ACTION.values())


def basic_actions() -> BasicActions:
    """Vrátí přepravku s názvy povinných akcí.
    """
    return BasicActions(MOVE_NAME='Jdi', PUT_DOWN_NAME='Polož',
                        TAKE_NAME='Vezmi', HELP_NAME='?', END_NAME='KONEC')


def bag() -> ABag:
    """Vrátí odkaz na batoh, do nějž bude hráč ukládat sebrané objekty.
    """
    return wrld.BAG


def world() -> AWorld:
    """Vrátí odkaz na svět hry.
    """
    return wrld


def execute_command(command:str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """
    return actions.execute_command(command)


def stop():
    """Ukončí hru a uvolní alokované prostředky.
    Zadáním prázdného příkazu lze následně spustit hru znovu.
    """
    actions.stop()



############################################################################



############################################################################
dbg.stop_mod (0, __name__)
