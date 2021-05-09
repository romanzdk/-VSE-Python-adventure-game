#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Třídy pro konstrukci scénářů.

Definované proměnné:
    next_index      - Index následujícího kroku
    HAPPY_NAME      - Název šťastného scénáře
    MISTAKE_NAME    - Název chybového scénáře
    MISTAKE_NS_NAME - Název chybového scénáře rozšiřujících akcí

"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from collections import namedtuple

from .scen_types import TypeOfScenario, TypeOfStep, tsNOT_START
from .game_types import AGame



############################################################################

# Definuje pomocnou třídu pojmenovanou ScenarioStep
_Step = namedtuple('ScenarioStep', 'index, typeOfStep command message '
                                   'place neighbors items bag')

def ScenarioStep(typeOfStep:TypeOfStep, command:str, message:str, place:str,
                 neighbors:tuple[str], items:tuple[str], bag:tuple[str]):
    """Funkce vystupuje vůči okolnímu programu jako konstruktor,
    který vytváří instance třídy ScenarioStep, přičemž očekává argumenty:
    typeOfStep:TypeOfStep   - Typ kroku scénáře
    command:str             - Zadávaný příkaz
    message:str             - Odpověď hry
    place:str               - Název aktuálního prostoru
    neighbors:tuple[str]    - Aktuální sousedé aktuálního prostoru
    items:tuple[str]        - Aktuální předměty v aktuálním prostoru
    bag:tuple[str]          - Aktuální předměty v batohu
    """
    result = ScenarioStep.new(ScenarioStep.next_index, typeOfStep,
             command, message, place, neighbors, items, bag)
    # Původní konstruktor pojmenovaných n-tic nevyhovuje, protože
    # po každém kroku je třeba inkrementovat index následujícího kroku
    ScenarioStep.next_index += 1
    return result

# Odkaz na konstruktor třídy ukládáme do atributu funkce
ScenarioStep.new = _Step
del _Step

# Atribut next_index zadává vypisovaný index následujícího kroku, jenž
# je vhodné inicializovat vždy při zadávání počátečního kroku scénáře
ScenarioStep.next_index = 0

def __repr__(self):     # Název v rámci modulu nekoliduje
    return (f'{self.index}. krok: {self.command}\n{30*"-"}\n'
            f'{self.message}\n{60*"-"}\n'
            f'Aktuální prostor:    {self.place}\n'
            f'Sousedé prostoru:    {self.neighbors}\n'
            f'Předměty v prostoru: {self.items}\n'
            f'Předměty v batohu:   {self.bag}\n{60*"="}\n')

# Funkci přiřadíme jako atribut třídě pojmenované n-tice
ScenarioStep.new.__repr__ = __repr__
del __repr__   # Smažu dočasnou proměnnou



############################################################################

class Scenario:
    """Třída scénářů definujících požadované chování hry.
    """
    count = 0
    print_state = False     # Zda při testu průběžně zobrazovat stav

    def __init__(self, name:str, scenario_type:TypeOfScenario,
                 steps:tuple['ScenarioStep']):
        # Ověří, že patří-li vytvářený scénář mezi první tři
        # je zadáván jako scénář požadovaného typu
        self._ordinal = Scenario.count;   Scenario.count+=1
        if (self._ordinal < 3) and (self._ordinal != scenario_type.ordinal):
            raise Exception("Nesedí typy prvních tří scénářů")
        else:
            self._type = scenario_type
        self._name = (name if self._ordinal > 2
                      else SCENARIO_NAMES[self._ordinal])
        self._steps = steps


    @property
    def name(self) -> str:
        """Vrátí název daného scénáře.
        """
        return self._name


    @property
    def ordinal(self) -> int:
        """Vrátí index scénáře v seznamu existujících scénářů.
        """
        return self._ordinal


    @property
    def steps(self) -> tuple['ScenarioStep']:
        """Vrátí n-tici kroků daného scénáře.
        """
        return self._steps


    @property
    def type(self) -> TypeOfScenario:
        """Vrátí typ daného scénáře.
        """
        return self._type


    def simulate(self, with_state:bool=False) -> None:
        """Vytiskne jednoduchou simulaci běhu hry podle šťastného scénáře,
        přičemž hodnota argumentu with_state určuje,
        zda se v každém kroku zobrazí pouze příkaz a odpověď hry (False),
        anebo se navíc vytisknou informace o požadovaném stavu hry
        po provedeném kroku (True).
        """
        print(f'\nSimulace scénáře: {self._name}\n{60*"#"}')
        for step in self.steps:
            if with_state:
                print(step)
            else:
                print(f'{step.index}. {step.command}\n{30*"-"}\n'
                      f'{step.message}\n{60*"="}\n')
        input(f'{60*"#"}\n=== Konec simulace scénáře {self._name} ===\n\n'
              f'Stiskněte Enter')


    def test(self, game:AGame, conv=None):
        """Otestuje zadanou hru podle daného scénáře.
        Je-li argument »conv« roven +1, převádí se zadané příkazy
        na velká písmena, je-li roven -1, převádí se na malá písmena
        a má-li jinou hodnotu nebo není zadá, ponechávají se příkazy
        ve tvaru, jak byly zadány ve scénáři.
        """
        from_scenario:list[str]
        from_game:list[str]

        def _error(reason:str, step:ScenarioStep, expected, obtained):
            """Zobrazí chybové hlášení upozorňující na příčinu chyby.
            """
            message = (f'Při vyhodnocování {step.index}. kroku scénáře '
                         f'{self.name} byla odhalena chyba:\n'
                       f'Chybným objekt:   {reason}\n'
                       f'Očekávaný objekt: {str(expected)}\n'
                       f'Obdržený objekt:  {str(obtained)}\n\n')
            print(message)
            print(f'Očekávaný stav hry po provedení testovaného příkazu:\n'
                  f'{step}')
            print(f'\nObdržený stav hry po provedení testovaného příkazu:')
            print(f'{AGame.current_state(game)}')
            raise Exception

        def compare_containers(scen_cont, game_cont):
            """Porovná obsah zadaných kontejnerů bez ohledu na velikost písmen.
            """
            # dbg.prSE(2, 1, 'test_by', f'{scen_cont=}, {game_cont=}')
            if not ('__iter__' in dir(game_cont)):
                _error('objekt hry není kontejner', step, scen_cont, game_cont)
            nonlocal from_scenario, from_game
            from_scenario = [item     .lower() for item in scen_cont].sort()
            from_game     = [item.name.lower() for item in game_cont].sort()
            # dbg.prSE(2, 0, 'test_by')
            return from_scenario != from_game

        print(f'\n{60*"%"}\nTest podle scénáře: {self.name} - {conv=}\n')
        step:ScenarioStep
        for step in self.steps:
            command = step.command
            if   conv == +1:  command = command.upper()
            elif conv == -1:  command = command.lower()
            print(f'{step.index}. {command}\n{30*"-"}')
            try:
                answer = game.execute_command(command)
                print(f'{answer}')
                if Scenario.print_state:
                    print(f'{30*"-"}\n{AGame.current_state(game)}')
                print(f'{30*"="}\n')
            except Exception as ex:
                print(f'Při vykonávání příkazu '
                      f'{step.index}. {(command:=step.command)}\n'
                      f'byla vyhozena výjimka {ex}')
                raise ex

            # print(f'Očekávaný stav hry po provedení testovaného příkazu:\n'
            #       f'{step}')
            # print(f'\nObdržený stav hry po provedení testovaného příkazu:')
            # print(f'{AGame.current_state(game)}')

            if (not answer or
                step.message.lower() != answer[:len(step.message)].lower()
            ):
                _error('odpověď hry', step, step.message, answer)
            if step.typeOfStep == tsNOT_START:
                continue
            current_place = game.world().current_place()
            if step.place != current_place.name:
                _error('aktuální prostor', step, step.place, current_place)
            if compare_containers(step.neighbors, current_place.neighbors):
                _error('aktuální sousedé', step, from_scenario, from_game)
            if compare_containers(step.items, current_place.items):
                _error('objekty v aktuálním prostoru', step, from_scenario,
                                                             from_game)
            if compare_containers(step.bag, game.bag().items):
                _error('objekty v batohu', step, from_scenario, from_game)
        if game.isAlive():
            _error('Po ukončení scénáře není hra ukončena', step, (), ())



############################################################################

HAPPY_NAME       = "HAPPY"
MISTAKE_NAME     = "MISTAKES"
MISTAKE_NS_NAME  = "MISTAKES_NS"
SCENARIO_NAMES   = (HAPPY_NAME, MISTAKE_NAME, MISTAKE_NS_NAME)



############################################################################
dbg.stop_mod (0, __name__)
