import tkinter.filedialog

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
    return "Unfinished"

def main():
    deck = importDeck()
    deck = parseDeck(deck)
    draw7(deck)

    print(deck)




main()
