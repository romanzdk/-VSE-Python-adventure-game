#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Balíček s továrním modulem prozrazujícím autora, modulem se scénáři
a výchozími verzemi všech modulů budoucí hry.
Oproti minulé verzi přibyly moduly budoucí hry.
"""
import dbg
dbg.start_pkg(0, __name__, __doc__)
# ############################################################################

# from ..api.scenarios    import Scenario
# from ..api.game_types   import AFactory

# from .scenarios import SCENARIOS


# ############################################################################

# class Factory(AFactory):
#     """Definice třídy umožňuje definovat
#     """
#     @property
#     def scenarios(self) -> tuple[Scenario]:
#         """Vrátí n-tici definovaných scénářů.
#         """
#         return SCENARIOS


#     @property
#     def authorName(self) -> str:
#         """Vrátí jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
#         tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
#         u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
#         Má-li autor programu více křestních jmen, může je uvést všechna.
#         """
#         return 'PECINOVSKÝ Rudolf'


#     @property
#     def authorID(self) -> str:
#         """Vrátí identifikační řetězec autora/autorky programu
#         zapsaný VELKÝMI PÍSMENY.
#         Tímto řetězcem bývá login do informačního systému školy.
#         """
#         return 'RUP_1B'

# factory = Factory()



############################################################################
dbg.stop_mod (0, __name__)
