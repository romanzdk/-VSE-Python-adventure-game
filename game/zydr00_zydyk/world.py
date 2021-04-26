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
    
    def __str__(self):
        return self._name


############################################################################

class Item(Named):
    """Instance představují h-objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Vytvoří h-objekt se zadaným názvem.
        """
        super().__init__(name, **args)

    @property
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """
        return self.weight

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


    def initialize(self):
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        self._item_names = [n.lower() for n in self._initial_item_names]
        self._items      = [Item(n)   for n in self._initial_item_names]


    @property
    def items(self) -> list[Item]:
        """Vrátí n-tici objektů v daném kontejneru.
        """
        return self._items[:]   # Vracím kopii, aby nikdo nemohl
                                # změnit její obsah

    def item(self, name:str) -> Item:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """
        name = name.lower()
        if name in self._item_names:
            return self._items[self._item_names.index(name)]
        return None


    def add_item(self, item:Item) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        self._items.append(item)
        self._item_names.append(item.name.lower())
        return True


    def remove_item(self, item_name:str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru
        a pokud se to podari, tak vrati objekt, jinak vrati None.
        """
        name = item_name.lower()
        if name in self._item_names:
            index = self._item_names.index(name)
            self._item_names.pop(index)
            result = self._items.pop(index)
            return result
        return None



############################################################################

class _Bag(ItemContainer):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    CAPACITY = 2    # Maximální kapacita batohu


    def __init__(self, initial_item_names:tuple[str], **args):
        super().__init__(initial_item_names=initial_item_names, **args)


    def initialize(self):
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """
        super().initialize()
        self.CAPACITY = 2


    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """
        return self.CAPACITY
    
    @property
    def items(self) -> list[Item]:
        return [Item(i) for i in self._initial_item_names]

    @items.setter
    def items(self, value) -> None:
        self._items = value
    

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
                 initial_item_names    :tuple[str], **args
        ):
        super().__init__(name=name, initial_item_names=initial_item_names,
                         **args)
        self._description = description
        self.initial_neighbor_names = [n.lower() for
                                       n in initial_neighbor_names]

    def initialize(self):
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """
        super().initialize()
        self._neighbors = [place(n) for n in self.initial_neighbor_names]
        self._items = [Item(i) for i in self._initial_item_names]


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
    
    @neighbors.setter
    def neighbors(self, value):
        self._neighbors = value

    
    @property
    def items(self) -> list[Item]:
        return tuple(self._items)
    
    @items.setter
    def items(self, value):
        self._items = value


############################################################################

def initialize():
    """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
        propojení jednotlivých prostorů a jejich výchozí obsah,
        nastaví výchozí aktuální prostor a inicializuje batoh.
    """
    global _current_place, _PLACES, BAG
    
    # inicializuj vsechny prostory
    for place in _PLACES:
        place.initialize()

    # nastav aktualni prvni prostor
    _current_place = _PLACES[0]

    # inicializuj batoh
    BAG.initialize()
    

def current_place() -> Place:
    """Vrátí odkaz na aktuální prostor,
    tj. na prostor, v němž se hráč pravé nachází.
    """
    global _current_place
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


############################################################################

_PLACES = (
    Place('pole',
          'Zde jste se probudili... Vedou odtud 4 cesty.',
          ('skaly', 'majak', 'jih', 'kopec',),
          ()
         ),
    Place('skaly',
          'U vysokych skal se nachazi hluboky temny les.\n'
          'Od lesa vychazi hruzostrasne vyti vlku...',
          ('pole', 'les',),
          ()
         ),
    Place('les',
          'Priblizujete se k lesu a slysite cim dal silnejsi vyti vlku.',
          ('skaly',),
          ()
         ),
    Place('kopec',
          'Na kopci jste objevili horici vrak helikoptery.',
          ('pole',),
          ('helikoptera', )
         ),
    Place('jih',
          'Nikde nic nablizku. Zadne znamky zachrany...',
          ('mlha','pole',),
          ()
         ),
    Place('mlha',
          'Zacina vam byt zima a v dohlednu se nic neobjevuje.',
          ('jih',),
          ()
         ),
    Place('majak',
          'U majaku se nachazi velka hala.',
          ('pole', 'hala'),
          ('dvere')
         ),
    Place('hala',
          'V hale jste nasli mimo jine velke pocitacove centrum.',
          ('majak'),
          ('pocitace')
         ),
)

_NAME_2_PLACE = {n.name.lower():n for n in _PLACES}


############################################################################

# Aktuální prostor = prostor, v němž se hráč právě nachází
_current_place: Place

# Jediná instance batohu, v této hře batoh začíná jako prázdný
BAG = _Bag(('kompas',))


############################################################################
dbg.stop_mod (0, __name__)
