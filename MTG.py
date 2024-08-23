import tkinter.filedialog
import csv

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
    print(deck.split('\n'))


main()
