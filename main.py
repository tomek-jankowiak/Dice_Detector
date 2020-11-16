from Picture import Picture


def main():
    easy_dices = ['./images/easy/dice1.png', './images/easy/dice2.jpg']
    pictures = []
    for dice in easy_dices:
        pictures.append(Picture(dice))

    pictures[0].process_picture()


if __name__ == "__main__":
    main()
