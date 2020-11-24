from Picture import Picture


def main():
    easy_dices = ['./images/easy/dice6.jpg', './images/medium/dice12.jpg']
    pictures = []
    for dice in easy_dices:
        pictures.append(Picture(dice))

    pictures[0].process_picture()


if __name__ == "__main__":
    main()
