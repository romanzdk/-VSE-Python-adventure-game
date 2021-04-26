#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Třídy definující typy scénářů a jejich kroků + jejich instance = typy.

Definované třídy:
    TypeOfScenario
    SubtypeOfStep(Enum) - 9 podtypů kroku scénáře
    TypeOfStep

Data:
    5 typů scénářů, názvy mají předponu st - st???
    40 typů kroku scénáře, názvy mají předponu ts - ts???
    ALL_TYPES        - Seznam všech definovaných typů kroků
    BASIC_TYPES      - Seznam povinných typů kroků
    HAPPY_TYPES      - Seznam typů kroků povinných ve scénáři HAPPY
    MISTAKE_TYPES    - Seznam typů kroků povinných ve scénáři MISTAKE
    MISTAKE_NS_TYPES - Seznam typů kroků povinných ve scénáři MISTAKE_NS

"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from enum import Enum


############################################################################

class TypeOfScenario:
    """Instance představují možné typy scénářů hry.
    """
    count = 0
    def __init__(self, description:str, purpose:str):
        self._ordinal     = TypeOfScenario.count;   TypeOfScenario.count+=1
        self._description = description
        self._purpose     = purpose

    ordinal     = property(lambda self: self._ordinal,
                           doc="Pořadí (index) scénáře mezi ostatními")
    description = property(lambda self: self._description,
                           doc="Charakteristika typu daného scénáře")
    purpose     = property(lambda self: self._purpose,
                           doc="Charakteristika obsahu daného scénáře")


############################################################################

stHAPPY       = TypeOfScenario(
                "základní úspěšný scénář",
                "úspěšné zvládnutí hry")
stMISTAKES    = TypeOfScenario(
                "základní chybový scénář",
                "reakce na chyby při zadávání základních příkazů")
stMISTAKES_NS = TypeOfScenario(
                "doplňkový chybový scénář",
                "reakce na chyby při zadávání rozšiřujících příkazů")
stGENERAL     = TypeOfScenario(
                "obecný testovatelný scénář",
                "alternativní možný testovatelný průběh hry")
stDEMO        = TypeOfScenario(
                "netestovatelný demonstrační scénář",
                "možný průběh hry pro simulace")


############################################################################

class SubtypeOfStep(Enum):
    """Podtyp typu kroku - subtype"""
    CORRECT     = 0 # Správně zadaný příkaz povinně zařazený do HAPPY
    HELP_STOP   = 1 # Správně zadaný povinný příkaz HELP či STOP
    MISTAKE     = 2 # Povinně testovaný chybně zadaný příkaz
    NONSTANDARD = 3 # Správně zadaný rozšiřující příkaz
    MISTAKE_NS  = 4 # Povinný test rozšiřujícího příkazu
    DIALOG      = 5 # Součást rozhovoru
    DEMO        = 6 # Demonstrační krok bez doprovodných informací,
                    # který proto nelze použít k testu funkce hry
    MODIFIED    = 7 # Typ používaný v modifikačních zadáních v obhajobách
    UNDEFINED   = 8 # Typ kroků vytvořených pro pomocné operace,
                    # a nesmí se proto vyskytnout v žádném scénáři



############################################################################

class TypeOfStep:
    """Mateřská třída typů kroků scénáře.
    """
    def __init__(self, subtype:SubtypeOfStep, param_count:int,
                 group:'TypeOfStep', name:str, doc:str, extended=False):
        """Definuje nový typ kroku, přičemž argument subtype definuje podtyp,
        arg_count požadovaný počet parametrů
        a group skupinu typů příkazů spouštějících shodnou akci.
        """
        self._subtype     = SubtypeOfStep(subtype)
        self._param_count = param_count
        self._group       = self if group==None else group
        self.__name__     = name
        self.__doc__      = doc
        self._append(extended)

    subtype   = property(lambda self: self._subtype,
                doc='Podtyp kroku')
    arg_count = property(lambda self: self._param_count,
                doc='Počet argumentů v krocích daného typu')
    group     = property(lambda self: self._group,
                doc='Skupina typů spouštějících shodnou akci')
    name      = property(lambda self: self.__name__,
                doc='Název daného typu kroku a příslušné proměnné')
    def __repr__(self): return self.__name__

    def __str__(self):
        return self.__name__

    def __repr__(self):
    #     return TypeOfStep.__name__ + '.' + self.__name__
    #
    # def __str__(self):
        return self.__name__

    def _append(self, extended:bool):
        """Přidá odkaz na daný typ do příslušných kontejnerů.
        """
        global ALL_TYPES, BASIC_TYPES, HAPPY_TYPES
        global MISTAKE_TYPES, MISTAKE_NS_TYPES
        if extended:
            # Při definici rozšiřujících typů byly již základní kontejnery
            # naplněny a naplňování jejich kontejnerů má na starosti
            #funkce create_extended_types_for(), která je vytváří
            return
        else:
            # Základní typy akcí, kontejnery jsou seznamy
            ALL_TYPES.append(self)
            st = self._subtype
            if st == SubtypeOfStep.CORRECT:
                BASIC_TYPES.append(self)
                HAPPY_TYPES.append(self)
            elif st == SubtypeOfStep.NONSTANDARD:
                if self.__name__ != 'NS_3':
                    HAPPY_TYPES.append(self)
                    NS_TYPES   .append(self)
            elif st == SubtypeOfStep.HELP_STOP:
                BASIC_TYPES  .append(self)
                MISTAKE_TYPES.append(self)
            elif st == SubtypeOfStep.MISTAKE:
                MISTAKE_TYPES.append(self)
            elif st == SubtypeOfStep.MISTAKE_NS:
                MISTAKE_NS_TYPES.append(self)
            elif st in {SubtypeOfStep.DEMO, SubtypeOfStep.DIALOG,
                        SubtypeOfStep.MODIFIED, SubtypeOfStep.UNDEFINED}:
                "Nedělá se nic"
            else:
                raise Exception(f'Neznámý podtyp kroku: {self} -> {st=}')


def clear_extended_types():
    """Volá se na počátku testu scénářů a vyčistí kontejnery typů
    dodatečně definovaných pro nadstandardní akce při testu scénářů,
    čímž smaže i všechny odkazy na tyto typy.
    """
    EXTEND_NS_TYPES.clear()    # Typy s názvem nadstandardní akce
    EXTEND_MISTAKES.clear()    # Chybové typy s názvem ns akce


def create_extended_types_for(action:str, group:TypeOfStep) -> TypeOfStep:
    """Vytvoří skupinu typů kroku svázaných s akcí se zadaným názvem
    patřící do základní skupiny definované argumentem group,
    Do vytvářené skupiny zařadí jak základní typ, tak příslušné chybové typy.
    Vrátí základní typ sdružený s danou akcí a reprezentující tak
    její novou skupinu.
    """
    a_   = action + '_'
    args = group.arg_count   # Počet argumentů zadané akce
    tos = TypeOfStep(SubtypeOfStep.NONSTANDARD, args, None,
                     a_ + group.name, # Název rozšířeného typu
                     f'Typ {group} pro akci {action}',
                     extended = True
          )
    EXTEND_NS_TYPES.add(tos)
    for type in _required_ns_err[args]:
        extended_type = TypeOfStep(SubtypeOfStep.MISTAKE_NS,
                             type.arg_count,    # Počet argumentů
                             tos,               # Skupina
                             a_ + type.name,    # Název rozšířeného typu
                             f'Typ {type} pro akci {action}',
                             extended = True
                        )
        EXTEND_MISTAKES.add(extended_type)



############################################################################

ALL_TYPES        = []  # Seznam všech definovaných typů kroků
BASIC_TYPES      = []  # Seznam povinných typů kroků
NS_TYPES         = []  # Základní typy nadstandardních (ns) akcí
HAPPY_TYPES      = []  # Seznam typů kroků povinných ve scénáři HAPPY
MISTAKE_TYPES    = []  # Seznam typů kroků povinných ve scénáři MISTAKE
MISTAKE_NS_TYPES = []  # Seznam typů kroků povinných ve scénáři MISTAKE_NS


def print_step_types():
    """Vytiskne povinné typy kroků roztříděné podle cílových scénářů.
    """
    _print_tuple(HAPPY_TYPES, 'HAPPY')
    _print_tuple(MISTAKE_TYPES, 'MISTAKE')
    _print_tuple(MISTAKE_NS_TYPES, 'MISTAKE_NS')


def _print_tuple(types:tuple, description:str):
    """Vytiskne popisek následovaný prvky zadané n-tice
    každý na samostatný řádek.
    """
    print(f'Typy kroků povinně přítomné ve scénáři {description}')
    for t in types:
        print(f'   {str(t):16s} - {t.__doc__}')



############################################################################

#Typ kroku neurčeného pro zařazení do nějakého scénáře,
#ale pouze pro doplnění chybového hlášení a pomocné akce
tsNOT_SET         =TypeOfStep(8, -1, None, 'tsNOT_SET',
                  "Typ kroku pro chybová hlášení a pomocné akce")

#Typy řádných kroků, které se musí objevit v základním úspěšném scénáři
tsSTART           =TypeOfStep(0, -1, None, 'tsSTART',
                  "Startovací krok s prázdným názvem")
tsGOTO            =TypeOfStep(0, 1, None, 'tsGOTO',
                  "Úspěšný přesun do sousedního prostoru")
tsTAKE            =TypeOfStep(0, 1, None, 'tsTAKE',
                  "Úspěšné zvednutí objektu v prostoru")
tsPUT_DOWN        =TypeOfStep(0, 1, None, 'tsPUT_DOWN',
                  "Úspěšné položení objektu z batohu")

#Následující typy kroků musí být otestovány v základním chybovém scénáři
tsEND             =TypeOfStep(1, 0, None, 'tsEND',
                  "Příkaz okamžitě ukončující hru")
tsHELP            =TypeOfStep(1, 0, None, 'tsHELP',
                  "Nápověda")

#Problémy se správným zadáním příkazu
tsNOT_START       =TypeOfStep(2, -1, None, 'tsNOT_START',
                  "Startovací příkaz není prázdný string")
tsEMPTY           =TypeOfStep(2, -1, tsSTART, 'tsEMPTY',
                  "NE-startovací zadání prázdného stringu")
tsUNKNOWN         =TypeOfStep(2, -1, None, 'tsUNKNOWN',
                  "Zadání neznámé akce")

#Vyvolání některé ze základních akcí bez povinného parametru
tsMOVE_WA         =TypeOfStep(2, 0, tsGOTO, 'tsMOVE_WA',
                  "Nebylo zadáno, kam se přesunout")
tsTAKE_WA         =TypeOfStep(2, 0, tsTAKE, 'tsTAKE_WA',
                  "Nebylo zadáno, co se má zvednout")
tsPUT_DOWN_WA     =TypeOfStep(2, 0, tsPUT_DOWN, 'tsPUT_DOWN_WA',
                  "Nebylo zadáno, co se má položit")

#Problémy se změnou místnosti
tsBAD_NEIGHBOR    =TypeOfStep(2, 1, tsGOTO, 'tsBAD_NEIGHBOR',
                  "Cílový prostor není sousedem aktuálního")

#Problémy se zvednutím či položením předmětu
tsBAD_ITEM        =TypeOfStep(2, 1, tsTAKE, 'tsBAD_ITEM',
                  "Zadaný předmět v prostoru není")
tsUNMOVABLE       =TypeOfStep(2, 1, tsTAKE, 'tsUNMOVABLE',
                  "Zadaný předmět nelze zvednout")
tsBAG_FULL        =TypeOfStep(2, 1, tsTAKE, 'tsBAG_FULL',
                  "Zadaný předmět se nevejde do batohu")
tsNOT_IN_BAG      =TypeOfStep(2, 1, tsPUT_DOWN, 'tsNOT_IN_BAG',
                  "Zadaný předmět v batohu není")

#Typy rozšiřujících kroků
tsNS_0            = TypeOfStep(3, 0, None, 'tsNS_0',
                  "Úspěšná bezparametrická rozšiřující akce")
tsNS_1            = TypeOfStep(3, 1, None, 'tsNS_1',
                  "Úspěšná jednoparametrická rozšiřující akce")
tsNS_2            = TypeOfStep(3, 2, None, 'tsNS_2',
                  "Úspěšná dvouparametrická rozšiřující akce")
tsNS_3            = TypeOfStep(3, 3, None, 'tsNS_3',
                  "Úspěšná tříparametrická rozšiřující akce")
tsNS0_WrongCond   = TypeOfStep(4, 0, tsNS_0, 'tsNS0_WrongCond',
                  "Neproveditelná bezparametrická rozšiřující akce")
tsNS1_WrongCond   = TypeOfStep(4, 1, tsNS_1, 'tsNS1_WrongCond',
                  "Neproveditelná jednoparametrická rozšiřující akce")
tsNS2_WrongCond   = TypeOfStep(4, 2, tsNS_2, 'tsNS2_WrongCond',
                  "Neproveditelná dvouparametrická rozšiřující akce")
tsNS3_WrongCond   = TypeOfStep(4, 2, tsNS_3, 'tsNS3_WrongCond',
                  "Neproveditelná tříparametrická rozšiřující akce")
tsNS1_0Args       = TypeOfStep(4, 0, tsNS_1, 'tsNS1_0Args',
        "Jednoparametrická rozšiřující akce s nezadaným argumentem")
tsNS2_1Args       = TypeOfStep(4, 1, tsNS_2, 'tsNS2_1Args',
        "Dvouparametrická rozšiřující akce s malým počtem zadaných argumentů")
tsNS3_012Args     = TypeOfStep(4, 2, tsNS_3, 'tsNS3_012Args',
        "Tříparametrická rozšiřující akce s malým počtem zadaných argumentů")
tsNS1_WRONG_ARG   = TypeOfStep(4, 1, tsNS_1, 'tsNS1_WRONG_ARG',
        "Jednoparametrická rozšiřující akce se špatným argumentem")
tsNS2_WRONG_1stARG= TypeOfStep(4, 2, tsNS_2, 'tsNS2_WRONG_1stARG',
        "Dvouparametrická rozšiřující akce s nevhodným prvním argumentem")
tsNS2_WRONG_2ndARG= TypeOfStep(4, 2, tsNS_2, 'tsNS2_WRONG_2ndARG',
        "Dvouparametrická rozšiřující akce s nevhodným druhým argumentem")
tsNS3_WRONG_1stARG= TypeOfStep(4, 3, tsNS_3, 'tsNS3_WRONG_1stARG',
        "Tříparametrická rozšiřující akce s nevhodným prvním argumentem")
tsNS3_WRONG_2ndARG= TypeOfStep(4, 3, tsNS_3, 'tsNS3_WRONG_2ndARG',
        "Tříparametrická rozšiřující akce s nevhodným druhým argumentem")
tsNS3_WRONG_3rdARG= TypeOfStep(4, 3, tsNS_3, 'tsNS3_WRONG_3rdARG',
        "Tříparametrická rozšiřující akce s nevhodným třetím argumentem")

#Typy kroku nepoužitelných pro testování reakce hry na zadaný příkaz
tsDIALOG          =TypeOfStep(5, -1, None, 'tsDIALOG',
        "Krok je součástí rozhovoru nebo nějaké obdobné činnosti")
tsDEMO            =TypeOfStep(6, -1, None, 'tsDEMO',
        "Netestovatelný krok určený pouze pro předvedení funkce hry")

#Typy kroku používané v modifikačních zadáních při obhajobách
tsMOD_A           =TypeOfStep(7, -1, None, 'tsMOD_A',
        "Modifikační krok používaný při obhajobách")
tsMOD_B           =TypeOfStep(7, -1, None, 'tsMOD_B',
        "Modifikační krok používaný při obhajobách")
tsMOD_C           =TypeOfStep(7, -1, None, 'tsMOD_C',
        "Modifikační krok používaný při obhajobách")



############################################################################

_required_ns_err = (
        (tsNS0_WrongCond, ),
        (tsNS1_0Args, tsNS1_WrongCond, tsNS1_WRONG_ARG),
        (tsNS2_1Args, tsNS2_WrongCond, tsNS2_WRONG_1stARG,
                                       tsNS2_WRONG_2ndARG),
        (tsNS3_012Args, tsNS3_WRONG_1stARG, tsNS3_WRONG_2ndARG,
                        tsNS3_WRONG_3rdARG)
)



############################################################################
HAPPY_TYPES.remove(tsNS_3)

#Množiny typů kroků povinně použitých v různých typech scénářů
ALL_TYPES        = frozenset(ALL_TYPES)     # Všechny typy
BASIC_TYPES      = frozenset(BASIC_TYPES)   # Povinné akce
NS_TYPES         = frozenset(NS_TYPES)      # Základní typy ns akcí
HAPPY_TYPES      = frozenset(HAPPY_TYPES)   # Povinné ve šťastném scénáři
MISTAKE_TYPES    = frozenset(MISTAKE_TYPES) # Povinné v chybovém scénáři
MISTAKE_NS_TYPES = frozenset(MISTAKE_NS_TYPES)#Povinné v chybovém NS scénáři

EXTEND_NS_TYPES  = set()    # Typy s názvem nadstandardní akce
EXTEND_MISTAKES  = set()    # Chybové typy s názvem ns akce



############################################################################
dbg.stop_mod (0, __name__)
