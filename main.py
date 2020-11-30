from Picture import Picture
from result import result


def main():
    easy_dices = ['./images/easy/dice1.jpg', './images/easy/dice2.jpg', './images/easy/dice3.jpg',
                  './images/easy/dice4.jpg', './images/easy/dice5.jpg', './images/easy/dice6.jpg',
                  './images/easy/dice7.jpg', './images/easy/dice8.jpg', './images/easy/dice9.jpg',
                  './images/easy/dice10.jpg']
    medium_dices = ['./images/medium/dice1.jpg', './images/medium/dice2.jpg', './images/medium/dice3.jpg',
                    './images/medium/dice4.jpg', './images/medium/dice5.jpg', './images/medium/dice6.jpg',
                    './images/medium/dice7.jpg', './images/medium/dice8.jpg', './images/medium/dice9.jpg',
                    './images/medium/dice10.jpg']
    hard_dices = ['./images/hard/dice1.jpg', './images/hard/dice2.jpg', './images/hard/dice3.jpg',
                  './images/hard/dice4.jpg', './images/hard/dice5.jpg', './images/hard/dice6.jpg',
                  './images/hard/dice7.jpg', './images/hard/dice8.jpg', './images/hard/dice9.jpg',
                  './images/hard/dice10.jpg']
    pictures = []
    for easy_dice, medium_dice, hard_dice in zip(easy_dices, medium_dices, hard_dices):
        pictures.append(Picture(easy_dice))
        pictures.append(Picture(medium_dice))
        pictures.append(Picture(hard_dice))

    for picture in pictures:
        picture.process_picture()
        result(result)


if __name__ == "__main__":
    main()
