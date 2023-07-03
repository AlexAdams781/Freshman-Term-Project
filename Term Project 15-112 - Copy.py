'''

Kard Kombos!

By Alex Adams

Lecture 2


Goal: Create a functioning card game

Game Rules:

1) User faces off against an AI of ranging difficulty.  Goal is to get the
most combinations of cards at the end.  Points are calculated by (# of
combinations) x (# of total cards).

2) Each game starts with options allowing the user to choose the AI difficulty
level and if he/she wants to play without memorizing the combos.

3) Before play starts, a list of 5-6 randomly generated card combinations of 2-6
lengths are presented to the user.  User must try to memorize all the
combinations before time limit. 

4) Game setup: There exists a deck of 52 or so cards.  13 are red, 13 are 
yellow, 13 are blue, and 13 are green.  9 cards are dealt on the 'table'.  Also,
players are dealt 3 cards as a 'hand'.

5) Players take turns making legal combinations out of the cards on the table
and in 'hand'.  After each turn, board replaces taken cards but leaves 1 less.

6) Key strategy in this game is to memorize the legal combinations before game
starts.  User must form combinations from memory.

7) If user forms an illegal combo, user passes and turn is skipped.

8) If player takes all cards on table, player goes again.

9) Game ends when everyone passes in one round.

10) Multiple games are played before total points are counted and winner is
declared.

Coding:

1) Will implement classes for the cards and players.  Not sure exactly how to do
this, since this will be a very large program.

2) Will also add a screen that lists all the rules.  Beginner/New users can
access this

3) AI difficulty will vary.  Easy AI will be easy to code.  Might explore
Monte Carlo methods for coding advanced AI.

4) Will also code an algorithm that generates random legal combinations for each
game.

5) 15-112 Graphics module will be used to animate the game.  At the very least,
UI will show cards on the table, cards in hand, and the deck.  Will consider
implementing higher quality animation such as: card movements, background
design, and screen transitions

'''

import random
from cmu_112_graphics import *
import copy
import math

print('hi')

# each card in the deck is a card object
class Card:
    colors = ['red', 'green', 'blue', 'yellow', 'black', 'brown']

    def __init__(self, color, isFaceUp):
        self.color = color
        self.faceDownColor = 5
        self.selectedColor = 4
        self.isFaceUp = isFaceUp
        self.isSelected = False

    # Creates a deck of 52 cards and shuffles it
    def getDeck(): 
        deck = []
        for i in range(4):
            for j in range(13):
                deck.append(Card(i, False))
        random.shuffle(deck)
        return deck

    # Generates a random combo of length num
    def getCombination(num):
        combo = []
        for i in range(num):
            color = random.randint(0,3)
            freq = combo.count(color)
            while freq > 3:
                color = random.randint(0,3)
                freq = combo.count(color)
            combo.append(Card(color, True))
        return combo

# Creates a set of 6 different combos of various lengths
    def getLegalCombinations():
        combosSizes = [2,2,3,4,5,6]
        combos = []
        numOfCombos = 6
        combos = [[] for i in range (6)]
        for combo in range(numOfCombos):
            sameCombo = True
            moreThan4 = True
            while sameCombo:
                L = Card.getCombination(combosSizes[combo])
                sameCombo = L in combos
                if not (L.count('red') == 4 or L.count('yellow') == 4 or \
                L.count('green') == 4 or L.count('blue') == 4):
                    moreThan4 = False
            combos[combo] = L
        return combos

    # following methods allow cards to be flipped or selected for combos
    def faceup(self):
        self.isFaceUp = True

    def facedown(self):
        self.isFaceUp = False

    def selected(self):
        self.isSelected = True

    def unselected(self):
        self.isSelected = False

    def select(self):
        return self.isSelected

    def __repr__(self):
        if self.isSelected:
            return (Card.colors[self.selectedColor])
        elif self.isFaceUp:
            return (Card.colors[self.color])
        else:
            return (Card.colors[self.faceDownColor])

    def __eq__(self, other):
        return (isinstance(other, Card) and (self.color == other.color))

def setup():
    # gets cards on table from deck and also gets player and ai hand cards
    tableCards = []
    playerHand = []
    aiHand = []
    deck = Card.getDeck()
    for i in range(9):
        card = deck[i]
        Card.faceup(card)
        tableCards.append(card)
    deck = deck[9:]
    for i in range(3):
        card = deck[i]
        Card.faceup(card)
        playerHand.append(card)
    deck = deck[3:]
    for i in range(3):
        card = deck[i]
        aiHand.append(card)
    deck = deck[3:]
    combinations = Card.getLegalCombinations()
    # also returns legal combinations
    return tableCards, playerHand, aiHand, deck, combinations

def findTableCardPos(app):
    # returns a list of coordinate points. These represent the top left corner of
    # all cards on table
    length = len(app.tableCards)
    if length == 0:
        return []
    cardPos = []
    rows = ((length-1)//4)+1
    cols = math.ceil(length/rows)
    margin = 10
    startPosXCor = app.tableCardsXCor - (cols*(app.cardWidth + margin) - margin)/2
    startPosYCor = app.tableCardsYCor - (rows*(app.cardHeight + margin) - margin)/2
    for r in range(rows):
        for c in range(cols):
            # following conditionals are organized so that the last card in a 5 or 7
            # card set is not added to the card positions list
            if not (length == 5 or length == 7):
                cardPos.append((startPosXCor + c*(app.cardWidth + margin), \
                startPosYCor + r*(app.cardHeight + margin)))
            elif r != 1 or c != cols-1:
                cardPos.append((startPosXCor + c*(app.cardWidth + margin), \
                startPosYCor + r*(app.cardHeight + margin)))
    return cardPos

def findPlayerCardPos(app, player):
    # same thing as last function but finds player or ai hand cards instead
    cardPos = []
    margin = 10
    if player == 'player':
        handLength = len(app.playerHand)
        for i in range(handLength):
            cardPos.append((app.playerHandXCor - (handLength*(app.cardWidth + margin) - margin)//2 + i*(margin + app.cardWidth),
            app.playerHandYCor - app.cardHeight//2))
    else:
        handLength = len(app.aiHand)
        for i in range(handLength):
            cardPos.append((app.aiHandXCor - (handLength*(app.cardWidth + margin) - margin)//2 + i*(margin + app.cardWidth),
            app.aiHandYCor - app.cardHeight//2))
    return cardPos

def appStarted(app):
    # lists all variables used throughout the mvc
    app.aiTurn = False
    app.tableCardsXCor = app.width//2
    app.tableCardsYCor = app.height//2
    app.playerHandXCor = app.width//2
    app.playerHandYCor = app.height*7//8
    app.playerMeldsXCor = app.width//2
    app.playerMeldsYCor = app.height*3//4
    app.aiMeldsXCor = app.width//2
    app.aiMeldsYCor = app.height//4
    app.aiHandXCor = app.width//2
    app.aiHandYCor = app.height//8
    app.deckXCor = app.width*3//4
    app.deckYCor = app.height//2
    app.cardWidth = app.width//20
    app.cardHeight = app.height//12
    app.tableCards, app.playerHand, app.aiHand, app.deck, app.combos = setup()
    app.isStartGame = True
    app.choseDifficultyLevel = False
    app.isMemorizeCombos = False
    app.isCombinationsBanner = True
    app.turnBanner = False
    app.isUserTurn = False
    app.isEndRound = False
    app.isEndGame = False
    app.isRulesBanner = False
    app.passCount = 0
    app.time = 0
    app.playerNumOfCards, app.playerNumOfCombos = 0, 0
    app.aiNumOfCards, app.aiNumOfCombos = 0, 0
    app.tableCardPositions = findTableCardPos(app)
    app.playerCardPositions = findPlayerCardPos(app, 'player')
    app.aiCardPositions = findPlayerCardPos(app, 'ai')
    app.playerMeldFormation = []
    app.playerMelds = []
    app.aiMelds = []
    app.gameText = 'Your Turn.'
    app.difficulty = ''
    app.userRoundScore, app.aiRoundScore = 0, 0
    app.userTotalScore, app.aiTotalScore = 0, 0
    app.round = 1

# this section deals with AI gameplay

def findLongestCombo(app, lessCombos):
    # used for easy difficulty
    # starts with longest memorized combo and returns it if possible to make
    # if not, then goes to next longest combo
    for combo in lessCombos[::-1]:
        if len(combo) != 0 and isLegal(app.tableCards, app.aiHand, combo):
            return combo
    return 'pass'

def basicAI(app):
    # both easy and medium difficulties are stored here and uses lessCombos as app.combos
    # medium difficulty uses advancedAI but with less combos to choose from
    lessCombos = []
    memoryProb = [0.95, 0.95, 0.9, 0.8, 0.7, 0.5]
    for i in range(len(app.combos)):
        if random.random() < memoryProb[i]:
            lessCombos.append(app.combos[i])
        else:
            lessCombos.append([])
    if app.difficulty == 'intermediate':
        return advancedAI(app, lessCombos)
    return findLongestCombo(app, lessCombos)

def emptyTable(tableCards, hand, combo):
    # returns true if player can sweep the table given the combo, table of cards and hand
    if not isLegal(tableCards, hand, combo):
        return False
    tempTable = copy.copy(tableCards)
    tempCards = copy.copy(hand)
    tempCombo = copy.copy(combo)
    for card in tempCards:
        Card.faceup(card)
    # first checks if all cards in table are in combo
    # then checks if all cards in combo (not on table) are in the hand
    for color in tempTable:
        if color not in tempCombo:
            return False
        tempCombo.remove(color)
    for color in tempCombo:
        if color not in tempCards:
            return False
        tempCards.remove(color)
    return True

def isLegal(tableCards, hand, combo):
    # returns true of a combo can be made, given player's hand and cards on table
    tempTable = copy.copy(tableCards)
    tempCards = copy.copy(hand)
    for color in combo:
        if color in tempTable:
            tempTable.remove(color)
        elif color in tempCards:
            tempCards.remove(color)
        else:
            return False
    return True

def simulateRepeatTurn(app, combo):
    # simulates 1000 scenarios where the AI makes a certain combo
    # the card replacements on the table and opponent's hand are randomized from the deck
    length = len(combo)
    isGoAgain = 0
    passes = 0
    SumComboLength = 0
    countCombos = 0
    for i in range(1000):
        playerHand = []
        tempTable = copy.copy(app.tableCards)
        tempHand = copy.copy(app.aiHand)
        for card in tempHand:
            Card.faceup(card)
        deck = copy.copy(app.deck)
        random.shuffle(deck) # important line here that allows simulations to be different each
        index = -1
        for color in combo:
            if color in tempTable:
                tempTable.remove(color)
                index += 1
            elif color in tempHand:
                tempHand.remove(color)
            else:
                continue
        # adds new cards to opponent's hand and table
        newDeckCards = deck[:index]
        playerHand = deck[index:index+len(app.playerHand)]
        for card in newDeckCards:
            Card.faceup(card)
        for card in playerHand:
            Card.faceup(card)
        tempTable.extend(newDeckCards)
        comboFound = False
        isTableSwept = False
        # once a combo is found, finds its length
        # loops through all combos to see if any one can sweep the table and records that
        for playerCombo in app.combos[::-1]:
            if (not isTableSwept) and emptyTable(tempTable, playerHand, playerCombo):
                isGoAgain += 1
                isTableSwept = True
            if (not comboFound) and isLegal(tempTable, playerHand, playerCombo):
                SumComboLength += len(playerCombo)
                countCombos += 1
                comboFound = True
        if not comboFound: # records a pass if no combos found
            passes += 1
    if SumComboLength == 0:
            countCombos = 1
    return isGoAgain/1000, passes/1000, SumComboLength/countCombos

def findCardsLeft(app, combo):
    # finds number of cards in AI hand after making a combo
    tempTable = copy.copy(app.tableCards)
    tempCards = copy.copy(app.aiHand)
    for color in combo:
        if color in tempTable:
            tempTable.remove(color)
        elif color in tempCards:
            tempCards.remove(color)
    return len(tempCards)

def advancedAI(app, combos):
    # returns the most optimal combo to make
    paths = []
    weightList = [0.25, 0.25, 0.2, 0.2, 0.1] # important line that assigns weights certain attributes to strategy
    goAgainRateList = [] # assigns probability of opponent sweeping table next turn
    passesRateList = [] # assigns probability of opponent passing next turn
    handUsageRateList = [] # assigns num of cards from hand used and scales it from 0 to 1
    AIComboLengthRateList = [] # assigns length of combo made
    userComboLengthRateList = [] # assigns avg length of combo that opponent made next turn
    totalRateList = []
    tempCombos = copy.copy(combos)
    for combo in tempCombos:
        if isLegal(app.tableCards, app.aiHand, combo):
            paths.append(combo)
    paths.reverse()
    for path in paths:
        if emptyTable(app.tableCards, app.aiHand, path): # returns any combo if can be used to sweep table
            return path
    print('paths', paths, app.tableCards, app.aiHand)
    for path in paths:
        # simulates for each combo that AI can make
        # rates each attribute on a 0-1 scale. 0 is best. 1 is worst.
        goAgainRate, passesRate, avgComboLength = simulateRepeatTurn(app, path)
        cardsLeft = findCardsLeft(app, path)
        goAgainRateList.append(goAgainRate)
        passesRateList.append(1-passesRate)
        handUsageRateList.append(1-cardsLeft/len(app.aiHand))
        AIComboLengthRateList.append(1-0.25*(len(path) - 2))
        userComboLengthRateList.append(0.25*(avgComboLength - 2))
    if len(paths) == 0:
        return 'pass'
    else:
        for i in range(len(goAgainRateList)):
            # this is where the weight come into play
            totalRateList.append(weightList[0]*goAgainRateList[i] + weightList[1]*passesRateList[i] + \
            weightList[2]*handUsageRateList[i] + \
            weightList[3]*AIComboLengthRateList[i] + weightList[4]*userComboLengthRateList[i])
        bestTotalRate = min(totalRateList)
        print(goAgainRateList, 'opponent sweeps deck')
        print(passesRateList, 'opponent passes')
        print(handUsageRateList, 'aihandusage')
        print(AIComboLengthRateList, 'avg AI combo length')
        print(userComboLengthRateList, ' avg userCombo length')
        print(totalRateList, 'ovr score')
        print('takes the path with the lowest score')
        index = totalRateList.index(bestTotalRate)
        return paths[index]

def CPUSelectCards(app, combo):
    # given combo, selects cards used for the combo on table and in the AI hand
    unselectedTableCards = copy.copy(app.tableCards)
    unselectedAIHand = copy.copy(app.aiHand)
    for color in combo:
        if color in unselectedTableCards:
            index = app.tableCards.index(color)
            Card.selected(app.tableCards[index])
            unselectedTableCards.remove(color)
        elif color in unselectedAIHand:
            index = app.aiHand.index(color)
            Card.selected(app.aiHand[index])
            unselectedAIHand.remove(color)

def CPUTurn(app):
    # first, finds the correct combo based on AI difficulty level
    passed = False
    tempCombosList = copy.copy(app.combos)
    if app.difficulty == 'hard':
        combo = advancedAI(app, app.combos)
    else:
        combo = basicAI(app)
    for card in app.aiHand:
        Card.facedown(card)
    if combo != 'pass':
        app.aiMelds.append(combo)
        CPUSelectCards(app, combo)
        app.passCount = 0 # important lines here. By the rules, round ends when both the CPU and user pass
        # app.passCount must reach 2 without any interruptions
    else:
        passed = True
    if passed:
        app.passCount += 1 #
        if app.passCount == 2: # if passCount = 2, proceeds to end round screen
            app.isEndRound = True
            endRound(app)
    replaceNum = replaceTable(app)
    fixHand(app, 'ai')
    if replaceNum != len(app.tableCards):
        # applied if had to replace all cards on table -> CPU swept table
        app.isUserTurn = True
        app.gameText = 'Your Turn.'
    else:
        # skips over user's turn
        app.gameText = 'CPU Goes Again.'
        CPUTurn(app)
    if passed:
        app.gameText = 'CPU Passed. Your Turn.'

# this section deals with user gameplay

def selectCards(app):
    # if the mouse click is in any of the cards on table, adds card to meld and
    # turns it black
    for i in range(len(app.tableCardPositions)):
        if app.cx > app.tableCardPositions[i][0] and app.cx < app.tableCardPositions[i][0] + app.cardWidth \
        and app.cy > app.tableCardPositions[i][1] and app.cy < app.tableCardPositions[i][1] + app.cardHeight:
            app.playerMeldFormation.append(app.tableCards[i])
            Card.selected(app.tableCards[i])
    overlapCards = []
    # same thing but with the cards in the player's hand
    for i in range(len(app.playerCardPositions)):
        if app.cx > app.playerCardPositions[i][0] and app.cx < app.playerCardPositions[i][0] + app.cardWidth \
        and app.cy > app.playerCardPositions[i][1] and app.cy < app.playerCardPositions[i][1] + app.cardHeight:
            overlapCards.append(i)
    if len(overlapCards) != 0:
        cardIndex = max(overlapCards)
        print(app.playerHand, overlapCards)
        app.playerMeldFormation.append(app.playerHand[cardIndex])
        Card.selected(app.playerHand[cardIndex])

def replaceTable(app):
    # called when a turn is finished
    # replaces all but one used cards on table with fresh ones from the deck
    prevNumOfCards = len(app.tableCards)
    newTableCards = []
    numOfCards = 0
    for card in app.tableCards:
        if not Card.select(card):
            numOfCards += 1
            newTableCards.append(card)
        else:
            Card.unselected(card)
    replaceNum = prevNumOfCards - numOfCards - 1 # all but one card gets replaced
    for i in range(replaceNum):
        card = app.deck[i]
        Card.faceup(card)
        newTableCards.append(card)
    app.deck = app.deck[replaceNum:]
    # updates table with the newly generated cards
    app.tableCards = newTableCards
    app.tableCardPositions = findTableCardPos(app)
    return replaceNum

def fixHand(app, turn):
    # removes all used cards and updates positions
    if turn == 'player':
        i = 0
        while i < len(app.playerHand):
            if Card.select(app.playerHand[i]):
                app.playerHand.pop(i)
            else:
                i += 1
        app.playerCardPositions = findPlayerCardPos(app, turn)
    else:
        i = 0
        while i < len(app.aiHand):
            if Card.select(app.aiHand[i]):
                app.aiHand.pop(i)
            else:
                i += 1
        app.aiCardPositions = findPlayerCardPos(app, turn)

def findNumOfCards(app, player):
    # goes through each card in each completed combo and returns count of all cards
    if player == 'user':
        melds = app.playerMelds
    else:
        melds = app.aiMelds
    cardNum = 0
    for i in melds:
        for j in i:
            cardNum += 1
    return cardNum, len(melds)

# this section deals with mousePressed

def endTurn(app):
    goAgain = False
    turnXCor = 220
    turnYCor = 340
    passXCor = 120
    passYCor = 340
    # if user presses 'done', goes through following sequence
    if app.cx > turnXCor - 40 and app.cx < turnXCor + 40 \
    and app.cy > turnYCor - 30 and app.cy < turnYCor + 30:
        # updates table and hand if meld is legal
        if app.playerMeldFormation in app.combos:
            app.playerMelds.append(app.playerMeldFormation)
            replaceNum = replaceTable(app)
            fixHand(app, 'player')
            for card in app.playerMeldFormation:
                Card.unselected(card)
            if replaceNum == len(app.tableCards):
                goAgain = True
        # reassigns cards and hands variables to their backup if illegal
        else:
            app.passCount += 1
            for card in app.playerMeldFormation:
                Card.unselected(card)
        app.passCount = 0
    # applies if user presses 'pass'
    elif app.cx > passXCor - 40 and app.cx < passXCor + 40 \
    and app.cy > passYCor - 30 and app.cy < passYCor + 30:
        # in this case, all cards are unselected and passCount is increased
        for card in app.playerMeldFormation:
            Card.unselected(card)
        app.passCount += 1
        if app.passCount == 2:
            app.isEndRound = True
            endRound(app)
    else:
        return None
    app.playerMeldFormation = []
    if not goAgain:
        app.isUserTurn = False
    else:
        app.gameText = 'Go Again.'

def endRound(app):
    # updates the scores of the ai and the player after each round
    app.playerNumOfCards, app.playerNumOfCombos = findNumOfCards(app, 'user')
    app.aiNumOfCards, app.aiNumOfCombos = findNumOfCards(app, 'ai')
    app.userRoundScore = app.playerNumOfCards*app.playerNumOfCombos
    app.aiRoundScore = app.aiNumOfCards*app.aiNumOfCombos
    app.userTotalScore += app.userRoundScore
    app.aiTotalScore += app.aiRoundScore

def redoTurn(app):
    # applies if user presses 'start over'
    # all cards are unselected
    xCor = 220
    yCor = 260
    if app.cx > xCor - 40 and app.cx < xCor + 40 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        for card in app.tableCards:
            Card.unselected(card)
        for card in app.playerHand:
            Card.unselected(card)
        app.playerMeldFormation = []

# following 3 functions are buttons that when pressed, set the ai difficulty level
def easy(app):
    xCor = app.width//2
    yCor = 200
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.difficulty = 'easy'
        app.choseDifficultyLevel = True

def medium(app):
    xCor = app.width//2
    yCor = 300
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.difficulty = 'intermediate'
        app.choseDifficultyLevel = True

def hard(app):
    xCor = app.width//2
    yCor = 400
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.difficulty = 'hard'
        app.choseDifficultyLevel = True
        print('hey')

# the 2 functions below are associated with whether or not the user decides to memorize the combos
def useComboBanner(app):
    xCor = app.width//2
    yCor = app.height*2//3
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.isStartGame = False

def memorizeCombos(app):
    xCor = app.width//2
    yCor = app.height//2
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.isStartGame = False
        app.isMemorizeCombos = True

# allows user to look at combinations when pressing 'kombos' button only if correct mode
def getCombinationsBanner(app):
    xCor = 120
    yCor = 260
    if not app.isMemorizeCombos:
        if app.cx > xCor - 40 and app.cx < xCor + 40 \
        and app.cy > yCor - 30 and app.cy < yCor + 30:
            app.isCombinationsBanner = True
            app.isUserTurn = False

# gets user back into the game
# also allows CPU to go first on even-numbered rounds
def exitCombinationsBanner(app):
    if app.isCombinationsBanner and (not app.isStartGame):
        if app.cx > app.width*2//5 and app.cx < app.width*3//5 and app.cy > app.height*7//10 \
        and app.cy < app.height*4//5:
            app.isCombinationsBanner = False
            if app.round % 2 == 0 and len(app.tableCards) == 9:
                app.isUserTurn = False
            else:
                app.isUserTurn = True
                app.gameText = 'Your Turn.'

# allows user to see rules of the game when pressing 'rules'
def getRulesBanner(app):
    xCor = 70
    yCor = app.height - 60
    if app.cx > xCor - 40 and app.cx < xCor + 40 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.isRulesBanner = True

# gets user back into game from rules
def rulesToGame(app):
    xCor = app.width*7//8 - 60
    yCor = app.height//8 + 50
    if app.cx > xCor - 40 and app.cx < xCor + 40 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        app.isRulesBanner = False

# resets game if user presses 'reset' button
def resetGame(app):
    xCor = app.width - 70
    yCor = 60
    if app.cx > xCor - 40 and app.cx < xCor + 40 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        appStarted(app)

# when user presses 'next round' resets game but records ai difficulty level and total scores
def nextRound(app):
    xCor = app.width//2
    yCor = app.height*4//5
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        roundNum = app.round + 1
        if roundNum == 7:
            app.isEndGame = True
        difficulty = app.difficulty
        userScore, aiScore = app.userTotalScore, app.aiTotalScore
        appStarted(app)
        app.isStartGame = False
        app.difficulty = difficulty
        app.userTotalScore, app.aiTotalScore = userScore, aiScore
        app.round = roundNum

# resets game when user presses 'new game'
def newGame(app):
    xCor = app.width//2
    yCor = app.height*3//4
    if app.cx > xCor - 80 and app.cx < xCor + 80 \
    and app.cy > yCor - 30 and app.cy < yCor + 30:
        appStarted(app)

def mousePressed(app, event):
    #assigns variables to mouse coordinates and goes throuh following functions
    app.cx = event.x
    app.cy = event.y
    if app.isStartGame:
        if app.choseDifficultyLevel:
            memorizeCombos(app)
            useComboBanner(app)
        else:
            easy(app)
            medium(app)
            hard(app)
    if app.isCombinationsBanner:
        exitCombinationsBanner(app)
    if app.isRulesBanner:
        rulesToGame(app)
    if app.isUserTurn:
        selectCards(app)
        redoTurn(app)
        endTurn(app)
        getCombinationsBanner(app)
    if app.isEndRound:
        nextRound(app)
    if app.isEndGame:
        newGame(app)
    if not (app.isStartGame or app.isCombinationsBanner):
        resetGame(app)
        getRulesBanner(app)



# 2 reasons timerFired is used
# delays CPU to 3 seconds after user finishes turn until it makes its decision
# Small dot animation for waiting sign during CPU's turn
def timerFired(app):
    if not app.isEndRound:
        if app.time > 30:
            app.time = 0
            CPUTurn(app)
        elif not app.isUserTurn and not app.isCombinationsBanner and not app.isRulesBanner:
            if app.gameText != 'CPU Goes Again.':
                if (app.time//5) % 2 == 0:
                    app.gameText = 'Waiting . . . '
                else:
                    app.gameText = 'Waiting  . . .'
            app.time += 1


# this section deals with reDraw All

def drawTableCards(app, canvas):
    # draws each table card from the positions
    length = len(app.tableCardPositions)
    for i in range(length):
        color = app.tableCards[i]
        canvas.create_rectangle(app.tableCardPositions[i][0], app.tableCardPositions[i][1], \
        app.tableCardPositions[i][0] + app.cardWidth, 
        app.tableCardPositions[i][1] + app.cardHeight, fill=color, width=2)

def drawPlayerHand(app, canvas):
    # cardPos.append(((app.playerHandXCor - (handLength*(app.cardWidth + margin)-margin)//2 + i*margin),
    # finds top left corner of hand and draws each card from there rightward
    if not (app.isStartGame or app.isCombinationsBanner):
        length = len(app.playerHand)
        margin = 10
        startPosXCor = app.playerHandXCor - (length*(app.cardWidth + margin)-margin)//2
        startPosYCor = app.playerHandYCor - app.cardHeight/2
        for i in range(length):
            color = app.playerHand[i]
            canvas.create_rectangle(startPosXCor + (margin + app.cardWidth)*i, startPosYCor, 
            startPosXCor + (margin + app.cardWidth)*i + app.cardWidth, startPosYCor + app.cardHeight,
            fill=color)

def drawMeld(app, canvas, index, startPosX, player):
    # draws a meld given it's index in the meld list and start position
    if player == 'ai':
        length = len(app.aiMelds[index])
    else:
        length = len(app.playerMelds[index])
    startPosX += index*app.width//7
    startPosY = app.height*3//4 - app.cardHeight//2
    if player == 'ai':
        startPosY -= app.height//2
    margin = 10
    for i in range(length):
        if player == 'ai':
            color = app.aiMelds[index][i]
        else:
            color = app.playerMelds[index][i]
        canvas.create_rectangle(startPosX + margin*i - (app.cardWidth + margin*(length-1))//2,
        startPosY, startPosX + margin*i + app.cardWidth//2 - margin*(length-1)//2,
        startPosY + app.cardHeight, fill=color)

def drawPlayerMelds(app, canvas):
    # draws the melds of the user from left to right
    length = len(app.playerMelds)
    startPosX = app.width//2 - ((length-1)*app.width//14)
    for i in range(length):
        drawMeld(app, canvas, i, startPosX, 'user')

def drawAIHand(app, canvas):
    # draws 3 brown (face-down) cards
    if not (app.isStartGame or app.isCombinationsBanner):
        length = len(app.aiHand)
        margin = 10
        startPosXCor = app.aiHandXCor - (length*(app.cardWidth + margin)-margin)//2
        startPosYCor = app.aiHandYCor - app.cardHeight/2
        for i in range(length):
            color = app.aiHand[i]
            canvas.create_rectangle(startPosXCor + (margin + app.cardWidth)*i, startPosYCor, 
            startPosXCor + (margin + app.cardWidth)*i + app.cardWidth, startPosYCor + app.cardHeight,
            fill=color)

def drawAIMelds(app, canvas):
    # draws the melds of the user from left to right
    length = len(app.aiMelds)
    startPosX = app.width//2 - ((length-1)*app.width//14)
    for i in range(length):
        drawMeld(app, canvas, i, startPosX, 'ai')

def drawDeck(app, canvas):
    # draws 52 cards slightly skewed to the right so it looks 3-D
    length = len(app.deck)
    margin = 0.2
    startPosXCor = app.deckXCor - (length*margin)/2 - app.cardWidth/2
    startPosYCor = app.deckYCor - app.cardHeight/2
    for i in range(length):
        canvas.create_rectangle(startPosXCor + int(margin*i), startPosYCor, 
        startPosXCor + int(margin*i) + app.cardWidth, startPosYCor + app.cardHeight,
        fill='brown')

def drawCombination(app, canvas, row, col, index, bigMargin):
    # draws each combination on the sign spaced apart evenly
    length = len(app.combos)
    combo = app.combos[index]
    comboXCor = app.width//2 + bigMargin*(col - 1)
    comboYCor = app.height//2 + (bigMargin//2)*(row - 1)
    littleMargin = 10
    startPosXCor = comboXCor - (length*littleMargin)/2 - app.cardWidth/2
    startPosYCor = comboYCor - app.cardHeight/2
    for i in range(len(combo)):
        color = combo[i]
        canvas.create_rectangle(startPosXCor + littleMargin*i, startPosYCor, 
        startPosXCor + littleMargin*i + app.cardWidth, startPosYCor + app.cardHeight,
        fill=color)

def drawDifficultyBanner(app, canvas):
    # draws starting banner at the game start
    if app.isStartGame:
        canvas.create_rectangle(app.width//8, app.height//8, app.width*7//8,
        app.height*7//8, fill='tan')
        if not app.choseDifficultyLevel:
            canvas.create_text(app.width//2, app.height//4, text='Choose A Difficulty Level',
            font='Arial 24')

def drawCombinationsBanner(app, canvas):
    if app.isMemorizeCombos:
        bannerText = 'Memorize These Kombos!'
    else:
        bannerText = 'Here are the Kombos!'
    # draws the sign that shows all legal combinations before game
    if app.isCombinationsBanner and (not app.isStartGame):
        canvas.create_rectangle(app.width//8, app.height//8, app.width*7//8,
        app.height*7//8, fill='tan')
        canvas.create_text(app.width//2, app.height//4, text=bannerText,
        font='Arial 24')
        margin = app.height//4
        for r in range(2):
            for c in range(3):
                index = c + r*3
                drawCombination(app, canvas, r, c, index, margin)

        canvas.create_rectangle(app.width//2 - app.width//10, app.height*3//4 - app.height//20,
        app.width//2 + app.width//10, app.height*3//4 + app.height//20, fill='lime')
        canvas.create_text(app.width//2, app.height*3//4, text='Got It!')

def drawEndRoundBanner(app, canvas):
    # draws the scores of each player along with the total scores
    if app.isEndRound:
        canvas.create_rectangle(app.width//8, app.height//8, app.width*7//8,
        app.height*7//8, fill='tan')
        canvas.create_text(app.width//2, app.height//5, 
        text='# Of Total Cards x # Of Total Kombos = Total Score', font='Arial 18')
        canvas.create_text(app.width//2, app.height*3//10, 
        text=f'You:     {app.playerNumOfCards} cards x {app.playerNumOfCombos} kombos = \
        {app.userRoundScore}', font='Arial 16')
        canvas.create_text(app.width//2, app.height*2//5, 
        text=f'CPU:     {app.aiNumOfCards} cards x {app.aiNumOfCombos} kombos = \
        {app.aiRoundScore}', font='Arial 16')
        canvas.create_text(app.width//2, app.height//2, 
        text='Total Score:', font='Arial 18')
        canvas.create_text(app.width//2, app.height*3//5, 
        text=f'You:     {app.userTotalScore}        CPU:    {app.aiTotalScore}', font='Arial 18')

def drawEndGameBanner(app, canvas):
    # same thing as above but indicates which player won with a message
    margin = 20
    canvas.create_rectangle(app.width//8, app.height//8, app.width*7//8,
    app.height*7//8, fill='tan')
    canvas.create_text(app.width//2, app.height//5, text='Final Score:', font='Arial 24')
    canvas.create_text(app.width//2, app.height//3, text='You:', font='Arial 20')
    canvas.create_text(app.width//2, app.height//3 + margin, text=app.userTotalScore, font='Arial 20')
    canvas.create_text(app.width//2, app.height//2, text='CPU:', font='Arial 20')
    canvas.create_text(app.width//2, app.height//2 + margin, text=app.aiTotalScore, font='Arial 20')
    if app.userTotalScore > app.aiTotalScore:
        finalMessage = 'Congrats! You Won!'
    elif app.userTotalScore < app.aiTotalScore:
        finalMessage = 'CPU Won. Better Luck Next Time.'
    else:
        finalMessage = 'Game Tied!'
    canvas.create_text(app.width//2, app.height*5//8, text=finalMessage, font='Arial 20')

def drawRulesBanner(app, canvas):
    # draws the rules of the game
    if app.isRulesBanner:
        canvas.create_rectangle(app.width//8, app.height//8, app.width*7//8,
        app.height*7//8, fill='tan')
        canvas.create_text(app.width//2, 110, text='Rules', font='Arial 20')
        canvas.create_text(app.width//2, app.height//2 + 30, text= '   \n \
    1) User faces off against an AI of ranging difficulty.  Goal is to get the \n \
    most combinations of cards at the end.  Points are calculated by (number of \n \
    combinations) x (number of total cards). \n \
    \n \
    2) Each game starts with options allowing the user to choose the AI difficulty \n \
    level and if he/she wants to play without memorizing the combos. \n \
    \n \
    3) Before play starts, a list of 6 randomly generated card combinations of 2-6 \n \
    lengths are presented to the user.  User must try to memorize all the \n \
    combinations before time limit. \n \
    \n \
    4) Game setup: There exists a deck of 52 or so cards.  13 are red, 13 are \n \
    yellow, 13 are blue, and 13 are green.  9 cards are dealt on the "table".  Also, \n \
    players are dealt 3 cards as a "hand". \n \
    \n \
    5) Players take turns making legal combinations out of the cards on the table \n \
    and in "hand".  After each turn, board replaces taken cards but leaves 1 less. \n \
    \n \
    6) Key strategy in this game is to memorize the legal combinations before game \n \
    starts.  User must form combinations from memory.  Can get an assist by \n \
    reviewing the legal combinations mid-game, but some sort of point penalty will \n \
    be enforced. \n \
    \n \
    7) If user forms an illegal combo, user passes and turn is skipped. \n \
    \n \
    8) If player takes all cards on table, player goes again. \n \
    \n \
    9) Game ends when everyone passes in one round. \n \
    \n \
    10) Multiple games are played before total points are counted and winner is \n \
    declared.', font='Arial 7')

# this section deals with all the buttons and texts in the game

def drawResetButton(app, canvas):
    xCor = app.width - 70
    yCor = 60
    if not (app.isStartGame or app.isCombinationsBanner):
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='navy')
        canvas.create_text(xCor, yCor, text='Reset', fill='white', font='Arial 18')

def drawEasyButton(app, canvas):
    xCor = app.width//2
    yCor = 200
    if app.isStartGame and (not app.choseDifficultyLevel):
        canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='lime')
        canvas.create_text(xCor, yCor, text='Easy', font='Arial 24')

def drawMediumButton(app, canvas):
    xCor = app.width//2
    yCor = 300
    if app.isStartGame and (not app.choseDifficultyLevel):
        canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='yellow')
        canvas.create_text(xCor, yCor, text='Medium', font='Arial 24')

def drawHardButton(app, canvas):
    xCor = app.width//2
    yCor = 400
    if app.isStartGame and (not app.choseDifficultyLevel):
        canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='red')
        canvas.create_text(xCor, yCor, text='Hard', font='Arial 24')

def drawEndTurnButton(app, canvas):
    xCor = 220
    yCor = 340
    if app.isUserTurn:
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='lime')
        canvas.create_text(xCor, yCor, text='Done')

def drawRedoTurnButton(app, canvas):
    xCor = 220
    yCor = 260
    if app.isUserTurn:
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='olive')
        canvas.create_text(xCor, yCor, text='Start Over')

def drawGetCombinationsBanner(app, canvas):
    xCor = 120
    yCor = 260
    if app.isUserTurn and (not app.isMemorizeCombos):
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='magenta')
        canvas.create_text(xCor, yCor, text='Kombos')

def drawPassButton(app, canvas):
    xCor = 120
    yCor = 340
    if app.isUserTurn:
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='orange')
        canvas.create_text(xCor, yCor, text='Pass')

def drawRulesButton(app, canvas):
    xCor = 70
    yCor = app.height - 60
    if app.isUserTurn:
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='orange')
        canvas.create_text(xCor, yCor, text='Rules')

def drawGameText(app, canvas):
    if not(app.isEndRound or app.isCombinationsBanner or app.isRulesBanner):
        xCor = app.width//2
        yCor = 30
        canvas.create_text(xCor, yCor, text=app.gameText, font='Arial 20')

def drawRoundDisplayText(app, canvas):
    xCor = 80
    yCor = 40
    if not app.isStartGame:
        canvas.create_text(xCor, yCor, text=f'Round {app.round}', font='Arial 24')
    
def drawEndRulesButton(app, canvas):
    xCor = app.width*7//8 - 60
    yCor = app.height//8 + 50
    if app.isRulesBanner:
        canvas.create_rectangle(xCor - 40, yCor - 30, xCor + 40, yCor + 30, fill='Salmon')
        canvas.create_text(xCor, yCor, text='Back To Game')

def drawNextRoundButton(app, canvas):
    xCor = app.width//2
    yCor = app.height*4//5
    if app.isEndRound:
        canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='dark green')
        canvas.create_text(xCor, yCor, text='Next Round', font='Arial 20', fill='white')

def drawNewGameButton(app, canvas):
    xCor = app.width//2
    yCor = app.height*3//4
    canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='dark green')
    canvas.create_text(xCor, yCor, text='Play Again', font='Arial 20', fill='white')

def drawYesButton(app, canvas):
    xCor = app.width//2
    yCor = app.height//2
    if app.isStartGame and app.choseDifficultyLevel:
        xCor = app.width//2
        yCor = app.height//2
        canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='lime')
        canvas.create_text(xCor, yCor, text='Yes', font='Arial 20')

def drawNoButton(app, canvas):
    xCor = app.width//2
    yCor = app.height*2//3
    if app.isStartGame and app.choseDifficultyLevel:
        canvas.create_rectangle(xCor - 80, yCor - 30, xCor + 80, yCor + 30, fill='red')
        canvas.create_text(xCor, yCor, text='No', font='Arial 20')

def drawMemorizeCombosText(app, canvas):
    xCor = app.width//2
    yCor = app.height//4
    if app.isStartGame and app.choseDifficultyLevel:
        canvas.create_text(xCor, yCor, text='Will you memorize the combos before each round?',
        font='Arial 18')

def redrawAll(app, canvas):
    # draws all animations
    if app.isEndGame:
        drawEndGameBanner(app, canvas)
        drawNewGame(app, canvas)
    else:
        canvas.create_rectangle(0, 0, app.width, app.height, fill='light gray')
        drawTableCards(app, canvas)
        drawPlayerHand(app, canvas)
        drawPlayerMelds(app, canvas)
        drawAIHand(app, canvas)
        drawAIMelds(app, canvas)
        drawDeck(app, canvas)
        drawCombinationsBanner(app, canvas)
        drawEndTurnButton(app, canvas)
        drawRedoTurnButton(app, canvas)
        drawPassButton(app, canvas)
        drawGetCombinationsBanner(app, canvas)
        drawGameText(app, canvas)
        drawRoundDisplayText(app, canvas)
        drawRulesButton(app, canvas)
        drawEndRoundBanner(app, canvas)
        drawResetButton(app, canvas)
        drawRulesBanner(app, canvas)
        drawEndRulesButton(app, canvas)
        drawDifficultyBanner(app, canvas)
        drawEasyButton(app, canvas)
        drawMediumButton(app, canvas)
        drawHardButton(app, canvas)
        drawNextRoundButton(app, canvas)
        drawYesButton(app, canvas)
        drawNoButton(app, canvas)
        drawMemorizeCombosText(app, canvas)

runApp(width=800, height=600)