import sys
from game import Game
from tool_registry import register_game_tools
def display_callback(message, message_type="info"):
    if message_type == "info":
        print(f"[CYBERPUNK INFO] {message}")
    elif message_type == "dice":
        print(f"[DICE ROLLED] {message}")
def main():
    game = Game(display_callback=display_callback)
    register_game_tools(game.tools, game.state)
        theme = "Cyberpunk"
    print(f"Starting a {theme} themed adventure...")
    game.start_game(theme)
    while True:
        try:
            command = input("Enter command (type 'exit' to quit): ").strip()
            if command.lower() == 'exit':
                print("Exiting game...")
                break
            response, room_info, inventory_info = game.process_command(command)
            if response:
                print(f"Game Response: {response}")
            if room_info:
                print(f"Current Room Info: {room_info}")
            if inventory_info:
                print(f"Inventory: {inventory_info}")
        except Exception as e:
            print(f"Error processing command: {e}")

if __name__ == "__main__":
    main()