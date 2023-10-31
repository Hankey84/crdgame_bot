## Refactoring and modificated by ChatGPT
import os
from PIL import Image, ImageDraw, ImageFont

# Function to generate a card image
def generate_card_image(suit, rank):
    width, height = 80, 110
    image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Arial.ttf", size=20)

    # Define the symbols and colors for each suit
    suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
    suit_colors = {"Hearts": "red", "Diamonds": "red", "Clubs": "black", "Spades": "black"}

    # Draw the suit symbol and rank
    draw.text((10, 20), suit_symbols[suit], fill=suit_colors[suit], font=font)
    draw.text((10, 50), rank, fill=suit_colors[suit], font=font, align='center')

    return image

# Lists of suits and ranks
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

# Check and create the directory for image storage
dir_path = "cards"

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

# Generate and save images for all combinations
for suit in suits:
    for rank in ranks:
        image = generate_card_image(suit, rank)
        image.save(os.path.join(dir_path, f"{suit}_{rank}.png"))

print("Images generated and saved.")
