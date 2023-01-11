import os
import random
import shutil
import json
import datetime
import time
from PIL import Image, ImageFont, ImageDraw

def check_dir(path):
    ans = []
    for file in os.listdir(path):
        ans.append(path+"/"+file)

    return ans


def pokemon_it(card, capy, ability1, ability2, weakness):
    font = ImageFont.truetype("Symbola.ttf", 20)
    img = Image.open(card)
    img2 = Image.open(capy)
    draw = ImageDraw.Draw(img)

    img2 = img2.resize((347, 230))
    img.paste(img2, (37, 61))
    draw.text((110, 25), capy[18:][:len(capy[18:]) - 4], (0, 0, 0), font=font)
    draw.text((40, 350), split_line(ability1), (0, 0, 0), font=font)
    draw.text((40, 410), split_line(ability2), (0, 0, 0), font=font)
    draw.text((30, 520), weakness, (0, 0, 0), font=ImageFont.truetype("Symbola.ttf", 11))
    draw.text((120, 520), "everything", (0, 0, 0), font=ImageFont.truetype("Symbola.ttf", 12))
    img.save("Pokemon_card.png", "PNG")

    os.remove("imgs/Pokemon_card.png")
    shutil.move("Pokemon_card.png", "imgs/")


def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)


def split_line(line):
    chars = 0
    chars_list = []
    int_list = []
    ans_int = 0
    for word in line.split(" "):
        chars += len(word) + 1
        chars_list.append(chars)

    for i in chars_list:
        if (30 - i) < 0:
            int_list.append((30 - i)*-1)
        else:
            int_list.append(30 - i)

    if str(type(min(int_list))) == "<class 'list'>":
        ans_int = min(int_list)[0] + 30
    elif str(type(min(int_list))) != "<class 'list'>":
        ans_int = min(int_list) + 30

    return line[:ans_int] + "\n" + line[ans_int:]


with open("data.json", "r") as f:
    data = json.load(f)

while True:
    load_data()
    cards = check_dir("imgs/cards")
    abilities = data["data"][1]["abilities"]
    weaknesses = data["data"][2]["weakness"]
    capies = check_dir("imgs/capybaras")
    capy_number = data["data"][3]["capy_number"]

    if data["data"][0]["day"] != datetime.datetime.now().day:
        capy_number += 1
        data["data"] = [{"day": datetime.datetime.now().day + 1}, {"abilities": data["data"][1]["abilities"]}, {"weakness": data["data"][2]["weakness"]}, {"capy_number": capy_number}]
        print("Capybara changed "+str(capy_number))

        with open("data.json", "w") as f:
            json.dump(data, f)

        pokemon_it(
            random.choice(cards),
            random.choice(capies),
            random.choice(abilities),
            random.choice(abilities),
            random.choice(weaknesses)
        )