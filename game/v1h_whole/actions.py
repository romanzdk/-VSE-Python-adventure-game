#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul action má na starosti zpracování příkazů.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from abc import abstractmethod

from .      import world
from .world import current_place, BAG
from .world import initialize as world_initialize


############################################################################

def is_active() -> bool:
    """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return _is_active


def execute_command(command:str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """
    command = command.strip()
    if _is_active:
        # Hra běží, reagujeme na zadaný příkaz
        if command == '':
            return 'Prázdný příkaz lze použít pouze pro start hry'
        else:
            words       = command.split()
            action_name = words[0].lower()
            action      = _NAME_2_ACTION.get(action_name)
            if not action:
                return f'Tento příkaz neznám: {words[0]}'
            answer = action.execute(words)
            return answer

    else:   # Hra neběží, musí se odstartovat
        if command == '':
            return _start_game()
        else:
            return ('Prvním příkazem není startovací příkaz.\n' 
                    'Hru, která neběží, lze spustit '
                    'pouze startovacím příkazem.\n')


def stop():
    """Ukončí aktuální běn hry.
    """
    _is_active = False



############################################################################

class AAction(world.Named):
    """Instance mají na starosti interpretaci příkazů zadávaných uživatelem
    hrajícím hru. Název spouštěné akce je první slovo zadávaného příkazu;
    další slova pak jsou interpretována jako argumenty.

    Lze ale definovat i akci, která odstartuje konverzaci
    (např. s osobou přítomnou v místnosti) a tím systém přepne do režimu,
    v němž se zadávané texty neinterpretují jako příkazy,
    ale předávají se definovanému objektu až do chvíle, kdy bude rozhovor
    ukončen a hra se přepne zpět do režimu klasických příkazů.
    """

    def __init__(self, name:str, description:str):
        super().__init__(name)
        self._description = description


    @property
    def description(self) -> str:
        """Vrátí popis příkazu s vysvětlením jeho funkce,
        významu jednotlivých parametrů a možností (resp. účelu) použití
        daného příkazu. Tento popis tak může sloužit jako nápověda
        k použití daného příkazu.
        """
        return self._description


    @abstractmethod
    def execute(self, arguments:tuple[str]) -> str:
        """Metoda realizující reakci hry na zadání daného příkazu.
        Předávané pole je vždy neprázdné, protože jeho nultý prvek
        je zadaný název vyvolaného příkazu. Počet argumentů je závislý
        na konkrétním akci, ale pro každou akci je konstantní.
        """



############################################################################

class End(AAction):
    """Předčasně ukončí hru.
    """
    def __init__(self):
        super().__init__('KONEC',
                         'Předčasně ukončí hru')


    def execute(self, arguments:tuple[str]) -> str:
        global _is_active
        _is_active = False
        return 'Ukončili jste hru.\nDěkujeme, že jste si zahráli.'



class Goto(AAction):
    """Řeší přesun hráče do zadaného sousedního prostoru.
    """
    def __init__(self):
        super().__init__('Jdi',
                         'Přesune se do zadaného sousedního prostoru')


    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, kam mám jít.\n'
                    'Je třeba zadat jméno cílového prostoru.')
        place_name = arguments[1].lower()
        place      = world.place(place_name)
        if (not place) or (not place in current_place().neighbors):
            return f'Do zadaného prostoru se odsud jít nedá: {place_name}.'
        world._current_place = place
        return f'Karkulka se přesunula do prostoru:\n{place.description}'



class Help(AAction):
    """Předčasně ukončí hru.
    """
    def __init__(self):
        super().__init__('?', 'Nápověda')

    def execute(self, arguments:tuple[str]) -> str:
        hlp = [action.name + ' - ' + action.description
               for action in _NAME_2_ACTION.values()]
        # print(f'{type(hlp) = }')
        # dbg.prItLh(hlp, 'Nápovědní texty:', '   ')
        message = (
            'Tvým úkolem je dovést Červenou Karkulku z domečku\n'
            'až k babičce, která bydlí v chaloupce za lesem.\n'
            'Můžeš zadat tyto příkazy:\n'
          + '\n'.join(hlp)
            )
        return message



class Put_down(AAction):
    """Řeší přesun předmětu z batohu do prostoru.
    """
    def __init__(self):
        super().__init__('Polož',
                         'Přesune předmět z batohu do aktuálního prostoru')

    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, co mám položit.\n'
                    'Je třeba zadat jméno pokládaného objektu.')
        item_name = arguments[1].lower()
        item      = BAG.remove_item(item_name)
        if not item:
            return f'Zadaný objekt v košíku není: {item_name}'
        current_place().add_item(item)
        return f'Karkulka vyndala z košíku objekt: {item.name}'


class Take(AAction):
    """Řeší přesun předmětu z aktuálního prostoru do batohu.
    """
    def __init__(self):
        super().__init__('Vezmi',
                         'Přesune předmět z aktuálního prostoru do batohu')

    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, co mám zvednout.\n'
                    'Je třeba zadat jméno zvedaného objektu.')
        item_name = arguments[1]
        item      = current_place().remove_item(item_name)
        if not item:
            return f'Zadaný objekt v prostoru není: {item_name}'
        if item.weight == world.Item.HEAVY:
            current_place().add_item(item)
            return f'Zadaný objekt není možno zvednout: {item.name}'
        if BAG.add_item(item):
            return f'Karkulka dala do košíku objekt: {item.name}'
        else:
            return f'Zadaný objekt se už do košíku nevejde: {item.name}'



############################################################################

class Wake_up(AAction):
    """Řeší probuzení zadaného tvora, nejlépe babičky.
    """
    def __init__(self):
        super().__init__('Probuď',
                         'Probudí zadaného tvora; ten musí spát '
                         'v aktuálním prostoru,')

    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, koho mám probudit.\n'
                    'Je třeba zadat jméno buzeného objektu.')
        item_name = arguments[1]
        item      = current_place().item(item_name)
        if not item:
            return f'Nelze budit objekt, který není přítomen: {item_name}'
        item_name = item_name.lower()
        if item_name not in _AWAKE:
            return f'Nelze budit předmět: {item.name}'
        if _AWAKE[item_name]:
            return f'Nelze budit osobu, která je již probuzená: {item_name}'
        _AWAKE[item_name] = True
        return f'Karkulka probudila osobu: {item_name}'



class Greet(AAction):
    """Řeší podravení probuzených osob.
    """
    def __init__(self):
        super().__init__('Pozdrav',
                         'V aktuálním prostoru pozdraví probuzeného tvora')

    def execute(self, arguments:tuple[str]) -> str:
        cp = current_place()
        for item in cp.items:
            if (low_name:=item.name.lower()) in _AWAKE:
                break
        else:
            return 'Není koho zdravit'
        if not _AWAKE[low_name]:
            return (f'Nemá smysl zdravit, {low_name} ještě není '
                    f'{"probuzená" if low_name=="babička" else "probuzený"}.')
        _GREETED[low_name] = True
        return (f'Karkulka pozdravila '
                f'{"babičku" if low_name=="babička" else "vlka"}.')



class Wish(AAction):
    """Řeší popřání probuzenému tvoru k narozeninám.
    """
    def __init__(self):
        super().__init__('Popřej',
                         'Popřeje probuzenému tvoru k narozeninám')

    def execute(self, arguments:tuple[str]) -> str:
        cp = current_place()
        for item in cp.items:
            if (low_name:=item.name.lower()) in _AWAKE:
                break
        else:
            return 'Není komu popřát'
        if not _AWAKE[low_name]:
            return (f'Nemá smysl přát, {low_name} ještě není '
                    f'{"probuzená" if low_name=="babička" else "probuzený"}.')
        # Ověří, že cíl předání již byl pozdraven
        if not _GREETED[low_name]:
            return (f'Karkulka ještě '
                    f'{"babičku" if low_name=="babička" else "vlka"} '
                    f'nepozdravila.')
        _WISHED[low_name] = True
        return (f'Karkulka popřála '
                f'{"babičce" if low_name=="babička" else "vlkovi"} '
                f'vše nejlepší k narozeninám')



class Give(AAction):
    """Řeší pozdravení probuzených osob.
    """
    def __init__(self):
        super().__init__('Předej',
                         'Předá probuzenému tvoru dva dárky k narozeninám')

    def execute(self, arguments:tuple[str]) -> str:
        # Ověří dostatečný počet argumentů
        if len(arguments) < 3:
            msg = 'Je třeba předat 2 věci. '
            if len(arguments) < 2:
                msg += 'Nebylo však zadáno nic.'
            else:
                msg += f'Byl však zadán pouze objekt: {arguments[1]}'
            return msg
        # Ověří že předmětu jsou v prostoru
        cp = current_place()
        if (  not (item1:=cp.item((x:=arguments[1]).lower()))
           or not (item2:=cp.item((x:=arguments[2]).lower()))
           ):
           return f'Nelze předat nepřítomný předmět: {x}'
        # Ověří, že předměty jsou přenositelné
        if (  (x:=item1).weight == world.Item.HEAVY
           or (x:=item2).weight == world.Item.HEAVY
           ):
           return f'Nelze předat nepřenosný předmět: {x.name}'
        # Ověří, že v prostoru je někdo, komu lze dárky předat
        for item in cp.items:
            if (low_name:=item.name.lower()) in _AWAKE:
                break
        else:
            return 'Není komu něco předat'
        # Ověří, že cíl předání je vzhůru
        if not _AWAKE[low_name]:
            return (f'Nemá smysl předávat, {low_name} ještě není '
                    f'{"probuzená" if low_name=="babička" else "probuzený"}.')
        # Ověří, že cíl předání již byl pozdraven
        if not _GREETED[low_name]:
            return (f'Karkulka ještě '
                    f'{"babičku" if low_name=="babička" else "vlka"} '
                    f'nepozdravila.')
        # Ověří, že cíli předání již bylo popřáno
        if not _WISHED[low_name]:
            return (f'Karkulka ještě '
                    f'{"babičce" if low_name=="babička" else "vlkovi"} '
                    f'nepopřála.')
        global _is_active
        _is_active = False
        return (f'Karkulka předala '
                f'{"babičce" if low_name=="babička" else "vlkovi"} '
                f'předměty: {item1.name} a {item2.name}\n'
                f'Úspěšně jste ukončili hru.\n'
                 'Děkujeme, že jste si zahráli.')



############################################################################

def _initialize():
    """Inicializuje všechny potřebné objekty hry.
    """
    world_initialize()
    global _AWAKE, _GREETED, _WISHED
    _AWAKE   = {'babička':False, 'vlk':False}
    _GREETED = {'babička':False, 'vlk':False}
    _WISHED  = {'babička':False, 'vlk':False}



def _start_game():
    """Spustí neběžící hru.
    """
    global _is_active
    _is_active = True
    _initialize()
    return (
        'Vítejte!\nToto je příběh o Červené Karkulce, babičce a vlkovi.\n'
        'Svými příkazy řídíte Karkulku, aby donesla bábovku a víno \n'
        'babičce v chaloupce za temným lesem. Když přijdete do chaloupky,\n'
        'tak položíte dárky, babičku vzbudíte, pozdravíte,\n'
        'popřejete ji k narozeninám a dárky předáte.\n'
        'Jste-li dobrodružné typy, můžete to místo s babičkou provést\n'
        's vlkem, který spí v temném lese.\n\n'
        'Nebudete-li si vědět rady, zadejte znak ?.'
    )



############################################################################

# Příznak toho, zda hra právě běží (True), anebo jen čeká na další spuštění
_is_active = False   # Na počátku čeká, až ji někdo spustí

# Převodník názvů akce na její objekt
_NAME_2_ACTION = {'jdi':Goto(),  'polož':Put_down(), 'vezmi':Take(),
                  'konec':End(), '?':Help(),
                  'probuď':Wake_up(), 'pozdrav':Greet(),
                  'popřej':Wish(), 'předej':Give()}

# Slovník, kde klíčem je název (malými písmeny) objektu
# a hodnotou je informace o tom, je-li daný objekt již vzhůru
# Názvy stačí, protože víme, že každý z objektů bude ve hře jen jeden
_AWAKE:dict[str:bool]

# Slovník, kde klíčem je název (malými písmeny) objektu,
# který lze pozdravit, a hodnotou je informace o tom, zda již byl pozdraven.
_GREETED:dict[str:bool]

# Slovník, kde klíčem je název (malými písmeny) objektu, jemuž lze popřát
# k narozeninám a hodnotou je informace o tom, zda mu již bylo popřáno.
_WISHED:dict[str:bool]


############################################################################
dbg.stop_mod (0, __name__)
