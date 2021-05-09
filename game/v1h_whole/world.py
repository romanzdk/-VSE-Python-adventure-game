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
    """Společný rodič všech tříd s pojmenovanými instancemi,
    v případě našich textových her je to rodič h-objektů, prostorů a akcí.
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
        return self.name
        # f'{self.__class__.__name__}:{self.name}'


    def __repr__(self):
        return '»' + self.name + '«'
        # f'{self.__class__.__name__}:{self.name}'



############################################################################

class Item(Named):
    """Instance představují h-objekty v prostorech či batohu.
    """

    HEAVY: int = 999    # Váha nepřenositelného h-objektu

    def __init__(self, name:str, **args):
        """Vytvoří h-objekt se zadaným názvem. Podle prvního znaku
        pozná přenositelnost objektu a nastaví jeho váhu.
        Zbylé znaky argumentu si zapamatuje jako jeho název.
        """
        prefix    = name[0]   # Předpona indikující další vlastnosti
        real_name = name[1:]  # Název h-objektu používaný v příkazech
        super().__init__(real_name)
        self._weight = 1 if prefix == '_' else Item.HEAVY


    @property
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """
        return self._weight



############################################################################

class ItemContainer():
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names:tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """
        super().__init__(**args)
        # Počáteční názvy se ukládají včetně prefixů, aby se při
        # inicializaci daly použít jako argumenty initoru
        self._initial_item_names = initial_item_names


    def initialize(self):
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů
        bez prefixů a převedených na malá písmena.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        # Následující dva atributy se vytvářejí až při první inicializaci
        self._items      = [Item(name) for name in self._initial_item_names]
        # Názvy se ukládají bez prefixů a převedené na malá písmena
        self._item_names = [item.name.lower() for item in self._items]


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
            result = self._items[self._item_names.index(name)]
            return result
        return None


    def add_item(self, item:AItem) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        self._items     .append(item)
        self._item_names.append(item.name.lower())
        return True


    def remove_item(self, item_name:str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru
        a vrátí informaci o tom, jestli se to podařilo.
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
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    # Kapacitu měříme počtem předmětů v batohu
    # Bylo by ji ale možno zobecnit na klasickou váhu, hmotnost apod.
    CAPACITY = 2    # Maximální kapacita batohu


    def __init__(self, initial_item_names:tuple[str], **args):
        super().__init__(initial_item_names=initial_item_names, **args)


    def initialize(self):
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """
        super().initialize()


    def add_item(self, item:AItem) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        # print(f'Batoh: {self.items}\n'
        #       f'Přidávám {item}, {item.weight=}')
        if len(self.items) + item.weight > _Bag.CAPACITY:
            # print('Je to plný')
            return False
        else:
            super().add_item(item)
            return True


    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """



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
        self._name2neighbor = {name:_NAME_2_PLACE[name] for name
                            in self.initial_neighbor_names}


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
        return tuple(self._name2neighbor.values())


    def neighbor(self, name:str) -> 'Place':
        """Vrátí sousední prostor se zadaným názvem. Nemá-li daný prostor
        souseda se zadaným názvem, vrátí None.
        """
        return self._name2neighbor.get(name.lower())



############################################################################

def initialize():
    """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
        propojení jednotlivých prostorů a jejich výchozí obsah,
        nastaví výchozí aktuální prostor a inicializuje batoh.
    """
    global _current_place
    for place in _NAME_2_PLACE.values(): place.initialize()
    BAG.initialize()
    _current_place = _NAME_2_PLACE['domeček']


def current_place() -> Place:
    """Vrátí odkaz na aktuální prostor,
    tj. na prostor, v němž se hráč pravé nachází.
    """
    return _current_place



def places() -> tuple[Place]:
    """Vrátí n-tici odkazů na všechny prostory ve hře
    včetně těch aktuálně nedosažitelných či neaktivních.
    """
    result = tuple(_NAME_2_PLACE.values())
    return result


def place(name:str) -> Place:
    """Vrátí prostor se zadaným názvem. Pokud ve hře takový není,
    vrátí None.
    """
    result = _NAME_2_PLACE.get(name.lower())
    return result



############################################################################

_NAME_2_PLACE = {p.name.lower() : p for p in (
    Place('Domeček',
          'Domeček, z nějž Karkulka vyráží za babičkou',
          ('Les', ),
          ('_Bábovka', '_Víno', '#Stůl', '_Panenka', ),
         ),
    Place('Les',
          'Les s jahodami, malinami a pramenem vody',
          ('Domeček', 'Temný_les', ),
          ('_Maliny', '_Jahody', '#Studánka', ),
         ),
    Place('Temný_les',
          'Temný_les s jeskyní a číhajícím vlkem',
          ('Les', 'Jeskyně', 'Chaloupka', ),
          ('#Vlk', )
         ),
    Place('Jeskyně',
          'Jeskyně, v níž přes zimu přespává medvěd',
          ('Temný_les',),
          ('_Kosti', '#Krápník', )
         ),
    Place('Chaloupka',
          'Chaloupka, kde bydlí babička',
          ('Temný_les',),
          ('#Postel', '#Stůl', '#Babička', ),
         ),
)}


############################################################################

# Aktuální prostor = prostor, v němž se hráč právě nachází
_current_place:Place

# Jediná instance batohu, v této hře batoh začíná jako prázdný
BAG = _Bag(())


############################################################################
dbg.stop_mod (0, __name__)
