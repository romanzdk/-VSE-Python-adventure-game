#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Dokumentační komentář modulu.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from .texts import *



############################################################################

class TestException:
    """Výjimka vyhazovaná při objevu závažných chyb v průběhu testování.
    """



############################################################################
#
# def clear_err_msgs():
#     """Vyčistí seznam chybových zpráv na počátku dalšího testu.
#     """
#     _ERR_MSGs.clear()
#
#
# def get_err_msgs():
#     """Vrátí kopii seznamu chybových zpráv.
#     """
#     return _ERR_MSGs[:]
#
#
# def add_err_msg(err_msg:str):
#     """Přidá do seznamu chybových zpráv další zprávu.
#     """
#     _ERR_MSGs.append(err_msg)
#



############################################################################

_ERR_MSGs:list[str] = []



############################################################################
dbg.stop_mod (0, __name__)
