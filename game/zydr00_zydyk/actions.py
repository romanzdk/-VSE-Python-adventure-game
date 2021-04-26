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

class End(AAction):
    """Resi predcasne ukonceni hry"""

    def __init__(self):
        super().__init__('konec', 'Predcasne ukonci hru')
    
    def execute(self, arguments:tuple[str]) -> str:
        global _is_active
        _is_active = False
        return ('Ukončili jste hru.\n'
                'Děkujeme, že jste si zahráli.')

############################################################################

class Go_To(AAction):
    """Resi presun hrace do zadaneho prostoru"""

    def __init__(self):
        super().__init__('jdi', 'Presune hrace do zadaneho prostoru')
    
    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, kam mám jít.\n'
                    'Je třeba zadat jméno cílového prostoru.')
        place_name = arguments[1]
        place = world.place(place_name)
        if not place in current_place().neighbors:
            return f'Do zadaného prostoru se odsud jít nedá: {place_name}.'
        world._current_place = place
        return (f'Presunuli jste se do prostoru: {place.name}.\n'+
                place.description)

############################################################################

class Put_Down(AAction):
    """Resi presun predmetu z batohu do prostoru"""

    def __init__(self):
        super().__init__('poloz', 'Presune predmet z batohu do prostoru')
    
    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, co mám položit.\n'
                    'Je třeba zadat jméno pokládaného objektu.')
        item_name = arguments[1]
        item = BAG.remove_item(item_name)
        if not item:
            return f'Zadaný objekt v batohu není: {item_name}'
        current_place().add_item(item)
        return f'Vyhodili jste {item.name}.'

############################################################################

class Take(AAction):
    """Resi presun predmetu z prostoru do batohu"""

    def __init__(self):
        """Vytvoří h-objekt se zadaným názvem.
        """
        super().__init__('vezmi', 'Presune predmet z prostoru do batohu')
    
    def execute(self, arguments:tuple[str]) -> str:
        if len(arguments) < 2:
            return ('Nevím, co mám zvednout.\n'
                   'Je třeba zadat jméno zvedaného objektu.')
        item_name = arguments[1]
        item = current_place().remove_item(item_name)
        if not item:
            return f'Zadaný objekt v prostoru není: {item_name}'
        BAG.add_item(item)
        return f'Sebrali jste {item.name}.'


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
    command = command.strip().lower()
    if _is_active:
        # Hra běží, reagujeme na zadaný příkaz
        if command == '':
            return 'Prázdný příkaz lze použít pouze pro start hry'
        else:
            words = command.split()
            action = _NAME_2_ACTION.get(words[0])
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

############################################################################

def _initialize():
    """Inicializuje vsechny potrebne objekty hry
    """
    world.initialize()

def _start_game():
    """Spusti nebezici hru
    """
    global _is_active
    _is_active = True
    _initialize()

    return ('Vítejte!\nPrávě jste se probudil na zasněženém poli...\n'
          'Nemůžete si vzpomenout, co se stalo...\n'
          'Je zima a padá sníh...\n'
          '...\n'
          'Dostaňte se z tohoto místa a zachraňte se.\n'
          'Nebudete-li si vědět rady, zadejte znak ?.')

############################################################################

_is_active = False

# Prevodnik nazvu akce na jeji objekt
_NAME_2_ACTION = {
    'jdi':Go_To(),
    'konec':End(),
    'poloz':Put_Down(),
    'vezmi':Take()
}

############################################################################
dbg.stop_mod (0, __name__)
