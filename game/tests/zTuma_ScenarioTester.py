#############################################################################
# Author: Andrii Tuma
# Date: 27.03.2021
# Если Вы читаете это, храни Вас Господь
#############################################################################
# game.tests.zTuma_ScenarioTester
# from hw07_3scenarios.pecr807_pecinovsky.scenarios import *
# from ..pecr807_pecinovsky.factory import *
from ..api.scenario    import *
from ..api.scen_types   import *

lepota = "###################################################################"

def init_for_factory(fact):    #!RP#
    """Inicializace proměnných pro test zadané továrny.
    """
    global factory, scenario, happyActions, notUsedActions
    global knownPlaces, visitedPlaces, nonStandardActions, hObjects
    global usedComands, usedTypes, allTypes, erors, status, happyNS
    global comandsByType, nonStandardTypes
    global minSteps, minPlaces, minVisited, minOwnActions, ok, nonOk

    factory  = fact   #!RP#
    scenario = factory.scenarios()[0]
    happyActions   = [tsSTART, tsGOTO, tsTAKE, tsPUT_DOWN]
    notUsedActions = [tsSTART, tsGOTO, tsTAKE, tsPUT_DOWN]
    knownPlaces = []
    visitedPlaces = []
    nonStandardActions = []
    hObjects = []
    usedComands = []
    usedTypes = []
    allTypes = []
    for typ in ALL_TYPES:
        allTypes.append(typ.__name__)
    erors = []
    status = 1
    comandsByType = {}
    nonStandardTypes = {}
    ########################################################
    # minimáalní požadované atributy scénáře pro splnění testu
    minSteps = 12
    minPlaces = 6
    minVisited = 4
    minOwnActions = 4
    ########################################################
    ok = "suit"
    nonOk = "DOES NOT SUIT"
    ########################################################


class Pair:
    def __init__(self, firstStep, secondStep, index):
        self.firstStep = firstStep
        self.secondStep = secondStep
        self.index = index

    def getStep(self, interestedStep):
        if(interestedStep == 1):
            return self.firstStep
        if(interestedStep == 2):
            return self.secondStep
########################################################


def controlSameBag(pair):
    firstBag = pair.firstStep.bag
    secondBag = pair.secondStep.bag
    error = "Krok čislo " + str(pair.index) + " má chybu se zminěním batohu. Jelikož po tom kroku batoh neměl se měnit.\n : Mělo by byt" + \
        str(firstBag) + " Je: " + \
        str(secondBag) + " eshkere"
    if firstBag != secondBag:
        erors.append(error)
########################################################


def controlSamePlace(pair, num):
    firstPlace = pair.firstStep.place
    secondPlace = pair.secondStep.place
    error = "Krok čislo " + str((pair.index + num)) + " má chybu se zminěním polohy. Jelikož po tom kroku poloha neměla se měnit.\n Mělo by byt: " + \
        str(firstPlace) + " Je: " + str(secondPlace)
    if secondPlace != firstPlace:
        erors.append(error)
########################################################


def controlNeigbors(pair, num):
    firstNeigbors = pair.firstStep.neighbors
    secondNeigbors = pair.secondStep.neighbors
    error = "Krok čislo " + str(pair.index + num) + " má chybu se zminěním sousedu. Jelikož po tom kroku sousedi neměli by se měnit.\n Mělo by byt: " + \
        str(firstNeigbors) + " Je: " + \
        str(secondNeigbors)
    if firstNeigbors != secondNeigbors:
        erors.append(error)
########################################################


def controlNonArgs(pair):
    comand = pair.secondStep.command.split()
    if(len(comand) == 0):
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " obsahuje chybu. Prazdný přikaz muže byt jenom u tsSTART"
        erors.append(error)
        return
########################################################


def verifyNumberOfArguments2(pair, required):
    comand = pair.secondStep.command.split()

    if len(comand) != required:
        error = "Krok čislo " + \
            str(pair.index + 1) + " obsahuje chybu. Komanda musí mít v sobě " + \
            str(required) + " slova."
        erors.append(error)
        return
########################################################


def verifyNumberOfArguments1(pair, required):
    comand = pair.firstStep.command.split()
    if len(comand) != required:
        error = "Krok čislo " + \
            str(pair.index) + " obsahuje chybu. Komanda musí mít v sobě " + \
            str(required) + " slova. "
        erors.append(error)
        return
########################################################


def controlTakeItem(pair):
    comand = pair.secondStep.command.split()

    if len(comand) < 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se převzetim itemu. Není ukazano co je třeba vzit"
        erors.append(error)
        return
    if len(comand) > 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se převzetim itemu. Nerozumim přikaz. Musí tam byt 2 slova"
        erors.append(error)
        return
    item = comand[1]
    item = str(item).lower()

    firstItems = pair.firstStep.items
    firstItemsCorrected = []
    for it in firstItems:
        firstItemsCorrected.append(it.lower())
    firstItems = firstItemsCorrected

    secondItems = pair.secondStep.items
    secondItemsCorrected = []
    for it in secondItems:
        secondItemsCorrected.append(it.lower())
    secondItems = secondItemsCorrected

    firstBag = pair.firstStep.bag
    firstBagCorrected = []
    for it in firstBag:
        firstBagCorrected.append(it.lower())
    firstBag = firstBagCorrected

    secondBag = pair.secondStep.bag
    secondBagCorrected = []
    for it in secondBag:
        secondBagCorrected.append(it.lower())
    secondBag = secondBagCorrected

    if item not in firstItems:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se převzetim itemu. Zadaneho itemu není v poloze. Item: " + \
            item + ". Poloha: " + str(firstItems)
        erors.append(error)
        return
    if item in secondItems:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se převzetim itemu. Zadaný item v nasledujicim kroku stale je v lokaci"
        erors.append(error)
        return
    if item not in secondBag:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se převzetim itemu. Zadaný item nepřidá se k batohu. Item: " + \
            item + ". Batoh: " + str(secondBag)
        erors.append(error)
        return
    if len(secondBag) == 3:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se převzetim itemu. Batoh už je plný"
        erors.append(error)
        return
    thirdItems = firstItems
    thirdItems.remove(item)
    thirdItems.sort()
    secondItems.sort()
    if thirdItems != secondItems:
        error = "Krok čislo " + str(pair.index + 1) + " má chybu s Itemami v prostoru. Je: " + str(
            secondItems) + " Mělo by byt: " + str(thirdItems)
        erors.append(error)
        return
    thirdBag = firstBag
    thirdBag.append(item)
    thirdBag.sort()
    secondBag.sort()
    if thirdBag != secondBag:
        error = "Krok čislo " + str(pair.index + 1) + " má chybu s Itemami v batohu. Je: " + str(
            secondBag) + " Mělo by byt: " + str(thirdBag)
        erors.append(error)
        return
########################################################


def controlMove(pair):
    comand = pair.secondStep.command.split()
    if len(comand) < 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se pohybem. Není ukazano kam je třeba jit"
        erors.append(error)
        return
    if len(comand) > 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se pohybem. Nerozumim přikaz. Musí tam byt 2 slova"
        erors.append(error)
        return

    firstNeigbors = pair.firstStep.neighbors
    firstNeigborsCorrect = []
    for ng in firstNeigbors:
        firstNeigborsCorrect.append(ng.lower())
    firstNeigbors = firstNeigborsCorrect

    secondNeigbors = pair.secondStep.neighbors
    secondNeigborsCorrect = []
    for ng in secondNeigbors:
        secondNeigborsCorrect.append(ng.lower())
    secondNeigbors = secondNeigborsCorrect

    firstPlace = pair.firstStep.place.lower()
    secondPlace = pair.secondStep.place.lower()
    goal = comand[1].lower()

    if goal not in firstNeigbors:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se pohybem. Není taková sousední lokace: " + \
            goal + ". Sousedi: " + str(firstNeigbors)
        erors.append(error)
        return
    if firstPlace not in secondNeigbors:
        error = "Krok čislo " + str(pair.index + 1) + " má chybu se pohybem. Misto odkud vyšel hrdina není v současnych sousedich: " + \
            firstPlace + ". Sousedi: " + \
            str(secondNeigbors)
        erors.append(error)
        return
    if secondPlace != goal:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se pohybem. Aktualní misto není cilovym mistem: " + \
            goal + ". Aktualní prostor: " + secondPlace
        erors.append(error)
        return
########################################################


def controlPutting(pair):
    comand = pair.secondStep.command.split()

    if len(comand) < 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se položením itemu. Není ukazano co je třeba položit"
        erors.append(error)
        return
    if len(comand) > 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu se položením itemu. Nerozumim přikaz. Musí tam byt 2 slova"
        erors.append(error)
        return
    item = comand[1]
    item = str(item).lower()

    firstItems = pair.firstStep.items
    firstItemsCorrected = []
    for it in firstItems:
        firstItemsCorrected.append(it.lower())
    firstItems = firstItemsCorrected

    secondItems = pair.secondStep.items
    secondItemsCorrected = []
    for it in secondItems:
        secondItemsCorrected.append(it.lower())
    secondItems = secondItemsCorrected

    secondBag = pair.secondStep.bag
    secondBagCorrected = []
    for it in secondBag:
        secondBagCorrected.append(it.lower())
    secondBag = secondBagCorrected

    firstBag = pair.firstStep.bag
    firstBagCorrected = []
    for it in firstBag:
        firstBagCorrected.append(it.lower())
    firstBag = firstBagCorrected

    if item not in firstBag:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se položením itemu. Takoveho itemu v batohu není: " + \
            item + ". Batoh: " + str(firstBag)
        erors.append(error)
        return
    if item in secondBag:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se položením itemu. Item se zustal v batohu: " + \
            item + ". Batoh: " + str(secondBag)
        erors.append(error)
        return
    if item not in secondItems:
        error = "Krok čislo " + \
            str(pair.index + 1) + " má chybu se položením itemu. Item po vyložení není v mistnosti: " + \
            item + ". Mistnost: " + str(secondItems)
        erors.append(error)
        return
    thirdItems = firstItems
    thirdItems.append(item)
    thirdItems.sort()
    secondItems.sort()
    if thirdItems != secondItems:
        error = "Krok čislo " + str(pair.index + 1) + " má chybu s Itemami v prostoru. Je: " + str(
            secondItems) + " Mělo by byt: " + str(thirdItems)
        erors.append(error)
        return
    thirdBag = firstBag
    thirdBag.remove(item)
    thirdBag.sort()
    secondBag.sort()
    if thirdBag != secondBag:
        error = "Krok čislo " + str(pair.index + 1) + " má chybu s Itemami v batohu. Je: " + str(
            secondBag) + " Mělo by byt: " + str(thirdBag)
        erors.append(error)
        return
########################################################


def controlNeigbor(pair, num):
    comand = pair.secondStep.command.split()

    if len(comand) < 2:
        error = "Krok čislo " + \
            str(pair.index + num) + \
            " má chybu se pohybem. Není ukazano kam je třeba jit"
        erors.append(error)
        return
    if len(comand) > 2:
        error = "Krok čislo " + \
            str(pair.index + num) + \
            " má chybu se pohybem. Nerozumim přikaz. Musí tam byt 2 slova"
        erors.append(error)
        return
    firstNeigbors = pair.firstStep.neighbors
    firstNeigborsCorrect = []
    for ng in firstNeigbors:
        firstNeigborsCorrect.append(ng.lower())
    firstNeigbors = firstNeigborsCorrect

    if comand[1].lower() in firstNeigbors:
        error = "Krok čislo " + \
            str(pair.index + num) + \
            " má chybu se pohybem. Takový soused pravě je."
        erors.append(error)
        return
########################################################


def controlItem(pair, num):
    comand = pair.secondStep.command.split()
    if len(comand) < 2:
        error = "Krok čislo " + \
            str(pair.index + num) + \
            " má chybu s převzetim itemu. Není ukazano co je třeba vzit"
        erors.append(error)
        return
    if len(comand) > 2:
        error = "Krok čislo " + \
            str(pair.index + num) + \
            " má chybu s převzetim itemu. Nerozumim přikaz. Musí tam byt 2 slova"
        erors.append(error)
        return
    item = comand[1]
    item = str(item).lower()

    firstItems = pair.firstStep.items
    firstItemsCorrected = []
    for it in firstItems:
        firstItemsCorrected.append(it.lower())
    firstItems = firstItemsCorrected
    if item in firstItems:
        error = "Krok čislo " + \
            str(pair.index + num) + \
            " má chybu s převzetim itemu. Takový item pravě je."
        erors.append(error)
        return
########################################################


def controlComandType(pair, num):
    step = pair.firstStep if num == 0 else pair.secondStep
    comand = step.command.split()

    if len(comand) == 0:
        comandsByType.update({step.typeOfStep.name: comand})
        return

    if str(step.typeOfStep.group) in comandsByType:
        if(comand[0].lower() != str(comandsByType.get(str(step.typeOfStep.group))).lower()):
            error = "Step čislo " + \
                str(pair.index + num) + \
                " má chybu s zadaním komandy. Komanda s takovou grupou už má jiný nazev"
            erors.append(error)
            return
        return

    if step.typeOfStep.name not in comandsByType and str(step.typeOfStep.group) not in comandsByType:
        comandsByType.update({step.typeOfStep.name: comand[0].lower()})

    if str(comandsByType.get(step.typeOfStep.name)).lower() != comand[0].lower():
        error = "Step čislo " + \
            str(pair.index + num) + \
            " má chybu s zadaním komandy. Komanda s takovym typem už má jiný nazev"
        erors.append(error)
        return
    titles = []
    for key in comandsByType.keys():
        titles.append(comandsByType.get(key))
    if titles.count(comand[0].lower()) > 1:
        error = "Step čislo " + \
            str(pair.index + num) + \
            " má chybu s zadaním komandy. Komanda s takovym jmenem už existuje"
        erors.append(error)
        return
    if comand[0].lower() in nonStandardTypes:
        error = "Step čislo " + \
            str(pair.index + num) + \
            " má chybu s zadaním komandy. Komanda s takovym jmenem už existuje"
        erors.append(error)
        return
########################################################


def controlNotInBag(pair):
    comand = pair.secondStep.command.split()
    if len(comand) < 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu s položením itemu. Není ukazano co je třeba položit"
        erors.append(error)
        return
    if len(comand) > 2:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu s položením itemu. Nerozumim přikaz. Musí tam byt 2 slova"
        erors.append(error)
        return
    item = comand[1]
    item = str(item).lower()

    firstBag = pair.firstStep.bag
    firstBagCorrected = []
    for it in firstBag:
        firstBagCorrected.append(it.lower())
    firstBag = firstBagCorrected

    if item in firstBag:
        error = "Krok čislo " + \
            str(pair.index + 1) + \
            " má chybu s položením itemu. Takový item pravě je v batohu."
        erors.append(error)
        return

########################################################


def controlNonSType(pair):
    comand = pair.firstStep.command.split()
    if len(comand) == 0:
        error = "Step čislo " + \
            str(pair.index) + \
            " má chybu s zadaním komandy. Prazdny zapis je možný jenom při tsStart"
        erors.append(error)
        return
    titles = []
    for key in comandsByType.keys():
        titles.append(comandsByType.get(key))
    if comand[0].lower() in titles:
        error = "Step čislo " + \
            str(pair.index) + \
            " má chybu s zadaním komandy. Komanda s takovym jmenem už existuje"
        erors.append(error)
        return
    typ = pair.firstStep.typeOfStep.name
    if(typ != "tsNS_0" and typ != "tsNS_1" and typ != "tsNS_2" and typ != "tsNS_3"):
        if(comand[0].lower() in nonStandardTypes):
            rememberedType = nonStandardTypes.get(comand[0].lower())
            if(rememberedType != str(pair.firstStep.typeOfStep.group)):
                error = "Step čislo " + \
                    str(pair.index) + \
                    " má chybu s zadaním komandy. Pro takovou komandu je definovana jina hrupa"
                erors.append(error)
                return
            else:
                return
        else:
            error = "Step čislo " + \
                str(pair.index) + \
                " má chybu s zadaním komandy. Takoveho nestandartního přikazu není"
            erors.append(error)
            return

    nonStandardTypes.update(
        {comand[0].lower(): str(pair.firstStep.typeOfStep.group)})
########################################################


def controlNotStart(pair):
    comand = pair.firstStep.command.split()
    if len(comand) == 0:
        error = "Step čislo " + \
            str(pair.index) + " má chybu s zadaním komandy. Příkaz v testu špatného odstartování hry nesmí být prázdný"
        erors.append(error)
        return
    if pair.index > 0:
        error = "Step čislo " + \
            str(pair.index) + " má chybu s zadaním komandy. Příkaz typu tsNOT_START musí byt prvnim v Mistakes Scenario. Hra už pravě běží"
        erors.append(error)

########################################################
def controlTsStart(pair):
    comand = pair.firstStep.command.split()
    controlComandType(pair, 0)
    if len(comand) != 0:
        error = "Step čislo " + \
            str(pair.index) + \
            " má chybu se startovacím přikazem. Startovací přikaz musí byt prazdný ''"
        erors.append(error)
########################################################
def controlTsGoTo(pair):
    controlMove(pair)
    controlNonArgs(pair)
    controlComandType(pair, 1)
    controlSameBag(pair)
########################################################
def controlTsEND(pair):
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    controlComandType(pair, 1)
########################################################
def controlTsTake(pair):
    controlNonArgs(pair)
    controlSamePlace(pair, 1)
    controlComandType(pair, 1)
    controlTakeItem(pair)
########################################################
def controlTsPutDown(pair):
    controlNonArgs(pair)
    controlSamePlace(pair, 1)
    controlComandType(pair, 1)
    controlPutting(pair)
########################################################
def controlTsNS_0(pair):
    controlNonArgs(pair)
    controlNonSType(pair)
    verifyNumberOfArguments1(pair, 1)
    controlNonSType(pair)
########################################################
def controlTsNS_1(pair):
    controlNonArgs(pair)
    controlNonSType(pair)
    verifyNumberOfArguments1(pair, 2)
    controlNonSType(pair)
########################################################
def controlTsNS_2(pair):
    controlNonArgs(pair)
    controlNonSType(pair)
    verifyNumberOfArguments1(pair, 3)
    controlNonSType(pair)
########################################################
def controlTsNS_3(pair):
    controlNonArgs(pair)
    controlNonSType(pair)
    verifyNumberOfArguments1(pair, 4)
    controlNonSType(pair)
########################################################
def controlTsNOT_START(pair):
    controlNotStart(pair)
########################################################
def controlTsEMPTY(pair):
    controlNeigbors(pair, 0)
    controlSamePlace(pair, 0)
    controlSameBag(pair)
    controlComandType(pair, 0)
########################################################
def controltsUNKNOWN(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 0)
    controlSamePlace(pair, 0)
    controlSameBag(pair)
    controlComandType(pair, 0)
########################################################
def controlTsMOVE_WA(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 0)
    controlSamePlace(pair, 0)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 1)
    controlComandType(pair, 0)
########################################################
def controlTsTAKE_WA(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 0)
    controlSamePlace(pair, 0)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 1)
    controlComandType(pair, 0)
########################################################
def controlTsPUT_DOWN_WA(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 0)
    controlSamePlace(pair, 0)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 1)
    controlComandType(pair, 0)
########################################################
def controlTsBAD_NEIGHBOR(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    controlNeigbor(pair, 1)
    controlComandType(pair, 0)
########################################################
def controlTsBAD_ITEM(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    controlItem(pair, 1)
    controlComandType(pair, 0)
########################################################
def controlTsUNMOVABLE(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 2)
    controlComandType(pair, 0)
########################################################
def controlTsBAG_FULL(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 2)
    controlComandType(pair, 0)
########################################################
def controlTsNOT_IN_BAG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    controlComandType(pair, 0)
    controlNotInBag(pair)
########################################################
def controlTsHELP(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    controlComandType(pair, 0)
########################################################
def controlTsNS0_WrongCond(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 1)
    controlNonSType(pair)
########################################################
def controlTsNS1_WrongCond(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 2)
    controlNonSType(pair)
########################################################
def controlTsNS2_WrongCond(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 3)
    controlNonSType(pair)
########################################################
def controlTsNS3_WrongCond(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 4)
    controlNonSType(pair)
########################################################
def controlTsNS1_WRONG_ARG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 2)
    controlNonSType(pair)
########################################################
def controlTsNS2_WRONG_1stARG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 3)
    controlNonSType(pair)
########################################################
def controlTsNS2_WRONG_2ndARG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 3)
    controlNonSType(pair)
########################################################
def controlTsNS3_WRONG_1stARG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 4)
    controlNonSType(pair)
########################################################
def controlTsNS3_WRONG_2ndARG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 4)
    controlNonSType(pair)
########################################################
def controlTsNS3_WRONG_3rdARG(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 4)
    controlNonSType(pair)
########################################################
def controlTsNS1_0Args(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 1)
    controlNonSType(pair)
########################################################
def controlTsNS2_1Args(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 2)
    controlNonSType(pair)
########################################################
def controlTsNS3_012Args(pair):
    controlNonArgs(pair)
    controlNeigbors(pair, 1)
    controlSamePlace(pair, 1)
    controlSameBag(pair)
    verifyNumberOfArguments1(pair, 3)
    controlNonSType(pair)
########################################################
def requiredNSSteps():
    actions = nonStandardTypes.keys()
    requiredTypes = []
    for action in actions:
        typ = nonStandardTypes.get(action)
        if typ == "tsNS_0":
            requiredTitle = action + "_" + "tsNS0_WrongCond"
            requiredTypes.append(requiredTitle)
        if typ == "tsNS_1":
            requiredTitle = action + "_" + "tsNS1_WrongCond"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS1_0Args"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS1_WRONG_ARG"
            requiredTypes.append(requiredTitle)
        if typ == "tsNS_2":
            requiredTitle = action + "_" + "tsNS2_WrongCond"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS2_1Args"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS2_WRONG_1stARG"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS2_WRONG_2ndARG"
            requiredTypes.append(requiredTitle)
        if typ == "tsNS_3":
            requiredTitle = action + "_" + "tsNS3_WrongCond"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS3_012Args"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS3_WRONG_1stARG"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS3_WRONG_2ndARG"
            requiredTypes.append(requiredTitle)
            requiredTitle = action + "_" + "tsNS3_WRONG_3rdARG"
            requiredTypes.append(requiredTitle)
    return requiredTypes
########################################################
def bubleControl(pair):
    typ = pair.firstStep.typeOfStep.name
    if typ == "tsSTART":
        controlTsStart(pair)
    if typ == "tsNS_0":
        controlTsNS_0(pair)
    if typ == "tsNS_1":
        controlTsNS_1(pair)
    if typ == "tsNS_2":
        controlTsNS_2(pair)
    if typ == "tsNS_3":
        controlTsNS_3(pair)
    if typ == "tsNOT_START":
        controlTsNOT_START(pair)
    if typ == "tsEMPTY":
        controlTsEMPTY(pair)
    if typ == "tsUNKNOWN":
        controltsUNKNOWN(pair)
    if typ == "tsMOVE_WA":
        controlTsMOVE_WA(pair)
    if typ == "tsTAKE_WA":
        controlTsTAKE_WA(pair)
    if typ == "tsPUT_DOWN_WA":
        controlTsPUT_DOWN_WA(pair)
    if typ == "tsBAG_FULL":
        controlTsBAG_FULL(pair)
    if typ == "tsHELP":
        controlTsHELP(pair)
    if typ == "tsNS0_WrongCond":
        controlTsNS0_WrongCond(pair)
    if typ == "tsNS1_WrongCond":
        controlTsNS1_WrongCond(pair)
    if typ == "tsNS2_WrongCond":
        controlTsNS2_WrongCond(pair)
    if typ == "tsNS3_WrongCond":
        controlTsNS3_WrongCond(pair)
    if typ == "tsNS1_WRONG_ARG":
        controlTsNS1_WRONG_ARG(pair)
    if typ == "tsNS2_WRONG_1stARG":
        controlTsNS2_WRONG_1stARG(pair)
    if typ == "tsNS2_WRONG_2ndARG":
        controlTsNS2_WRONG_2ndARG(pair)
    if typ == "tsNS3_WRONG_1stARG":
        controlTsNS3_WRONG_1stARG(pair)
    if typ == "tsNS3_WRONG_2ndARG":
        controlTsNS3_WRONG_2ndARG(pair)
    if typ == "tsNS3_WRONG_3rdARG":
        controlTsNS3_WRONG_3rdARG(pair)
    if typ == "tsNS1_0Args":
        controlTsNS1_0Args(pair)
    if typ == "tsNS2_1Args":
        controlTsNS2_1Args(pair)
    if typ == "tsNS3_012Args":
        controlTsNS3_012Args(pair)
    typ = pair.secondStep.typeOfStep.name
    if typ == "tsTAKE":
        controlTsTake(pair)
    if typ == "tsGOTO":
        controlTsGoTo(pair)
    if typ == "tsPUT_DOWN":
        controlTsPutDown(pair)
    if typ == "tsBAD_NEIGHBOR":
        controlTsBAD_NEIGHBOR(pair)
    if typ == "tsBAD_ITEM":
        controlTsBAD_ITEM(pair)
    if typ == "tsNOT_IN_BAG":
        controlTsNOT_IN_BAG(pair)
    if typ == "tsUNMOVABLE":
        controlTsUNMOVABLE(pair)
    if typ == "tsEND":
        controlTsEND(pair)
########################################################
def makeBeautifulList(title, ourList):
    adding = ""
    beautifulString = title 
    i = 0
    while i < (len(title) - 4):
        adding = adding + " "
        i = i + 1
    b = 0
    line = ""
    if len(ourList) == 0:
        return beautifulString + "[]"
    types = str(ourList).split() 
    while b < len(types):
        line = line + str(types[b]) + " "
        if len(line) > 50:
            beautifulString = beautifulString + line + "\n" + adding
            line = ""
        else:
            if b == (len(types) - 1):
                beautifulString = beautifulString + line
        b = b + 1
    return beautifulString

########################################################        
def testMainSteps():
    start = (lepota + "\nAuthor: " + factory.authorName()   #!RP#
                    + "\nStart test scenario: "
                    + HAPPY_NAME + "\n" + lepota
            )
    print(start)
    status = 1

    i = 0
    while i < len(scenario.steps):
        step = scenario.steps[i]
        if step.typeOfStep in notUsedActions:
            notUsedActions.remove(step.typeOfStep)
        if(step.typeOfStep.name not in usedTypes):
            usedTypes.append(step.typeOfStep.name)
        for neigbor in step.neighbors:
            if neigbor not in knownPlaces:
                knownPlaces.append(neigbor)
        if step.place not in knownPlaces:
            knownPlaces.append(step.place)
        if step.place not in visitedPlaces:
            visitedPlaces.append(step.place)
        for item in step.items:
            if item not in hObjects:
                hObjects.append(item)
        if step.typeOfStep != tsSTART and step.command != '':
            comand = step.command.split()
            comand = comand[0]
            if comand not in usedComands:
                usedComands.append(comand)
    
        if step.typeOfStep not in happyActions and step.typeOfStep != tsEND:
            comand = step.command.split()
            comand = comand[0]
            if comand not in nonStandardActions:
                nonStandardActions.append(comand)
        print(str(i) + ".    " + step.typeOfStep.name + " - " + step.command)
        i = i + 1
    notUsedActionsNamed = []
    for typ in notUsedActions:
        notUsedActionsNamed.append(typ.name)
    print("\n" + makeBeautifulList("Nepokryté typy akcí: ", notUsedActionsNamed) + "\n")
    if len(notUsedActionsNamed) > 0:
        print("Takové typy akcí mají byt realizované, jinak test neprojde"+ "\n")
        status = 0
    stepsQuantity = "Počet kroků: " + str(len(scenario.steps)) + " " + ok   if len(
        scenario.steps) >= minSteps else "Počet kroků: " + str(len(scenario)) + " " + nonOk + " (min =" + str(minSteps) + ")"
    print(stepsQuantity + "\n")
    nonStandartActionsMessage = "Nestandardních akcí: " + \
        str(len(nonStandardActions)) + " "
    adding = ok if len(nonStandardActions) >= minOwnActions else nonOk + \
        " (min =" + str(minOwnActions) + ")" 
    nonStandartActionsMessage = nonStandartActionsMessage + \
        adding + str(nonStandardActions)
    print(nonStandartActionsMessage + "\n")
    knownPlacesMessage = "Zmíněných prostorů: " + str(len(knownPlaces)) + " "
    adding = ok if len(knownPlaces) >= minPlaces else nonOk + \
        " (min = " + str(minPlaces) + ")"
    knownPlacesMessage = knownPlacesMessage + adding + " " + str(knownPlaces)
    print(knownPlacesMessage + "\n")
    visitedPlacesMessage = "Navštívených prostorů: " + \
        str(len(visitedPlaces)) + " "
    adding = ok if len(visitedPlaces) >= minVisited else nonOk + \
        " (min = " + str(minVisited) + ")"
    visitedPlacesMessage = visitedPlacesMessage + \
        adding + " " + str(visitedPlaces)
    print(visitedPlacesMessage + "\n")
    usedComandsMessage = "Zadaných akcí: " + \
        str(len(usedComands)) + " " + str(usedComands)
    print(usedComandsMessage + "\n")
    unusedTypes = []
    for typ in allTypes:
        if typ not in usedTypes:
            unusedTypes.append(typ)
    unusedTypesMessage = "Nezadané typy kroků: " + \
        str(len(unusedTypes)) + " " 
    print(makeBeautifulList(unusedTypesMessage, unusedTypes) + "\n")
    nonUsedMandatory = []
    for typ in unusedTypes:
        if typ in happyActions:
            nonUsedMandatory.append(typ)
    nonUsedMandatoryMessage = "Z toho povinných: " + \
        str(len(nonUsedMandatory)) + " " + str(nonUsedMandatory)
    print(nonUsedMandatoryMessage + "\n")
    print("Navštívené prostory: " + str(visitedPlaces) + "\n")
    unvisited = []
    for place in knownPlaces:
        if place not in visitedPlaces:
            unvisited.append(place)
    print("Nenavštívené prostory: " + str(unvisited) + "\n")
    print(makeBeautifulList(("Zmíněné h-objekty: " + str(len(hObjects))+ " "), hObjects) + "\n")
    if len(notUsedActionsNamed) > 0 or len(knownPlaces) < minPlaces or len(visitedPlaces) < minVisited or len(nonStandardActions) < minOwnActions or len(scenario.steps) < minSteps:
        status = 0
    if scenario.steps[0].typeOfStep.name != "tsSTART":
        print("Scenař musi vždy se začinat krokem typu tsSTART" + "\n")
        status = 0
    if scenario.steps[len(scenario.steps) - 1].typeOfStep.name != "tsEND":
        print("Scenař musi vždy se ukončovat krokem typu tsEND" + "\n")
        status = 0
    if status == 1:
        i = 0
        while i < (len(scenario.steps) - 1):
            pair = Pair(scenario.steps[i], scenario.steps[i+1], i)
            bubleControl(pair)
            i = i + 1
            if len(erors) > 0:
                status = 0
                for eror in erors:
                    print(eror)
                break
    adding = "Test prošel" if status == 1 else "TEST NEPROŠEL"
    finish = lepota + "\n" + adding + "\n" + lepota
    print(finish)
########################################################


def testClasicMistakes():

    start = (lepota + "\nAuthor: " + factory.authorName()   #!RP#
                    + "\nStart test scenario: "
                    + MISTAKE_NAME + "\n" + lepota
            )
    print(start)
    status = 1
    i = 0
    while i < len(scenario.steps):
        step = scenario.steps[i]
        if step.typeOfStep in notUsedActions:
            notUsedActions.remove(step.typeOfStep)
        if(step.typeOfStep.name not in usedTypes):
            usedTypes.append(step.typeOfStep.name)
        for neigbor in step.neighbors:
            if neigbor not in knownPlaces:
                knownPlaces.append(neigbor)
        if step.place not in knownPlaces and step.place != '':
            knownPlaces.append(step.place)
        if step.place not in visitedPlaces and step.place != '':
            visitedPlaces.append(step.place)
        for item in step.items:
            if item not in hObjects:
                hObjects.append(item)
        if step.typeOfStep != tsSTART and step.typeOfStep != tsEMPTY:
            comand = step.command.split()
            comand = comand[0]
            if comand not in usedComands:
                usedComands.append(comand)
        
        if step.typeOfStep not in happyActions and step.typeOfStep != tsEND and step.typeOfStep != tsEMPTY:
            comand = step.command.split()
            comand = comand[0]
            if comand not in nonStandardActions:
                nonStandardActions.append(comand)
        print(str(i) + ".    " + step.typeOfStep.name + " - " + step.command)
        i = i + 1
    notUsedActionsNamed = []
    for typ in notUsedActions:
        notUsedActionsNamed.append(typ.name)
    print("\n" + makeBeautifulList("Nepokryté typy akcí: ", notUsedActionsNamed) + "\n")
    if len(notUsedActionsNamed) > 0:
        print("Takové typy akcí mají byt realizované, jinak test neprojde" + "\n")
        status = 0
    stepsQuantity = "Počet kroků: " + str(len(scenario.steps))
    print(stepsQuantity + "\n")
    nonStandartActionsMessage = "Nestandardních akcí: " + \
        str(len(nonStandardActions)) + " "
    print(nonStandartActionsMessage + "\n")
    knownPlacesMessage = "Zmíněných prostorů: " + \
        str(len(knownPlaces)) + " " + str(knownPlaces)
    print(knownPlacesMessage + "\n")
    visitedPlacesMessage = "Navštívených prostorů: " + \
        str(len(visitedPlaces)) + " " + str(visitedPlaces)
    print(visitedPlacesMessage + "\n")
    usedComandsMessage = "Zadaných akcí: " + \
        str(len(usedComands)) + " " + str(usedComands)
    print(usedComandsMessage + "\n")
    unusedTypes = []
    for typ in allTypes:
        if typ not in usedTypes:
            unusedTypes.append(typ)
    unusedTypesMessage = "Nezadané typy kroků: " + \
        str(len(unusedTypes)) + " " 
    print(makeBeautifulList(unusedTypesMessage, unusedTypes) + "\n")
    nonUsedMandatory = []
    for typ in unusedTypes:
        if typ in happyActions:
            nonUsedMandatory.append(typ)
    nonUsedMandatoryMessage = "Z toho povinných: " + \
        str(len(nonUsedMandatory)) + " " + str(nonUsedMandatory)
    print(nonUsedMandatoryMessage + "\n")
    print("Navštívené prostory: " + str(visitedPlaces) + "\n")
    unvisited = []
    for place in knownPlaces:
        if place not in visitedPlaces:
            unvisited.append(place)
    print("Nenavštívené prostory: " + str(unvisited) + "\n")
    print(makeBeautifulList(("Zmíněné h-objekty: " + str(len(hObjects))+ " "), hObjects) + "\n")
    if scenario.steps[0].typeOfStep.name != "tsNOT_START":
        print("Scenař musi vždy se začinat krokem typu tsNOT_START" + "\n")
        status = 0
    if scenario.steps[len(scenario.steps) - 1].typeOfStep.name != "tsEND":
        print("Scenař musi vždy se ukončovat krokem typu tsEND" + "\n")
        status = 0
    if status == 1:
        i = 0
        while i < (len(scenario.steps) - 1):
            pair = Pair(scenario.steps[i], scenario.steps[i+1], i)
            bubleControl(pair)
            i = i + 1
            if len(erors) > 0:
                status = 0
                for eror in erors:
                    print(eror)
                break
    adding = "Test prošel" if status == 1 else "TEST NEPROŠEL"
    finish = lepota + "\n" + adding + "\n" + lepota
    print(finish)
########################################################
#########################################################


def testMistakesNS():

    start = (lepota + "\nAuthor: " + factory.authorName()    #!RP#
                    + "\nStart test scenario: "
                    + MISTAKE_NS_NAME + "\n" + lepota
            )
    print(start)
    status = 1
    i = 0
    while i < len(scenario.steps):
        step = scenario.steps[i]
        if step.typeOfStep != tsSTART and step.command != '':
            comand = step.command.split()
            comand = comand[0].lower()
            title = comand + "_" + step.typeOfStep.name
            if title in notUsedActions:
                notUsedActions.remove(title)
        if(step.typeOfStep.name not in usedTypes):
            usedTypes.append(step.typeOfStep.name)
        for neigbor in step.neighbors:
            if neigbor not in knownPlaces:
                knownPlaces.append(neigbor)
        if step.place not in knownPlaces:
            knownPlaces.append(step.place)
        if step.place not in visitedPlaces:
            visitedPlaces.append(step.place)
        for item in step.items:
            if item not in hObjects:
                hObjects.append(item)
        if step.typeOfStep != tsSTART and step.typeOfStep != tsEMPTY and step.command != '':
            comand = step.command.split()
            comand = comand[0]
            if comand not in usedComands:
                usedComands.append(comand)
        
        if step.typeOfStep not in happyActions and step.typeOfStep != tsEND and step.typeOfStep != tsEMPTY:
            comand = step.command.split()

            comand = comand[0]
            if comand not in nonStandardActions:
                nonStandardActions.append(comand)
        print(str(i) + ".    " + step.typeOfStep.name + " - " + step.command)
        i = i + 1
    ###############################################################################################
    # Kontrola jsou-li v scenario Mistakes_NS nestandardni typy odlišne od standardnich typu Happy scenario
    nonStandardActionsLower = []
    for act in nonStandardActions:
        nonStandardActionsLower.append(act.lower())
    happyNSLower = []
    for act in happyNS:
        happyNSLower.append(act.lower())
    indikator = 0
    for act in nonStandardActionsLower:
        if act not in happyNSLower:
            indikator = 1
    if len(nonStandardActionsLower) != len(happyNSLower):
        indikator = 1
    if indikator == 1:
        print("Nestandartní typy v Happy scenario a Mistakes_NS scenario nemají se lišit. HappyNS:" +
              str(happyNSLower) + " Mistakes_NS:" + str(nonStandardActionsLower)+ "\n")
        status == 0
    ###############################################################################################
    notUsedActionsNamed = []
    for typ in notUsedActions:
        notUsedActionsNamed.append(typ)
    print("\n" + makeBeautifulList("Nepokryté typy akcí: ", notUsedActionsNamed) + "\n")
    if len(notUsedActionsNamed) > 0:
        print("Takové typy akcí mají byt realizované, jinak test neprojde" + "\n")
        status = 0
    stepsQuantity = "Počet kroků: " + str(len(scenario.steps))
    print(stepsQuantity + "\n")
    nonStandartActionsMessage = "Nestandardních akcí: " + \
        str(len(nonStandardActions)) + " " + str(nonStandardActions)
    print(nonStandartActionsMessage + "\n")
    knownPlacesMessage = "Zmíněných prostorů: " + \
        str(len(knownPlaces)) + " " + str(knownPlaces)
    print(knownPlacesMessage + "\n")
    visitedPlacesMessage = "Navštívených prostorů: " + \
        str(len(visitedPlaces)) + " " + str(visitedPlaces)
    print(visitedPlacesMessage + "\n")
    usedComandsMessage = "Zadaných akcí: " + \
        str(len(usedComands)) + " " + str(usedComands)
    print(usedComandsMessage + "\n")
    unusedTypes = []
    for typ in allTypes:
        if typ not in usedTypes:
            unusedTypes.append(typ)
    unusedTypesMessage = "Nezadané typy kroků: " + \
        str(len(unusedTypes)) + " "
    
    print(makeBeautifulList(unusedTypesMessage, unusedTypes) + "\n")
    nonUsedMandatory = []
    for typ in unusedTypes:
        if typ in happyActions:
            nonUsedMandatory.append(typ)
    nonUsedMandatoryMessage = "Z toho povinných: " + \
        str(len(nonUsedMandatory)) + " " + str(nonUsedMandatory)
    print(nonUsedMandatoryMessage + "\n")
    print("Navštívené prostory: " + str(visitedPlaces) + "\n")
    unvisited = []
    for place in knownPlaces:
        if place not in visitedPlaces:
            unvisited.append(place)
    print("Nenavštívené prostory: " + str(unvisited) + "\n")
    print(makeBeautifulList(("Zmíněné h-objekty: " + str(len(hObjects))+ " "), hObjects) + "\n")
    if scenario.steps[0].typeOfStep.name != "tsSTART":
        print("Scenař musi vždy se začinat krokem typu tsSTART " + "\n")
        status = 0
    if scenario.steps[len(scenario.steps) - 1].typeOfStep.name != "tsEND":
        print("Scenař musi vždy se ukončovat krokem typu tsEND" + "\n")
        status = 0
    if status == 1:
        i = 0
        while i < (len(scenario.steps) - 1):
            pair = Pair(scenario.steps[i], scenario.steps[i+1], i)
            bubleControl(pair)
            i = i + 1
            if len(erors) > 0:
                status = 0
                for eror in erors:
                    print(eror)
                break
    adding = "Test prošel" if status == 1 else "TEST NEPROŠEL"
    finish = lepota + "\n" + adding + "\n" + lepota
    print(finish)


###############################

def test(fact):        #!RP#
    """Metoda otestuje trojici scénářů poskytovanou zadanou továrnou.
    """
    global factory, scenario, happyActions, notUsedActions
    global knownPlaces, visitedPlaces, nonStandardActions, hObjects
    global usedComands, usedTypes, allTypes, erors, status, happyNS
    global comandsByType, nonStandardTypes
    global minSteps, minPlaces, minVisited, minOwnActions, ok, nonOk

    init_for_factory(fact)

    testMainSteps()
    print()
    # print(comandsByType)
    # print(nonStandardTypes)
    happyNS = nonStandardActions
    scenario = factory.scenarios()[1]
    happyActions = [tsSTART, tsNOT_START, tsEMPTY, tsUNKNOWN, tsMOVE_WA, tsTAKE_WA, tsPUT_DOWN_WA,
                    tsBAD_NEIGHBOR, tsBAD_ITEM, tsUNMOVABLE, tsTAKE, tsBAG_FULL, tsNOT_IN_BAG, tsHELP, tsEND]
    notUsedActions = [tsSTART, tsNOT_START, tsEMPTY, tsUNKNOWN, tsMOVE_WA, tsTAKE_WA, tsPUT_DOWN_WA,
                      tsBAD_NEIGHBOR, tsBAD_ITEM, tsUNMOVABLE, tsTAKE, tsBAG_FULL, tsNOT_IN_BAG, tsHELP, tsEND]
    knownPlaces = []
    visitedPlaces = []
    nonStandardActions = []
    hObjects = []
    usedComands = []
    usedTypes = []
    erors = []
    status = 1


    testClasicMistakes()
    print()
    # print(comandsByType)
    # print(nonStandardTypes)
    scenario = factory.scenarios()[2]
    happyActions = [tsSTART, tsGOTO, tsTAKE, tsPUT_DOWN]
    notUsedActions = requiredNSSteps()
    knownPlaces = []
    visitedPlaces = []
    nonStandardActions = []
    hObjects = []
    usedComands = []
    usedTypes = []
    erors = []
    status = 1


    testMistakesNS()

############################################################################

