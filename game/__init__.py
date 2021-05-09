#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Balíček s postupně vyvíjenou hrou a jejími testy.¤

Podbalíčky:
    api     Společné API všech her
    tests   Testy jednotlivých etap vývoje hry
    v#?_... Balíčky stavu hry v jednotlivých etapách

    v1a_happy_scenario      Definována jen továrna a šťastný scénář
    v1b_all_scenarios       Definovány všechny čtyři scénáře
                            HAPPY, MISTAKES, MISTAKES_NS a START
    v1c_basic_architecture  Zárodek hry se základní architekturou
                            převzatou z api
    v1d_start               Aplikaci je možno spustit, tj. odstartuje se
    v1f_basic_actions       Fungují základní čtyři akce
    v1e_world               Aplikace po odstartování vybuduje svět,
                            zhroutí se až na prvním dalším příkazu
    v1g_mistakes            Základní akce vzdorují chybně zadaným příkazům,
                            je testovatelná scénáři START a MISTAKES
    v1h_whole               Hra funguje včetně nadstandardních akcí,
                            projde testy podle všech čtyř scénářů
"""
import dbg
dbg.start_pkg(0, __name__, __doc__)
############################################################################
