import random
import tkinter.filedialog

import pygame
import requests


def pick_file():
    return tkinter.filedialog.askopenfilename(
        title="Select Your Deck", filetypes=[("Text files", "*.txt")]
    )


def read_deck(filename):
    f = open(filename, "r")
    deck = f.read()
    f.close()
    return deck


def import_deck():
    return read_deck(pick_file())


def parse_deck(deck):
    deck = deck.split("\n")
    deck = list(filter(None, deck))
    new_deck = []
    for card in deck:
        card_properties = card.split()
        quantity = int(card_properties[0])
        card_name = " ".join(card_properties[1:])
        new_deck.extend([card_name] * quantity)
    return new_deck


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


def get_card_from_api(card_name):
    response = requests.get(f"https://api.scryfall.com/cards/search?q={card_name}")
    data = response.json()
    return data["data"][0]


cache = {}


def get_card_info(card_name):
    if card_name in cache:
        return cache[card_name]
    else:
        data = get_card_from_api(card_name)
        cache[card_name] = data
        return data


def get_card_part(card_name, part):
    return get_card_info(card_name)[part]


def main():
    pygame.init()

    info_object = pygame.display.Info()
    screen = pygame.display.set_mode((info_object.current_w, info_object.current_h))
    pygame.display.set_caption("MTGSim")

    deck = import_deck()
    deck = parse_deck(deck)
    deck = shuffle(deck)
    deck, hand = draw7(deck)
    print(hand)
    print(get_card_part(hand[0], "name"))

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
