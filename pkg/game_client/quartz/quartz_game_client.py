from Cocoa import NSWorkspace
from Quartz import CGWindowListCopyWindowInfo
from Quartz import kCGNullWindowID
from Quartz import kCGWindowImageBoundsIgnoreFraming
from Quartz import kCGWindowImageNominalResolution
from Quartz import kCGWindowListOptionOnScreenOnly
from pkg.game_client.game_client import GameClient
import Quartz
import Quartz
import numpy as np
import time


class QuartzGameClient(GameClient):
    window = None

    def __init__(self, window_title):
        self.window_title = window_title

    def locate_window(self):
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in window_list:
            # TODO: Implement a more flexible window matching approach in the future
            if window.get('kCGWindowName') == self.window_title:
                self.window = window
                return window
        print(f"Window with title '{self.window_title}' not found.")
        return None

    def capture_window_portion(self, region):
        window_id = self.window['kCGWindowNumber']
        bounds = self.window['kCGWindowBounds']
        window_x, window_y = bounds['X'], bounds['Y']
        region_x, region_y, width, height = region
        rect = Quartz.CGRectMake(
            window_x + region_x, window_y + region_y, width, height)
        image = Quartz.CGWindowListCreateImage(rect, Quartz.kCGWindowListOptionIncludingWindow,
                                               window_id, kCGWindowImageBoundsIgnoreFraming | kCGWindowImageNominalResolution)
        return image

    def save_cgimage_to_file(self, cgimage, file_name):
        image_rep = Quartz.NSBitmapImageRep.alloc().initWithCGImage_(cgimage)
        image_data = image_rep.representationUsingType_properties_(
            Quartz.NSPNGFileType, None)
        image_data.writeToFile_atomically_(file_name, True)

    def average_color(self, image):
        # Get the image width and height
        width = Quartz.CGImageGetWidth(image)
        height = Quartz.CGImageGetHeight(image)

        # Get the image data provider
        data_provider = Quartz.CGImageGetDataProvider(image)

        # Get the raw data from the data provider
        data = Quartz.CGDataProviderCopyData(data_provider)
        raw_data = np.frombuffer(data, dtype=np.uint8)

        # Calculate the bytes per row (may include padding)
        bytes_per_row = Quartz.CGImageGetBytesPerRow(image)

        # Extract the RGB values (ignoring the alpha channel and any padding bytes)
        rgb_data = raw_data.reshape((height, bytes_per_row))[
            :, :width*4][:, :3*width]

        # Reshape to (height, width, 3)
        rgb_data = rgb_data.reshape((height, width, 3))

        # Calculate the average color for the R, G, and B channels
        avg_color = np.mean(rgb_data, axis=(0, 1))

        return avg_color

    def send_key_to_app(self, app_name, key_code):
        # Get the list of running applications
        apps = NSWorkspace.sharedWorkspace().runningApplications()

        # Find the target app
        target_app = None
        for app in apps:
            if app.localizedName() == app_name:
                target_app = app
                break

        if not target_app:
            print(f"Application '{app_name}' not found.")
            return

        pid = target_app.processIdentifier()
        print(f"Found application '{app_name}' with PID {pid}")

        # Create the event
        event = Quartz.CGEventCreateKeyboardEvent(None, key_code, True)

        # Set the target application
        Quartz.CGEventPostToPid(pid, event)
        time.sleep(0.1)  # Add a small delay

        # Release the key
        event = Quartz.CGEventCreateKeyboardEvent(None, key_code, False)
        Quartz.CGEventPostToPid(pid, event)

        print(f"Sent key code {key_code} to '{app_name}'")
