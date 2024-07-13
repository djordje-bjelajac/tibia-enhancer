from pkg.game_client.game_client import GameClient
import math
import numpy as np

average_color_target = np.array(
    [122.61803922, 122.23539216, 122.49519608]).sum()


def round_down(number):
    factor = 1000
    return math.floor(number * factor) / factor


class ActionManager:
    def __init__(self, client: GameClient):
        self.client = client

    def check_triggers(self):
        pass

    def execute_action(self):
        region_of_interest = (12, 33, 850, 12)
        self.client.locate_window()
        cgimage = self.client.capture_window_portion((region_of_interest))

        if round_down(self.client.average_color(cgimage).sum()) == round_down(average_color_target):
            print("Target color detected.")

        self.client.send_key_to_app('Tibia', 103)
