#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Sada tříd deklarujících požadavky na jednotlivé součásti aplikace.

Definované (abstraktní) třídy:
    AAuthor(ABC)
    ANamed(ABC)
    AItem(ABC)
    AItemContainer(ABC)
    ABag(AItemContainer)
    APlace(AItemContainer, ANamed)
    AWorld(ABC)
    AAction(ABC)
    BasicCommands
    AGame(ABC)
    AFactory(AAuthor)

"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from abc            import ABC, abstractmethod
from collections    import namedtuple
from typing         import Union     #V# Od 3.10 nebude potřeba



############################################################################

class AAuthor(ABC):
    """Instance této třídy umějí na požádání vrátit
    jméno a identifikační řetězec autora/autorky své třídy.
    """

    @abstractmethod
    def authorName(self) -> str:
        """Vrátí jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
        tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
        u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
        Má-li autor programu více křestních jmen, může je uvést všechna.
        """

    @abstractmethod
    def authorID(self) -> str:
        """Vrátí identifikační řetězec autora/autorky programu
        zapsaný VELKÝMI PÍSMENY.
        Tímto řetězcem bývá login do informačního systému školy.
        """

    @abstractmethod
    def package(self) -> str:
        """Vrátí úplný název balíčku s kódem autorova řešení.
        Součástí jednoduchého názvu by mělo být autorovo ID a příjmení.
        """

    def __repr__(self) -> str:
        """Vrátí uživatelský textový podpis instance definovaný jako
        řetězec skládající se z ID autora následovaného jeho jménem.
        """
        return f'{self.authorID} - {self.authorName}'



############################################################################

class ANamed(ABC):
    """Instance představují objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Inicializuje objekt zadaným názvem.
        """
        super().__init__(**args)


    @property
    @abstractmethod
    def name(self) -> str:
        """Vrátí název daného objektu.
        """



############################################################################

class AItem(ANamed):
    """Instance představují h-objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Vytvoří h-objekt se zadaným názvem.
        """
        super().__init__(name, **args)


    @property
    @abstractmethod
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """



############################################################################

class AItemContainer(ABC):
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names:tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """
        super().__init__(**args)


    @abstractmethod
    def initialize(self):
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """


    @property
    @abstractmethod
    def items(self) -> list[AItem]:
        """Vrátí n-tici objektů v daném kontejneru.
        """


    @abstractmethod
    def item(self, name:str) -> AItem:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """


    @abstractmethod
    def add_item(self, item:AItem) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """


    @abstractmethod
    def remove_item(self, item_name:str) -> bool:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru
        a vrátí informaci o tom, jestli se to podařilo.
        """



############################################################################

class ABag(AItemContainer):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    def __init__(self, initial_item_names:tuple[str], **args):
        super().__init__(initial_item_names=initial_item_names, **args)


    @abstractmethod
    def initialize(self):
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """


    @property
    @abstractmethod
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """



############################################################################

class APlace(AItemContainer, ANamed):
    """Instance představují prostory, mezi nimiž hráč přechází.
    Prostory mohou být místnosti, planety, životní etapy atd.
    Prostory mohou obsahovat různé objekty,
    které mohou hráči pomoci v dosažení cíle hry.
    Každý prostor zná své aktuální bezprostřední sousedy
    a ví, jaké objekty se v něm v daném okamžiku nacházejí.
    Sousedé daného prostoru i v něm se nacházející objekty
    se mohou v průběhu hry měnit.
    """

    def __init__(self, name:str, description:str,
                 initial_neighbor_names:tuple[str],
                 initial_item_names    :tuple[str], **args
        ):
        super().__init__(name=name, initial_item_names=initial_item_names,
                         **args)


    @abstractmethod
    def initialize(self):
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """


    @property
    @abstractmethod
    def description(self) -> str:
        """Vrátí stručný popis daného prostoru.
        """


    @property
    @abstractmethod
    def neighbors(self) -> tuple['APlace']:
        """Vrátí n-tici aktuálních sousedů daného prostoru,
        tj. prostorů, do nichž je možno se z tohoto prostoru přesunout
        příkazem typu TypeOfStep.GOTO.
        """



############################################################################

class AWorld(ABC):
    """Instance vystupuje v roli správce světa hry a jeho prostorů.
    V dané hře musí být definována jako jedináček (např. modul).
    Má na starosti vzájemné propojení jednotlivých prostorů
    a udržuje informaci o tom, ve kterém z nich se hráč právě nachází.
    Vzájemné uspořádání prostorů se může v průběhu hry měnit –
    prostory mohou v průběhu hry získávat a ztrácet sousedy.
    """

    @abstractmethod
    def initialize(self):
        """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
        propojení jednotlivých prostorů a jejich výchozí obsah,
        nastaví výchozí aktuální prostor a inicializuje batoh.
        """

    @abstractmethod
    def current_place(self) -> APlace:
        """Vrátí odkaz na aktuální prostor,
        tj. na prostor, v němž se hráč pravé nachází.
        """

    @abstractmethod
    def places(self) -> tuple[APlace]:
        """Vrátí n-tici odkazů na všechny prostory ve hře
        včetně těch aktuálně nedosažitelných či neaktivních.
        """

    @abstractmethod
    def place(self, name:str) -> APlace:
        """Vrátí prostor se zadaným názvem. Pokud ve hře takový není,
        vrátí None.
        """



############################################################################

class AAction(ABC):
    """Instance mají na starosti interpretaci příkazů zadávaných uživatelem
    hrajícím hru. Název spouštěné akce je první slovo zadávaného příkazu;
    další slova pak jsou interpretována jako argumenty.

    Lze ale definovat i akci, která odstartuje konverzaci
    (např. s osobou přítomnou v místnosti) a tím systém přepne do režimu,
    v němž se zadávané texty neinterpretují jako příkazy,
    ale předávají se definovanému objektu až do chvíle, kdy bude rozhovor
    ukončen a hra se přepne zpět do režimu klasických příkazů.
    """

    @property
    @abstractmethod
    def description(self) -> str:
        """Vrátí popis příkazu s vysvětlením jeho funkce,
        významu jednotlivých parametrů a možností (resp. účelu) použití
        daného příkazu. Tento popis tak může sloužit jako nápověda
        k použití daného příkazu.
        """

    @abstractmethod
    def execute(self, arguments:tuple[str]) -> str:
        """Metoda realizující reakci hry na zadání daného příkazu.
        Předávané pole je vždy neprázdné, protože jeho nultý prvek
        je zadaný název vyvolaného příkazu. Počet argumentů je závislý
        na konkrétním akci, ale pro každou akci je konstantní.
        """



############################################################################

BasicActions = namedtuple('BasicActions',
    'MOVE_NAME PUT_DOWN_NAME TAKE_NAME HELP_NAME END_NAME')
BasicActions.__doc__ = """Přepravka s názvy povinných akcí."""



############################################################################

class AGame(ABC):
    """Instance má na starosti řízení hry a komunikaci s uživatelem.
    Je schopna akceptovat zadávané příkazy a poskytovat informace
    o průběžném stavu hry a jejích součástí.
    Hra musí být definována jako jedináček (singleton).
    """

    @abstractmethod
    def isAlive(self) -> bool:
        """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
        Spuštěnou hru není možno pustit znovu.
        Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
        """

    @abstractmethod
    def all_actions(self) -> tuple[AAction]:
        """Vrátí n-tici všech akcí použitelných ve hře.
        """

    @abstractmethod
    def basic_actions(self) -> BasicActions:
        """Vrátí přepravku s názvy povinných akcí.
        """

    @abstractmethod
    def bag(self) -> ABag:
        """Vrátí odkaz na batoh, do nějž bude hráč ukládat sebrané objekty.
        """

    @abstractmethod
    def world(self) -> AWorld:
        """Vrátí odkaz na svět hry.
        """

    @abstractmethod
    def execute_command(self, command:str) -> str:
        """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
        """

    @abstractmethod
    def stop(self):
        """Ukončí hru a uvolní alokované prostředky.
        Zadáním prázdného příkazu lze následně spustit hru znovu.
        """



############################################################################

class AFactory(AAuthor):
    """Instance představují tovární objekty,
    které na požádání dodají instance klíčových objektů aplikace,
    konkrétně aktuální hry, jejích scénářů a uživatelského rozhraní.
    """

    @abstractmethod
    def scenarios(self) -> tuple['Scenario']:
        """Vrátí n-tici definovaných scénářů.
        """


    def game(self) -> AGame:
        """Vrátí odkaz na objekt reprezentující hru.
        """
        raise Exception(f'Vlastnost game ještě není definována')


    def scenario(self, ID:Union[int, str]) -> 'Scenario':
        #V# Od 3.10 bude fungovat ID:(int | str)
        """Vrátí scénář se zadaným názvem nebo indexem.
        """
        if isinstance(ID, int):
            return self.scenarios()[ID]     # ==========>
        if isinstance(ID, str):
            for sc in self.scenarios():
                if ID==sc.name:   return ID # ==========>
        raise Exception(f'Zadaný argument neidentifikuje scénář: {ID}')



############################################################################
dbg.stop_mod (0, __name__)
