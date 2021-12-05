#!/usr/bin/python3
import data.engine as e
WINDOW_SIZE = (1050, 700)
high_score = 0


def main():
    game = e.game(WINDOW_SIZE, high_score)
    game.update_score()
    game.menu()


if __name__ == '__main__':
    main()
