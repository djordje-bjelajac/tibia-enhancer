from abc import ABC, abstractmethod


class GameClient(ABC):
    @abstractmethod
    def locate_window(self, window_title):
        pass

    @abstractmethod
    def capture_window_portion(self, region):
        pass

    @abstractmethod
    def save_cgimage_to_file(self, cgimage, file_name):
        pass

    @abstractmethod
    def average_color(self, cgiimage):
        pass

    @abstractmethod
    def send_key_to_app(self, app_name, key_code):
        pass
