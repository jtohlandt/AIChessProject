from my_chess.game import game
def main():
    current_game = game()
    print("Game started")
    current_game.set_mode()
    print("Game mode set")
    current_game.run()
    print("Game over")
if __name__ == "__main__":
    main()