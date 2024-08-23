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

def main():
    deck = importDeck()
    deck = deck.split('\n')
    deck = list(filter(None, deck))
    newDeck = []
    for card in deck:
        cardProperties = card.split()
        quantity = cardProperties[0]
        cardName = ' '.join(cardProperties[1:])
        card = [quantity, cardName]
        newDeck.append(card)
    deck = newDeck
    print(deck)




main()
