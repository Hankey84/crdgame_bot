import os
from PIL import Image, ImageDraw, ImageFont


def generate_card_image(suit, rank):
    # Создаем новое изображение
    width, height = 80, 110
    image = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    # Создаем объект ImageDraw для рисования
    draw = ImageDraw.Draw(image)

    # Задаем шрифт и размер текста
    font = ImageFont.truetype("Arial.ttf", size=20)

    # Рисуем масть
    if suit == "Hearts":
        draw.text((10, 20), "♥", fill="red", font=font)
        draw.text((10, 50), rank, fill="red", font=font, align='center')
    elif suit == "Diamonds":
        draw.text((10, 20), "♦", fill="red", font=font)
        draw.text((10, 50), rank, fill="red", font=font, align='center')
    elif suit == "Clubs":
        draw.text((10, 20), "♣", fill="black", font=font)
        draw.text((10, 50), rank, fill="black", font=font, align='center')
    elif suit == "Spades":
        draw.text((10, 20), "♠", fill="black", font=font)
        draw.text((10, 50), rank, fill="black", font=font, align='center')

    # Рисуем ранг
    #draw.text((10, 50), rank, fill="black", font=font, align='center')

    return image


# Списки мастей и рангов
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jacket", "Queen", "King", "Ace"]

# Проверка и создание директории для хранения картинок
dir_path = "cards"

if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
    # Генерация и сохранение изображений для всех комбинаций
    for suit in suits:
        for rank in ranks:
            image = generate_card_image(suit, rank)
            image.save(f"{dir_path}/{suit}_{rank}.png")
else:
    print("The directory is present.")

#xx = input('Press AnyKey..')
