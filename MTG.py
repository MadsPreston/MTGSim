import tkinter.filedialog
import random

def openfile():
    filename = tkinter.filedialog.askopenfile(mode='r')
    return filename.name

def readDeck(fileName):
    f = open(fileName, "r")
    deck = f.read()
    f.close()
    return deck

def importDeck():
    return readDeck(openfile())

def parseDeck(deck):
    deck = deck.split('\n')
    deck = list(filter(None, deck))
    newDeck = []
    for card in deck:
        cardProperties = card.split()
        quantity = int(cardProperties[0])
        cardName = ' '.join(cardProperties[1:])
        newDeck.extend([cardName] * quantity)
    return newDeck

def draw7(deck):
    i = 0
    hand = []
    while i < 7:
        card = random.choice(deck)
        hand.append(card)
        deck.remove(card)
        i += 1
    return deck, hand



def main():
    deck = importDeck()
    deck = parseDeck(deck)
    print(len(deck))
    deck, hand = draw7(deck)
    print(hand, len(deck), deck)




main()
