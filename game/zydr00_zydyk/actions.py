#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul action má na starosti zpracování příkazů.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from abc import ABC, abstractmethod

from . import world
from .world import current_place, BAG

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
        """Vytvoří h-objekt se zadaným názvem.
        """
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

class Cry(AAction):
    """Začne brečet smutky a strachy."""

    def __init__(self):
        super().__init__('brec', 'Začne brečet smutky a strachy.')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""
        if not has_cried():
            global _has_cried
            _has_cried = True
            return ('Brečíte zoufalstvím...\nPořád brečíte...\n'
            'Už vás to nebaví...\nVzchopíte se a jdete něco dělat.')
        else:
            return  ('Už jste jednou brečeli, pokud byste brečeli znovu,\n'
                     'tak by vám došly všechny síly a jistě byste umrzli.') 

############################################################################

class End(AAction):
    """Řeší předčasné ukončení hry"""

    def __init__(self):
        super().__init__('konec', 'Předčasně ukončí hru.')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""
        global _is_active
        _is_active = False
        return ('Ukončili jste hru.\n'
                'Děkujeme, že jste si zahráli.')

############################################################################

class Explore(AAction):
    """Prozkoumá zvolený objekt"""

    def __init__(self):
        super().__init__('prozkoumej', 'Prozkoumá zvoleny objekt.')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""
        if len(arguments) < 2:
            return ('Nevím co mám prozkoumat, zadejte argument.')
        item_name = arguments[1]
        item=world.item(item_name) #vytvoř z názvu objekt
        if item in current_place().items: #najdi objekt v prostoru
            if item.is_explored:
                return (
                    f'Předmět {item.name} jste již jednou prozkoumali, '
                    'nelze stejný\npředmět prozkoumávat znovu.')
            else:
                # přidej předměty do prostoru
                items_in_place = current_place().items
                current_place()._items = (list(items_in_place)
                                        +(item.items_to_unhide))
                
                #přidej názvy objektu do prostoru
                item_names_in_place = current_place().item_names
                current_place()._item_names = (list(item_names_in_place) + 
                                              list(item._item_names_to_unhide))
                item.is_explored = True
                return (f'Prozkoumali jste: {item_name}.\n'+
                        item.description)
        else:
            return f'Zadaný objekt v prostoru není: {item_name}.'

############################################################################

class Go_To(AAction):
    """Řeší přesun hráče do zadaného prostoru"""

    def __init__(self):
        super().__init__('jdi', 'Přesune hráče do zadaného prostoru')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""

        if len(arguments) < 2:
            return ('Nevím, kam mám jít.\n'
                    'Je třeba zadat jméno cílového prostoru.')
        place_name = arguments[1]
        place = world.place(place_name)
        if not place in current_place().neighbors:
            return f'Do zadaného prostoru se odsud jít nedá: {place_name}.'
        if current_place().will_kill:
            global _is_active
            _is_active = False
            return 'Konec hry.'
        world._current_place = place
        return (f'Přesunuli jste se do prostoru: {place.name}.\n'+
                place.description)

############################################################################

class Help(AAction):
    """Nápověda pro hráče"""

    def __init__(self):
        super().__init__('?', 'Zobrazí nápovědu')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""
        return (
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
            '?'
        )

############################################################################

class Put_Down(AAction):
    """Řeší přesun předmětu z batohu do prostoru"""

    def __init__(self):
        super().__init__('poloz', 'Přesune předmět z batohu do prostoru')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""

        if len(arguments) < 2:
            return ('Nevím, co mám položit.\n'
                    'Je třeba zadat jméno pokládaného objektu.')
        item_name = arguments[1]
        item = BAG.remove_item(item_name)
        if not item:
            return f'Zadaný objekt v batohu není: {item_name}.'
        current_place().add_item(item)
        return f'Vyhodili jste: {item.name}.'

############################################################################

class Shout(AAction):
    """Zakřičí o pomoc"""

    def __init__(self):
        super().__init__('zakric', 'Zakřičí o pomoc')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""

        if not has_shouted():
            global _has_shouted
            _has_shouted = True
            return ('Křičíte o pomoc...\Pořád křičíte...\nUž nemůžete...\n'
                    'Nikdo se neozývá...\nKřik vzdáváte.')
        else:
            return  ('Už jste jednou křičeli, pokud byste křičeli znovu,\n'
                     'tak by vám došly všechny síly a jistě byste umrzli.')

############################################################################

class Take(AAction):
    """Řeší přesun předmětu z prostoru do batohu"""

    def __init__(self):
        super().__init__('vezmi', 'Přesune předmět z prostoru do batohu')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""

        if len(arguments) < 2:
            return ('Nevím, co mám vzít.\n'
                   'Je třeba zadat jméno zvedaného objektu.')
        item_name = arguments[1]
        item=world.item(item_name) #vytvoř z názvu objekt
        if item in current_place().items: #pokud je předmět v prostoru
            if (BAG.free >= 1) and (item.is_pickable):
                current_place().remove_item(item_name)
                BAG.add_item(item)
                return (f'Sebrali jste: {item.name}.\n' +
                        item.description)
            else:
                if BAG.free < 1:
                    return 'Zadaný objekt se už do batohu nevejde!'
                else:
                    return f'Zadaný objekt není možno zvednout: {item_name}'
        else:
            return f'Zadaný objekt v prostoru není: {item_name}'
        
############################################################################

class Use(AAction):
    """Použije zadaný předmět na jiný předmět"""

    def __init__(self):
        super().__init__('pouzij', 'Použije předmět 1 na předmět 2')
    
    def execute(self, arguments:tuple[str]) -> str:
        """Provede zadaný příkaz"""

        if len(arguments) < 3:
            return ('Nevím na co mám zadaný předmět použít. '
                    'Zadejte druhý předmět.')
        item1 = arguments[1]
        item2 = arguments[2]
        item1 = world.item(item1)
        item2 = world.item(item2)
        def is_present(item, place, bag):
            if item is None:
                return False
            if (item in place.items) or (item in bag.items):
                return True
            return False

        # předmět 1 není k dispozici
        if not is_present(item1, current_place(), BAG):
            return (f'Nelze použít předmět: {arguments[1]}, '
                    'který tu není.')
        
        #předmět 2 není k dispozici
        if not is_present(item2, current_place(), BAG):
            return (f'Nelze použít předmět: {item1.name} na předmět: ' +
                    f'{arguments[2]}, který ve hře není.')

        # předmět je nepřenositelný
        if not item1.is_pickable:
            return (f'Nelze použít nepřenosný předmět: {item1.name}.')
        
        #předmět nelze použít na druhý předmět
        if not(item2.name in item1.can_be_used_on):
            return (f'Nelze použít předmět: {item1.name} '
                    f'na předmět: {item2.name}.')
        
        #použití předmětu neukončí hru
        if not item1.ends_game_when_used:
            return item2.text_when_used
        
        #použití předmětu ukončí hru
        global _is_active
        _is_active = False
        return item2.text_when_used
            
############################################################################
def is_active() -> bool:
    """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return _is_active

def has_cried() -> bool:
    """Vrátí informaci o tom, zdali hráč v aktuální hře již brečel."""
    return _has_cried

def has_shouted() -> bool:
    """Vrátí informaci o tom, zdali hráč v aktuální hře již křičel."""
    return _has_shouted

def execute_command(command:str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele."""
    command = command.strip().lower()
    if _is_active:
        # Hra běží, reagujeme na zadaný příkaz
        if command == '':
            return 'Prázdný příkaz lze použít pouze pro start hry.'
        else:
            words = command.split()
            action = _NAME_2_ACTION.get(words[0])
            if not action:
                return f'Tento příkaz neznám: {words[0]}.'
            answer = action.execute(words)
            return answer

    else:   # Hra neběží, musí se odstartovat
        if command == '':
            return _start_game()
        else:
            return ('Prvním příkazem není startovací příkaz.\n' 
                    'Hru, která neběží, lze spustit '
                    'pouze startovacím příkazem.')

def stop():
    """Ukončí aktuální běh hry.
    """
    global _is_active
    _is_active = False

############################################################################

def _initialize():
    """Inicializuje všechny potřebné objekty hry"""
    
    world.initialize()

def _start_game():
    """Spustí neběžící hru"""

    global _is_active, _has_cried, _has_shouted
    _is_active, _has_cried, _has_shouted = True, False, False
    _initialize()

    return ('Vítejte!\nPrávě jste se probudil na zasněženém poli...\n'
          'Nemůžete si vzpomenout, co se stalo...\n'
          'Je zima a padá sníh...\n'
          '...\n'
          'Dostaňte se z tohoto místa a zachraňte se.\n'
          'Nebudete-li si vědět rady, zadejte znak ?.')

############################################################################

_is_active = False
_has_cried = False
_has_shouted = False

# Převodník názvu akce na její objekt
_NAME_2_ACTION = {
    'brec':Cry(),
    'jdi':Go_To(),
    'konec':End(),
    'poloz':Put_Down(),
    'prozkoumej':Explore(),
    'pouzij':Use(),
    'vezmi':Take(),
    'zakric':Shout(),
    '?':Help()
}

############################################################################
dbg.stop_mod (0, __name__)
