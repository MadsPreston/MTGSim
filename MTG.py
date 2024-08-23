import random
import tkinter.filedialog

import pygame
import requests


def openfile():
    filename = tkinter.filedialog.askopenfile(mode="r")
    return filename.name


def readDeck(fileName):
    f = open(fileName, "r")
    deck = f.read()
    f.close()
    return deck


def importDeck():
    return readDeck(openfile())


def parseDeck(deck):
    deck = deck.split("\n")
    deck = list(filter(None, deck))
    newDeck = []
    for card in deck:
        cardProperties = card.split()
        quantity = int(cardProperties[0])
        cardName = " ".join(cardProperties[1:])
        newDeck.extend([cardName] * quantity)
    return newDeck


def shuffle(deck):
    random.shuffle(deck)
    return deck


def draw7(deck):
    i = 0
    hand = []
    while i < 7:
        card = deck[0]
        hand.append(card)
        deck.remove(card)
        i += 1
    return deck, hand


def getCardFromApi(cardName):
    response = requests.get(f"https://api.scryfall.com/cards/search?q={cardName}")
    data = response.json()
    return data["data"][0]


cache = {}


def getCardInfo(cardName):
    if cardName in cache:
        return cache[cardName]
    else:
        data = getCardFromApi(cardName)
        cache[cardName] = data
        return data


def getCardPiece(cardName, piece):
    return getCardInfo(cardName)[piece]


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("MTGSim")

    deck = importDeck()
    deck = parseDeck(deck)
    deck = shuffle(deck)
    deck, hand = draw7(deck)
    print(hand)
    print(getCardPiece(hand[0], "name"))

    images = []
    cards = []
    image1 = pygame.image.load("C:/Users/maddy/Downloads/Black Lotus.jpg").convert()
    card1 = image1.get_rect()

    images.append(image1)
    cards.append(card1)

    active_box = None

    while True:
        screen.fill("blue")

        pygame.draw.rect(screen, "purple", card1)
        screen.blit(image1, card1)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for (
                        num,
                        box,
                    ) in enumerate(cards):
                        if box.collidepoint(event.pos):
                            active_box = num
            if event.type == pygame.MOUSEMOTION:
                if active_box != None:
                    cards[active_box].move_ip(event.rel)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_box = None

        pygame.display.flip()


main()
