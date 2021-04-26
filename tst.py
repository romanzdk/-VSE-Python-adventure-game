#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Pomocný modul pro zrychlené zadávání testů.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from game.zydr00_zydyk import factory as f
from game.tests     import test_factory as tf

tf.test(f, 3)

############################################################################
dbg.stop_mod (0, __name__)
