import logging

from memory_puzzle import eventmanager
from memory_puzzle import model
from memory_puzzle import view
from memory_puzzle import controller

def set_up_logging():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def main():
    set_up_logging()

    event_manager = eventmanager.EventManager()
    game_model = model.Model(event_manager)
    keyboard = controller.Controller(event_manager, game_model)
    graphics = view.GraphicalView(event_manager, game_model)
    game_model.run()

if __name__ == '__main__':
    main()