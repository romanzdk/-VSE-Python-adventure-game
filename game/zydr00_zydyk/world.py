#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#Q:/65_PGM/65_PYT/game/game_v1a/world.py
"""
Modul world reprezentuje svět hry a obsahuje definice tříd prostorů,
předmětů (h-objektů) a batohu. Sám vystupuje v roli jejich správce.
Má na starosti uspořádání a vzájemné propojení jednotlivých prostorů
a udržuje informaci o tom, ve kterém z nich se hráč právě nachází.
Vzájemné uspořádání prostorů se může v průběhu hry měnit –
prostory mohou v průběhu hry získávat a ztrácet sousedy.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from ..api.game_types import *

############################################################################

class Named():
    """Instance představují objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Inicializuje objekt zadaným názvem.
        """
        super().__init__(**args)
        self._name = name

    @property
    def name(self) -> str:
        """Vrátí název daného objektu.
        """
        return self._name
    
    def __str__(self) -> str:
        """Vrátí název daného objektu.
        """
        return self.name

    def __repr__(self) -> str:
        """Vrátí název daného objektu.
        """
        return '»' + self.name + '«'

############################################################################

class Item(Named):
    """Instance představují h-objekty v prostorech či batohu.
    """

    def __init__(self, name:str, is_pickable:bool,
                 description:str, item_names_to_unhide:tuple[str], 
                 can_be_used_on:tuple[str], text_when_used:str, 
                 ends_game_when_used:bool, **args):
        """Vytvoří h-objekt se zadaným názvem.
        """
        super().__init__(name, **args)
        self._is_pickable = is_pickable
        self._description = description
        self._item_names_to_unhide = item_names_to_unhide
        self._can_be_used_on = can_be_used_on
        self._text_when_used = text_when_used
        self._ends_game_when_used = ends_game_when_used
        
    def initialize(self) -> None:
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """
        names = self._item_names_to_unhide
        self._items_to_unhide = [item(i) for i in names]
        self._is_explored = False

    @property
    def is_pickable(self) -> bool:
        """Vrátí informaci o tom, zda se dá daný předmět zvednout.
        """
        return self._is_pickable
    
    @property
    def description(self) -> str:
        """Vrátí stručný popis daného předmětu.
        """
        return self._description
    
    @property
    def items_to_unhide(self) -> list[AItem]:
        """Vrátí seznam předmětů, které se v prostoru odkryjí po prozkoumání.
        """
        return self._items_to_unhide
    
    @property
    def is_explored(self) -> bool:
        """Vrátí informaci o tom, zda je daný předmět prozkoumaný.
        """
        return self._is_explored
    
    @is_explored.setter
    def is_explored(self, value) -> None:
        """Nastaví prozkoumanost předmětu.
        """
        self._is_explored = value
    
    @property
    def can_be_used_on(self) -> list[AItem]:
        """Vrátí seznam předmětů, na které lze daný předmět použít.
        """
        return self._can_be_used_on
    
    @property
    def text_when_used(self) -> str:
        """Vrátí popis, který se vypíše po použití daného předmětu"""
        return self._text_when_used
    
    @property
    def ends_game_when_used(self) -> bool:
        """Vrátí informaci o tom, zda použití předmětu ukončí hru"""
        return self._ends_game_when_used

############################################################################

class ItemContainer():
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names:tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """
        super().__init__(**args)
        self._initial_item_names = initial_item_names


    def initialize(self) -> None:
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        self._item_names = [n.lower() for n in sorted(self._initial_item_names)]
        self._items = [item(n) for n in sorted(self._initial_item_names)]

    @property
    def items(self) -> tuple[Item]:
        """Vrátí n-tici objektů v daném kontejneru.
        """
        return tuple(self._items)

    @property
    def item_names(self) -> tuple[str]:
        """Vrátí n-tici názvů objektů v daném kontejneru.
        """
        return tuple(self._item_names)
    
    def item(self, name:str) -> Item:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """
        name = name.lower()
        if name in self._item_names:
            return self._items[self._item_names.index(name)]
        return None


    def add_item(self, item:Item) -> None:
        """Přidá zadaný objekt do kontejneru.
        """
        self._items.append(item)
        self._item_names.append(item.name.lower())

    def remove_item(self, item_name:str) -> bool:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru
        a pokud se to podaří, tak vrátí objekt, jinak vrátí None.
        """
        name = item_name.lower()
        if name in self._item_names:
            index  = self._item_names.index(name)
            name   = self._item_names.pop(index)
            result = self._items     .pop(index)
            return result
        return None

############################################################################

class _Bag(ItemContainer):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující počet objektů.
    """

    CAPACITY = 3    # Maximální kapacita batohu

    def __init__(self, initial_item_names:tuple[str], **args):
        super().__init__(initial_item_names=initial_item_names, **args)

    def initialize(self) -> None:
        """Inicializuje batoh na počátku hry.
        """
        super().initialize()

    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """
        return self.CAPACITY
    
    @property
    def free(self) -> int:
        """Vrátí volnou kapacitu batohu.
        """
        return self.CAPACITY - len(self._items)
    
############################################################################

class Place(ItemContainer, Named):
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
                 initial_item_names    :tuple[str], 
                 will_kill:bool, **args
        ):
        super().__init__(name=name, initial_item_names=initial_item_names,
                         **args)
        self._description = description
        self._initial_neighbor_names = [n.lower() for
                                       n in initial_neighbor_names]
        self._will_kill = will_kill

    def initialize(self) -> None:
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů v prostoru.
        """
        super().initialize()
        self._neighbors = [place(n) for n in self._initial_neighbor_names]

    @property
    def description(self) -> str:
        """Vrátí stručný popis daného prostoru.
        """
        return self._description

    @property
    def neighbors(self) -> tuple[APlace]:
        """Vrátí n-tici aktuálních sousedů daného prostoru,
        tj. prostorů, do nichž je možno se z tohoto prostoru přesunout
        příkazem typu TypeOfStep.GOTO.
        """
        return tuple(self._neighbors)
    
    @property
    def will_kill(self) -> bool:
        """Vrátí informaci o tom, zda hráč zemře, když do prostoru vstoupí.
        """
        return self._will_kill

############################################################################

def initialize() -> None:
    """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
        propojení jednotlivých prostorů a jejich výchozí obsah,
        nastaví výchozí aktuální prostor a inicializuje batoh.
    """
    global _current_place
    
    # inicializuj všechny předměty
    for item in _ITEMS:
        item.initialize()

    # inicializuj všechny prostory
    for place in _PLACES:
        place.initialize()

    # nastav aktuální první prostor
    _current_place = _PLACES[0]

    # inicializuj batoh
    BAG.initialize()
    
def current_place() -> Place:
    """Vrátí odkaz na aktuální prostor,
    tj. na prostor, v němž se hráč pravé nachází.
    """
    return _current_place

def places() -> tuple[Place]:
    """Vrátí n-tici odkazů na všechny prostory ve hře
    včetně těch aktuálně nedosažitelných či neaktivních.
    """
    return _PLACES

def place(name:str) -> Place:
    """Vrátí prostor se zadaným názvem. Pokud ve hře takový není,
    vrátí None.
    """
    return _NAME_2_PLACE.get(name)

def item(name:str) -> Item:
    """Vrátí předmět se zadaným názvem. Pokud ve hře takový není,
    vrátí None.
    """
    return _NAME_2_ITEM.get(name)

############################################################################

#n-tice všech předmětů ve hře
_ITEMS = (
    Item('helikoptera',                                         #nazev
        False,                                                  #je zvednutelny
        'Našli jste tyto věci: mobil, mapu, flash_disk a naradi.',
        ('mobil', 'mapa', 'flash_disk','naradi',),              #odhali veci
        (),                                                     #pouzit na
        '',                                                     #text po pouziti
        False                                                   #ukonci hru?
    ),
    Item('mobil', 
        True,
        'Telefon je bohužel rozbitý a tak je k ničemu.',
        (), 
        (),
        '',
        False
    ),
    Item('kompas',
        True,
        'Funkční kompas.',
        (), 
        ('mapa',),
        '',
        False
    ),
    Item('mapa',
        True,
        'Na mapě vidíte načrtnutou lebku v lese a maják. '
        'Zbytek mapy je ohořelý.',
        (),
        (),
        'Díky kompasu jste zjistili, kde jsou světové strany.',
        False
    ),
    Item('flash_disk', 
        True,
        'Obyčejná flashka. Její obsah bohužel nejste schopni zjistit.',
        (),
        ('pocitace',),
        '',
        True
    ),
    Item('naradi', 
        False,
        'Nářadí je zaklíněno pod troskami helikoptéry.',
        (),
        (),
        '',
        False
    ),
    Item('pocitace', 
        False,
        'Počítač vyžaduje zadání přístupových údajů.',
        (),
        (),
        'Použili jste: flash_disk na: pocitace.\n'
        'Flash disk jste připojili k počítači.\n'
        '...\n'
        'Úspěšně jste se díky obsahu na flashce dostali do počítačů...\n'
          'Nyní si můžete zavolat pomoc a budete zachráněni...'
          'Gratuluji, vyhráli jste!',
        False
    ),
    Item('dvere', 
        False,
        'Dveře jsou bohužel zamčené a nejdou otevřít.',
        (),
        (),
        '',
        False
    ),
)

#slovník názvů předmětů a jejich objektů
_NAME_2_ITEM = {n.name.lower():n for n in _ITEMS}

#všechny prostory nacházející se ve hře
_PLACES = (
    Place('pole',
          'Zde jste se probudili... Vedou odtud 4 cesty.',
          ('skaly', 'majak', 'jih', 'kopec',),
          (),
          False
         ),
    Place('skaly',
          'U vysokých skal se nachází hluboký temný les.\n'
          'Od lesa vychází hrůzostrašné vytí vlků...',
          ('pole', 'les',),
          (),
          False
         ),
    Place('les',
          'Přibližujete se k lesu a slyšíte čím dál silnější vytí vlků.\n...'
          '\n...\nVykot se rázem změnil v agresivní chrčení.\n...\n... \n'
          'Snažíte se zachránit útěkem před smečkou hladových vlků.\n...\n...'
          '\nBohužel vlci vás dohnali a sežrali.',
          ('skaly',),
          (),
          True
         ),
    Place('kopec',
          'Na kopci jste objevili hořící vrak helikoptéry.',
          ('pole',),
          ('helikoptera', ),
          False
         ),
    Place('jih',
          'Nikde nic nablízku. Žádné známky záchrany...',
          ('mlha','pole',),
          (),
          False
         ),
    Place('mlha',
          '\Začíná vám být zima a v dohlednu se nic neobjevuje.\n...\n...\n'
          'Příšerná zima.\n...\n... \nBohužel jste umrzli zimou.',
          ('jih',),
          (),
          True
         ),
    Place('majak',
          'U majáku se nachází velká hala.',
          ('pole', 'hala'),
          ('dvere',),
          False
         ),
    Place('hala',
          'V hale jste našli mimo jiné velké počítačové centrum.',
          ('majak',),
          ('pocitace',),
          False
         ),
)

#slovník názvů prostorů a jejich objektů
_NAME_2_PLACE = {n.name.lower():n for n in _PLACES}


############################################################################

# Aktuální prostor = prostor, v němž se hráč právě nachází
_current_place: Place

# Jediná instance batohu, v této hře batoh začíná jako prázdný
BAG = _Bag(('kompas',))


############################################################################
# dbg.stop_mod (0, __name__)
