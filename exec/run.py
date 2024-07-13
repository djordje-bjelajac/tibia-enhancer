from pkg.action_manager.action_manager import ActionManager
from pkg.game_client.quartz.quartz_game_client import QuartzGameClient
import time

game_title = 'Tibia - Marcus Aphi'
# x, y, width, height of the region to capture
region_of_interest = (12, 33, 850, 12)
monitor_frequency = 0.1  # Seconds between checks (adjust as needed)


def main():
    client = QuartzGameClient(game_title)
    action_manager = ActionManager(client)
    while True:
        action_manager.execute_action()
        time.sleep(monitor_frequency)


main()
