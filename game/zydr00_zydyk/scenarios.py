#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Základní trojice scénářů pro hru o sněhovém pekle.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from ..api.scenario  import ScenarioStep, Scenario
from ..api.scen_types import *  # Především typu kroků

############################################################################
# Základní úspěšný scénář demonstrující průběh hry, při němž hráč
# nezadává žádné chybné příkazy a dosáhne zadaného cíle.
ScenarioStep.next_index = 0  # Index počátečního kroku

HAPPY = Scenario('', stHAPPY, (
    START_STEP:=
    ScenarioStep(tsSTART, '',           # Zadaný příkaz
          'Vítejte!\nPrávě jste se probudil na zasněženém poli...\n'
          'Nemůžete si vzpomenout, co se stalo...\n'
          'Je zima a padá sníh...\n'
          '...\n'
          'Dostaňte se z tohoto místa a zachraňte se.\n'
          'Nebudete-li si vědět rady, zadejte znak ?.',
          'pole',    # Aktuální prostor
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas',),           # H-Objekty v batohu
          ),
    ScenarioStep(tsNS_0, 'zakric',           # Zadaný příkaz
          'Křičíte o pomoc...\Pořád křičíte...\nUž nemůžete...\n'
          'Nikdo se neozývá...\nKřik vzdáváte.',
          'pole',    # Aktuální prostor
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas',),           # H-Objekty v batohu
          ),
      ScenarioStep(tsNS_0, 'brec',           # Zadaný příkaz
          'Brečíte zoufalstvím...\nPořád brečíte...\nUž vás to nebaví...\n'
          'Vzchopíte se a jdete něco dělat.',
          'pole',    # Aktuální prostor
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas',),           # H-Objekty v batohu
          ),
      ScenarioStep(tsGOTO, 'jdi skaly', # Zadaný příkaz
          'Přesunuli jste se do prostoru: skaly.\n'
          'U vysokých skal se nachází hluboký temný les.\n'
          'Od lesa vychází hrůzostrašné vytí vlků...',
          'skaly',    # Aktuální prostor
          ('les', 'pole', ),    # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas', ),   # H-Objekty v batohu
          ),
      ScenarioStep(tsGOTO, 'jdi pole',
          'Přesunuli jste se do prostoru: pole.\n'
          'Zde jste se probudili... Vedou odtud 4 cesty.',
          'pole',
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (),
          ('kompas', ),
          ),
    ScenarioStep(tsGOTO, 'jdi kopec', # Zadaný příkaz
          'Přesunuli jste se do prostoru: kopec.\n'
          'Na kopci jste objevili hořící vrak helikoptéry.',
          'kopec',    # Aktuální prostor
          ('pole', ),    # Aktuální sousedé
          ('helikoptera',), # H-objekty v prostoru
          ('kompas', ),   # H-Objekty v batohu
          ),
    ScenarioStep(tsNS_1, 'prozkoumej helikoptera',
          'Prozkoumali jste: helikoptera.\n'
          'Našli jste tyto věci: mobil, mapu, flash_disk a naradi.',
          'kopec',
          ('pole',),
          ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
          ('kompas',),
          ),
    ScenarioStep(tsTAKE, 'vezmi flash_disk',
          'Sebrali jste: flash_disk.\n'
          'Obyčejná flashka. Její obsah bohužel nejste schopni zjistit.',
          'kopec',
          ('pole',),
          ('mobil', 'mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', ),
          ),
      ScenarioStep(tsTAKE, 'vezmi mobil',
          'Sebrali jste: mobil.\n'
          'Telefon je bohužel rozbitý a tak je k ničemu.',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', 'mobil'),
          ),
      ScenarioStep(tsPUT_DOWN, 'poloz mobil',
          'Vyhodili jste: mobil.',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera', 'mobil'),
          ('kompas', 'flash_disk'),
          ),
    ScenarioStep(tsGOTO, 'jdi pole',
          'Přesunuli jste se do prostoru: pole.\n'
          'Zde jste se probudili... Vedou odtud 4 cesty.',
          'pole',
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (),
          ('kompas', 'flash_disk', ),
          ),
    ScenarioStep(tsGOTO, 'jdi majak',
          'Přesunuli jste se do prostoru: majak.\n'
          'U majáku se nachází velká hala.',
          'majak',
          ('hala', 'pole', ),
          ('dvere', ),
          ('kompas', 'flash_disk', ),
          ),
    ScenarioStep(tsGOTO, 'jdi hala',
          'Přesunuli jste se do prostoru: hala.\n'
          'V hale jste našli mimo jiné velké počítačové centrum.',
          'hala',
          ('majak',),
          ('pocitace', ),
          ('kompas', 'flash_disk', ),
          ),
    ScenarioStep(tsNS_2, 'pouzij flash_disk pocitace',
          'Použili jste: flash_disk na: pocitace.\n'
          'Flash disk jste připojili k počítači.\n'
          '...\n'
          'Úspěšně jste se díky obsahu na flashce dostali do počítačů...\n'
          'Nyní si můžete zavolat pomoc a budete zachráněni...'
          'Gratuluji, vyhráli jste!',
          'hala',
          ('majak',),
          ('pocitace', 'flash_disk' ),
          ('kompas', ),
          )
    )
)

############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení základních akcí
# a současně vyzkouší vyvolání nápovědy a nestandardní ukončení.

ScenarioStep.next_index = -1  # Index kroku před korektním startem

WRONG_START = ScenarioStep(tsNOT_START, 'start', # Zadaný příkaz
        'Prvním příkazem není startovací příkaz.\n' +
        'Hru, která neběží, lze spustit pouze startovacím příkazem.',
        '',                                         # Aktuální prostor
        (),                                         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        )

ScenarioStep.next_index = +1  # Index prvního kroku za startem

MISTAKE = Scenario('', stMISTAKES, (
    WRONG_START,

    START_STEP,

    ScenarioStep(tsEMPTY, '',                       # Zadaný příkaz
        'Prázdný příkaz lze použít pouze pro start hry',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsUNKNOWN, 'maso',                 # Zadaný příkaz
        'Tento příkaz neznám: maso',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsMOVE_WA, "jdi",                  # Zadaný příkaz
        'Nevím, kam mám jít.\n'
        'Je třeba zadat jméno cílového prostoru.',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsTAKE_WA, "vezmi",                # Zadaný příkaz
        'Nevím, co mám vzít.\n'
        'Je třeba zadat jméno zvedaného objektu.',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsPUT_DOWN_WA, "poloz",            # Zadaný příkaz
        'Nevím, co mám položit.\n'
        'Je třeba zadat jméno pokládaného objektu.',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsBAD_NEIGHBOR, "jdi do_háje", # Zadaný příkaz
        'Do zadaného prostoru se odsud jít nedá: do_háje.',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsBAD_ITEM, "vezmi whisky",        # Zadaný příkaz
        'Zadaný objekt v prostoru není: whisky',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsGOTO, 'jdi kopec',               # Zadaný příkaz
          'Přesunuli jste se do prostoru: kopec.\n'
          'Na kopci jste objevili hořící vrak helikoptéry.',
          'kopec',                                  # Aktuální prostor
          ('pole', ),                               # Aktuální sousedé
          ('helikoptera',),                         # H-objekty v prostoru
          ('kompas', ),                             # H-Objekty v batohu
        ),  

    ScenarioStep(tsUNMOVABLE, "vezmi helikoptera",  # Zadaný příkaz
        'Zadaný objekt není možno zvednout: helikoptera',
        'kopec',                                    # Aktuální prostor
          ('pole', ),                               # Aktuální sousedé
          ('helikoptera',),                         # H-objekty v prostoru
          ('kompas', ),                             # H-Objekty v batohu
        ),
    
    ScenarioStep(tsNS_1, 'prozkoumej helikoptera',
          'Prozkoumali jste: helikoptera.\n'
          'Našli jste tyto věci: mobil, mapu, flash_disk a naradi.',
          'kopec',
          ('pole',),
          ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
          ('kompas',),
          ),

    ScenarioStep(tsTAKE, 'vezmi flash_disk',
          'Sebrali jste: flash_disk.\n'
          'Obyčejná flashka. Její obsah bohužel nejste schopni zjistit.',
          'kopec',
          ('pole',),
          ('mobil', 'mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', ),
          ),
    
    ScenarioStep(tsTAKE, 'vezmi mobil',
          'Sebrali jste: mobil.\n'
          'Telefon je bohužel rozbitý a tak je k ničemu.',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', 'mobil'),
          ),

    ScenarioStep(tsBAG_FULL, 'vezmi mapa',
          'Zadaný objekt se už do batohu nevejde!',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', 'mobil'),
          ),

    ScenarioStep(tsNOT_IN_BAG, 'poloz mapa',     # Zadaný příkaz
        'Zadaný objekt v batohu není: mapa',
        'kopec',
        ('pole',),
        ('mapa', 'naradi', 'helikoptera'),
        ('kompas', 'flash_disk', 'mobil'),
        ),

    ScenarioStep(tsHELP, '?',                       # Zadaný příkaz
        'Vaším úkolem je zachránit se - dostat se z tohoto místa\n'
        'Můžete zadat tyto příkazy:\n'
        'jdi <místo>\n'
        'vezmi <předmět>\n'
        'poloz <předmět>\n'
        'prozkoumej <předmět>\n'
        'pouzij <předmět1> <předmět2>\n'
        'zakric\n'
        'brec\n'
        'konec\n'
        '?',
        'kopec',
        ('pole',),
        ('mapa', 'naradi', 'helikoptera'),
        ('kompas', 'flash_disk', 'mobil'),
        ),

    ScenarioStep(tsEND, 'konec',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'kopec',
        ('pole',),
        ('mapa', 'naradi', 'helikoptera'),
        ('kompas', 'flash_disk', 'mobil'),
        ),

    ),
)

############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# # zadává chybně příkazy k provedení rozšiřujících akcí.
ScenarioStep.next_index = 7 # Index prvního nestandardního kroku
MISTAKE_NS = Scenario('', stMISTAKES_NS, (
        HAPPY.steps[0],
        HAPPY.steps[1],   # zakric
        HAPPY.steps[2],   # brec
        HAPPY.steps[3],   # jdi skaly
        HAPPY.steps[4],   # jdi pole
        HAPPY.steps[5],   # jdi kopec
        HAPPY.steps[6],   # prozkoumej helikoptera

    ScenarioStep(tsNS0_WrongCond, 'zakric',
        'Už jste jednou křičeli, pokud byste křičeli znovu,\n'
        'tak by vám došly všechny síly a jistě byste umrzli.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS0_WrongCond, 'brec',
        'Už jste jednou brečeli, pokud byste brečeli znovu,\n'
        'tak by vám došly všechny síly a jistě byste umrzli.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS1_WrongCond, 'prozkoumej helikoptera',
        'Předmět helikoptera jste již jednou prozkoumali, nelze stejný\n'
        'předmět prozkoumávat znovu.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),
    ScenarioStep(tsNS1_WRONG_ARG, 'prozkoumej sekera',
        'Zadaný objekt v prostoru není: sekera.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),
    ScenarioStep(tsNS1_0Args, 'prozkoumej',
        'Nevím co mám prozkoumat, zadejte argument.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),
    ScenarioStep(tsNS2_WRONG_1stARG, 'pouzij helikoptera mobil',
        'Nelze použít nepřenosný předmět: helikoptera.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS2_1Args, 'pouzij kompas',
        'Nevím na co mám zadaný předmět použít. Zadejte druhý předmět.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS2_WRONG_2ndARG, 'pouzij mobil nabijecka',
        'Nelze použít předmět: mobil na předmět: nabijecka, který ve hře není.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS2_WrongCond, 'pouzij kompas mobil',
        'Nelze použít předmět: kompas na předmět: mobil.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera',),
        ('kompas',),
    ),
    ScenarioStep(tsEND, 'konec',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'kopec',
        ('pole',),
        ('mapa', 'naradi', 'helikoptera', 'flash_disk', 'mobil'),
        ('kompas', ),
        ),
    )
)

############################################################################

ScenarioStep.next_index = +1  # Index prvního kroku za startem

START = Scenario('START', stGENERAL, (
    START_STEP,

    ScenarioStep(tsGOTO, 'jdi kopec',                           # Zadaný příkaz
          'Přesunuli jste se do prostoru: kopec.\n'
          'Na kopci jste objevili hořící vrak helikoptéry.',
          'kopec',                                           # Aktuální prostor
          ('pole', ),                                        # Aktuální sousedé
          ('helikoptera',),                             # H-objekty v prostoru
          ('kompas', ),                                    # H-Objekty v batohu
    ),
    ScenarioStep(tsPUT_DOWN, 'poloz kompas',
          'Vyhodili jste: kompas.',
          'kopec',
          ('pole',),
          ('helikoptera','kompas'),
          (),
    ),
    ScenarioStep(tsTAKE, 'vezmi kompas',
          'Sebrali jste: kompas.\n'
          'Funkční kompas.',
          'kopec',
          ('pole',),
          ('helikoptera',),
          ('kompas', ),
          ),
    ScenarioStep(tsEND, 'konec',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'kopec',
        ('pole',),
        ('mapa', 'naradi', 'helikoptera'),
        ('kompas', 'flash_disk', 'mobil'),
        )
))

############################################################################

SCENARIOS = (HAPPY, MISTAKE, MISTAKE_NS, START)

############################################################################
dbg.stop_mod (0, __name__)