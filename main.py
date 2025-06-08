import agents
import agents.print_game_agent
import keyboard

def main():
    while True:
        agents.print_game_agent.graph.invoke({})
        print("Executado")

keyboard.add_hotkey("alt+j", main)
keyboard.wait("ctrl+b")