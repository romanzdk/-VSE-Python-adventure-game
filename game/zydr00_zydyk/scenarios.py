#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Základní trojice scénářů pro hru o snehovem pekle.
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
          'Kricite o pomoc...\nPorad kricite...\nUz nemuzete...\n'
          'Nikdo se neozyva...\nKrik vzdavate.',
          'pole',    # Aktuální prostor
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas',),           # H-Objekty v batohu
          ),
      ScenarioStep(tsNS_0, 'brec',           # Zadaný příkaz
          'Brecite zoufalstvim...\nPorad brecite...\nUz vas to nebavi...\n'
          'Vzchopite se a jdete neco delat.',
          'pole',    # Aktuální prostor
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas',),           # H-Objekty v batohu
          ),
      ScenarioStep(tsGOTO, 'jdi skaly', # Zadaný příkaz
          'Presunuli jste se do prostoru: skaly.\n'
          'U vysokych skal se nachazi hluboky temny les.\n'
          'Od lesa vychazi hruzostrasne vyti vlku...',
          'skaly',    # Aktuální prostor
          ('les', 'pole', ),    # Aktuální sousedé
          (), # H-objekty v prostoru
          ('kompas', ),   # H-Objekty v batohu
          ),
      ScenarioStep(tsGOTO, 'jdi pole',
          'Presunuli jste se do prostoru: pole.\n'
          'Zde jste se probudili... Vedou odtud 4 cesty.',
          'pole',
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (),
          ('kompas', ),
          ),
    ScenarioStep(tsGOTO, 'jdi kopec', # Zadaný příkaz
          'Presunuli jste se do prostoru: kopec.\n'
          'Na kopci jste objevili horici vrak helikoptery.',
          'kopec',    # Aktuální prostor
          ('pole', ),    # Aktuální sousedé
          ('helikoptera',), # H-objekty v prostoru
          ('kompas', ),   # H-Objekty v batohu
          ),
    ScenarioStep(tsNS_1, 'prozkoumej helikoptera',
          'Prozkoumali jste helikopteru...\n'
          'Nasli jste tyto veci: mobil, mapu, flash disk a naradi.',
          'kopec',
          ('pole',),
          ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
          ('kompas',),
          ),
    ScenarioStep(tsTAKE, 'vezmi flash_disk',
          'Sebrali jste flash disk. Nic o nem nevite.',
          'kopec',
          ('pole',),
          ('mobil', 'mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', ),
          ),
      ScenarioStep(tsTAKE, 'vezmi mobil',
          'Sebral jste mobil.\n'
          'Telefon je bohuzel rozbity a tak je k nicemu.',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', 'mobil'),
          ),
      ScenarioStep(tsPUT_DOWN, 'poloz mobil',
          'Vyhodili jste mobil.\n',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera', 'mobil'),
          ('kompas', 'flash_disk'),
          ),
    ScenarioStep(tsGOTO, 'jdi pole',
          'Přesunul jste se na pole, kde jste se vzbudil.',
          'pole',
          ('majak','skaly', 'kopec', 'jih',),     # Aktuální sousedé
          (),
          ('kompas', 'flash_disk', ),
          ),
    ScenarioStep(tsGOTO, 'jdi majak',
          'Presunuli jste se k majaku...\n'
          'Prisli jste ke dverim majaku. U majaku se nachazi velka hala.',
          'majak',
          ('hala', 'pole', ),
          ('dvere', ),
          ('kompas', 'flash_disk', ),
          ),
    ScenarioStep(tsGOTO, 'jdi hala',
          'Preseunuli jste se do haly...\n'
          'V hale jste nasli mimo jine velke pocitacove centrum.',
          'hala',
          ('majak',),
          ('pocitace', ),
          ('kompas', 'flash_disk', ),
          ),
    ScenarioStep(tsNS_2, 'pouzij flash_disk pocitace',
          'Pouzili jste flash disk.\nFlash disk jste pripojili k pocitaci.\n'
          '...\n'
          'Uspesne jste se diky obsahu na flashce dostali do pocitacu...\n'
          'Nyni si muzete zavolat pomoc a budete zachraneni...'
          'Gratuluji, vyhrali jste!',
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
        '\nPrvním příkazem není startovací příkaz.' +
        '\nHru, která neběží, lze spustit pouze startovacím příkazem.\n',
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
        'Nevím, co mám zvednout.\n'
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
        'Do zadaného prostoru se odsud jít nedá: do_háje.\n',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsBAD_ITEM, "vezmi whisky",        # Zadaný příkaz
        'Zadaný objekt v prostoru není: whisky\n',
        'pole',                                     # Aktuální prostor
        ('majak','skaly', 'kopec', 'jih',),         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        ('kompas',),                                # H-Objekty v batohu
        ),

    ScenarioStep(tsGOTO, 'jdi kopec',               # Zadaný příkaz
          'Presunuli jste se na kopec.\n'
          'Na kopci jste objevili horici vrak helikoptery.',
          'kopec',                                  # Aktuální prostor
          ('pole', ),                               # Aktuální sousedé
          ('helikoptera',),                         # H-objekty v prostoru
          ('kompas', ),                             # H-Objekty v batohu
        ),  

    ScenarioStep(tsUNMOVABLE, "vezmi helikoptera",  # Zadaný příkaz
        'Zadaný objekt není možno zvednout: helikoptera\n',
        'kopec',                                    # Aktuální prostor
          ('pole', ),                               # Aktuální sousedé
          ('helikoptera',),                         # H-objekty v prostoru
          ('kompas', ),                             # H-Objekty v batohu
        ),
    
    ScenarioStep(tsNS_1, 'prozkoumej helikoptera',
          'Prozkoumali jste helikopteru...\n'
          'Nasli jste tyto veci: mobil, mapu, flash disk a naradi.',
          'kopec',
          ('pole',),
          ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
          ('kompas',),
          ),

    ScenarioStep(tsTAKE, 'vezmi flash_disk',
          'Sebrali jste flash disk. Nic o nem nevite.',
          'kopec',
          ('pole',),
          ('mobil', 'mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', ),
          ),
    
    ScenarioStep(tsTAKE, 'vezmi mobil',
          'Sebral jste mobil.\n'
          'Telefon je bohuzel rozbity a tak je k nicemu.',
          'kopec',
          ('pole',),
          ('mapa', 'naradi', 'helikoptera'),
          ('kompas', 'flash_disk', 'mobil'),
          ),

    ScenarioStep(tsBAG_FULL, 'vezmi mapa',
          'Zadaný objekt se už do košíku nevejde!',
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
        'Tvým úkolem je zachránit se - dostat se z tohoto místa\n'
        'Můžeš zadat tyto příkazy:\n'
        'jdi <misto>\n'
        'vezmi <predmet>\n'
        'poloz <predmet>\n'
        'prozkoumej <predmet>\n'
        'pouzij <predmet1> <predmet2>\n'
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
        'Uz jsi jednou kricel, pokud by jsi zakricel znovu,\n'
        'tak by ti dosly vsechny sily a jiste by jsi umrzl.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS0_WrongCond, 'brec',
        'Uz jsi jednou brecel, pokud by jsi brecel znovu,\n'
        'tak by ti dosly vsechny sily a jiste by jsi umrzl.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS1_WrongCond, 'prozkoumej helikoptera',
        'Predmet helikoptera jsi jiz jednou prozkoumal, nelze stejny\n'
        'predmet prozkoumavat znovu.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),
    ScenarioStep(tsNS1_WRONG_ARG, 'prozkoumej sekera',
        'Predmet sekera nelze prozkoumat, jelikoz se zde nenachazi',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),
    ScenarioStep(tsNS1_0Args, 'prozkoumej',
        'Nevim co mam prozkoumat, zadejte argument.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),
    ScenarioStep(tsNS2_WRONG_1stARG, 'pouzij helikoptera mobil',
        'Nelze pouzit neprenosny predmet: helikoptera',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS2_1Args, 'pouzij kompas',
        'Nevim na co mam zadany predmet pouzit. Zadejte druhy predmet.',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsNS2_WRONG_2ndARG, 'pouzij kompas mobil',
        'Nelze pouzit predmet: kompas na predmet: mobil',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera'),
        ('kompas',),
    ),

    ScenarioStep(tsPUT_DOWN, 'poloz kompas',
        'Vyhodili jste kompas.\n',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera', 'kompas'),
        (),
    ),

    ScenarioStep(tsNS2_WrongCond, 'pouzij kompas mapa',
        'Nelze pouzit predmet: kompas, ktery nemas v batohu',
        'kopec',
        ('pole',),
        ('mobil', 'flash_disk', 'mapa', 'naradi', 'helikoptera', 'kompas'),
        (),
    ),
    ScenarioStep(tsEND, 'konec',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'kopec',
        ('pole',),
        ('mapa', 'naradi', 'helikoptera'),
        ('kompas', 'flash_disk', 'mobil'),
        ),
    )
)

############################################################################

ScenarioStep.next_index = +1  # Index prvního kroku za startem

START = Scenario('START', stGENERAL, (
    START_STEP,

    ScenarioStep(tsGOTO, 'jdi kopec',                           # Zadaný příkaz
          'Presunuli jste se do prostoru: kopec.\n'
          'Na kopci jste objevili horici vrak helikoptery.',
          'kopec',                                           # Aktuální prostor
          ('pole', ),                                        # Aktuální sousedé
          ('helikoptera',),                             # H-objekty v prostoru
          ('kompas', ),                                    # H-Objekty v batohu
    ),
    ScenarioStep(tsPUT_DOWN, 'poloz kompas',
          'Vyhodili jste kompas.',
          'kopec',
          ('pole',),
          ('helikoptera','kompas'),
          (),
    ),
    ScenarioStep(tsTAKE, 'vezmi kompas',
          'Sebrali jste kompas.',
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