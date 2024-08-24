import random
import tkinter.filedialog
from io import BytesIO

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


def drawX(deck, num):
    i = 0
    hand = []
    while i < num:
        card = deck[0]
        hand.append(card)
        deck.remove(card)
        i += 1
    return deck, hand


def get_card_from_api(card_name):
    card_name = card_name.replace(" ", "+")
    response = requests.get(f"https://api.scryfall.com/cards/named/?exact={card_name}")
    data = response.json()
    return data


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


def get_card_image(card_name, size):
    card_url = get_card_info(card_name)["image_uris"][size]
    return requests.get(card_url)


def add_card(image, cards):
    cards.append({"image": image, "rect": image.get_rect(), "rotated": False})


def render_card(card, cards):
    image = pygame.image.load(
        (BytesIO(get_card_image(card, "small").content))
    ).convert()
    add_card(image, cards)


def main():
    pygame.init()

    info_object = pygame.display.Info()
    screen = pygame.display.set_mode((info_object.current_w, info_object.current_h))
    pygame.display.set_caption("MTGSim")

    deck = import_deck()
    deck = parse_deck(deck)
    deck = shuffle(deck)
    deck, hand = drawX(deck, 7)

    cards = []

    add_card(pygame.image.load("CardBack.jpg").convert(), cards)

    for card in hand:
        render_card(card, cards)

    active_box = None

    while True:
        screen.fill("blue")

        for card in cards:
            pygame.draw.rect(screen, "purple", card["rect"])
            screen.blit(card["image"], card["rect"])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click and drag cards
                if event.button == 1:
                    for (
                        num,
                        card,
                    ) in enumerate(cards):
                        if card["rect"].collidepoint(event.pos):
                            active_box = num
                # Turn cards on middle-click
                if event.button == 2:
                    for num, card in enumerate(cards):
                        if card["rect"].collidepoint(event.pos):
                            if num == 0:
                                # Do not turn library card
                                continue
                            if card["rotated"]:
                                card["image"] = pygame.transform.rotate(
                                    card["image"], 90
                                )
                                card["rotated"] = False
                            else:
                                card["image"] = pygame.transform.rotate(
                                    card["image"], -90
                                )
                                card["rotated"] = True
                            # Update bounding box
                            card["rect"] = card["image"].get_rect(
                                center=card["rect"].center
                            )

                # Draw cards when right-clicking on deck
                if event.button == 3:
                    deck, hand = drawX(deck, 1)
                    card = hand[len(hand) - 1]
                    render_card(card, cards)

            if event.type == pygame.MOUSEMOTION:
                if active_box is not None:
                    cards[active_box]["rect"].move_ip(event.rel)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_box = None

        pygame.display.flip()


main()
