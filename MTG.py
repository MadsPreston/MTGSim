import random
import time
import tkinter.filedialog
from io import BytesIO

import pygame
import requests


def pick_file():
    """Opens a file dialog for text files and returns the path"""
    path = tkinter.filedialog.askopenfilename(
        title="Select Your Deck", filetypes=[("Text files", "*.txt")]
    )
    if not path:
        raise ValueError("No file selected.")

    return path


def read_deck(filename):
    """Reads the content of a text file and returns it as a string."""
    f = open(filename, "r")
    deck = f.read()
    f.close()
    return deck


def import_deck():
    """Opens a file dialog to select a text file, reads its content, and returns it as a string."""
    return read_deck(pick_file())


def parse_deck(deck):
    """
    Parses a deck string into a list of card names based on quantities.

    Args:
        deck (str): String of card names, one on each line with quantity preceding.

    Returns:
        List with each card name repeated according to its quantity.

    Raises:
        ValueError: If card quantity is negative or deck is incorrectly formatted.
    """
    try:
        deck = deck.split("\n")
        deck = list(filter(None, deck))
        new_deck = []
        for card in deck:
            card_properties = card.split()
            quantity = int(card_properties[0])
            card_name = " ".join(card_properties[1:])
            if quantity <= 0:
                raise ValueError("Card quantity must be positive.")
            new_deck.extend([card_name] * quantity)
    except (ValueError, IndexError):
        raise ValueError(
            "Invalid deck format. Please ensure each line has a positive integer followed by a card name."
        )
    return new_deck


def shuffle(deck):
    """Randomly shuffles the deck (a list of card names) and returns the shuffled deck."""
    random.shuffle(deck)
    return deck


def drawX(deck, num):
    """
    Draws a specified number of cards from the deck and returns the updated deck and the drawn hand.

    Args:
        deck (list): The deck of cards.
        num (int): The number of cards to draw.

    Returns:
        tuple: The updated deck and a list of drawn cards.
    """
    i = 0
    hand = []
    while i < num:
        card = deck[0]
        hand.append(card)
        deck.remove(card)
        i += 1
    return deck, hand


def get_card_from_api(card_name):
    """
    Fetches card information from the Scryfall API based on the exact card name.

    Args:
        card_name (str): The name of the card to retrieve.

    Returns:
        dict: The card data returned by the Scryfall API.
    """
    card_name = card_name.replace(" ", "+")
    response = requests.get(f"https://api.scryfall.com/cards/named/?exact={card_name}")
    response.raise_for_status()
    return response.json()


cache = {}


def get_card_info(card_name):
    """
    Retrieves card information from cache or fetches it from the API if not cached.

    Args:
        card_name (str): The name of the card to retrieve.

    Returns:
        dict: The card data from the cache or the API.
    """
    if card_name in cache:
        return cache[card_name]
    else:
        data = get_card_from_api(card_name)
        cache[card_name] = data
        return data


def get_card_part(card_name, *parts):
    """
    Retrieves a specific part of card information from the cached data or API, supporting nested keys.

    Args:
        card_name (str): The name of the card.
        *parts: A sequence of keys to access nested dictionary values.

    Returns:
        The value at the specified path in the card information.
    """
    data = get_card_info(card_name)
    for part in parts:
        data = data.get(part)
        if data is None:
            break
    return data


def get_card_image(card_name, size):
    """
    Fetches the image of a card from the Scryfall API based on the card name and image size.

    Args:
        card_name (str): The name of the card.
        size (str): The size of the image ("small", "normal", "large", "png", "art_crop", "border_crop").

    Returns:
        The HTTP response object containing the image.
    """
    card_url = get_card_part(card_name, "image_uris", size)
    return requests.get(card_url)


def add_card(image, cards):
    """
    Adds a card dictionary to the list of cards.

    Args:
        image (Surface): The image of the card.
        cards (list): The list to which the card information will be added.
    """
    cards.append({"image": image, "rect": image.get_rect(), "rotated": False})


def fetch_and_add_card(card, cards):
    """
    Fetches a card image and adds a card dictionary to the list of cards.

    Args:
        card (str): The name of the card.
        cards (list): The list to which the card information will be added.
    """
    image = pygame.image.load(
        (BytesIO(get_card_image(card, "small").content))
    ).convert()
    add_card(image, cards)


def turn_card(card):
    """
    Rotates a card 90 degrees and updates its rect. Rotates counterclockwise if not already turned,
    counterclockwise if already turned.

    Args:
        card (dict): A dictionary representing the card, containing an 'image' surface
                     and a 'rotated' boolean flag indicating its current orientation.
    """
    if card["rotated"]:
        card["image"] = pygame.transform.rotate(card["image"], 90)
        card["rotated"] = False
    else:
        card["image"] = pygame.transform.rotate(card["image"], -90)
        card["rotated"] = True
    # Update bounding box
    card["rect"] = card["image"].get_rect(center=card["rect"].center)


def main():
    pygame.init()

    # Set up the display
    info_object = pygame.display.Info()
    screen = pygame.display.set_mode((info_object.current_w, info_object.current_h))
    pygame.display.set_caption("MTGSim")

    # Import, parse, shuffle the deck, and draw initial hand
    deck = import_deck()
    deck = parse_deck(deck)
    deck = shuffle(deck)
    deck, hand = drawX(deck, 7)

    # Initialize the list of cards that are on screen
    cards = []

    # Add the library image to the list of cards
    add_card(pygame.image.load("CardBack.jpg").convert(), cards)

    # Fetch images and add all cards in hand to cards list
    for card in hand:
        fetch_and_add_card(card, cards)

    # Keeping track of dragging
    active_box = None
    click_time = 1
    double_click = 0.5

    while True:
        # Background
        screen.fill("blue")

        # Draw each card on the screen
        for card in cards:
            pygame.draw.rect(screen, "purple", card["rect"])
            screen.blit(card["image"], card["rect"])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for num in reversed(
                        range(len(cards))
                    ):  # Reverse range to handle top-most card first
                        card = cards[num]
                        if card["rect"].collidepoint(event.pos):
                            if (
                                time.time() - click_time < double_click
                            ):  # if time between clicks is less than double_click time
                                if num == 0:
                                    # Do not turn library card
                                    continue
                                turn_card(card)
                                # Reset click time to prevent extra clicks
                                click_time = 1
                            else:
                                # Save click time to check if double-clicked
                                click_time = time.time()

                            # Set active_box for card dragging
                            active_box = num
                            break

                if event.button == 3:  # Right click
                    if cards[0]["rect"].collidepoint(event.pos):  # On deck
                        # Draw a card
                        deck, hand = drawX(deck, 1)
                        card = hand[len(hand) - 1]
                        fetch_and_add_card(card, cards)

            if event.type == pygame.MOUSEMOTION:
                if active_box is not None:
                    # Move the card being dragged
                    cards[active_box]["rect"].move_ip(event.rel)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Release card
                    active_box = None

        pygame.display.flip()


main()
