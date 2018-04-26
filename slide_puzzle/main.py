from slide_puzzle import eventmanager
from slide_puzzle import model
from slide_puzzle import view
from slide_puzzle import controller

def main():
    event_manager = eventmanager.EventManager()
    game_model = model.Model(event_manager)
    keyboard = controller.Controller(event_manager, game_model)
    graphics = view.GraphicalView(event_manager, game_model)
    game_model.run()

if __name__ == '__main__':
    main()