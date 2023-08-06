import numpy as np
from mss import mss
from PIL import Image
import cv2
import time


class Cannyfier():
    """
    This class reads a box (window) in the monitor in real time and process that part
    of the screen with Canny function from cv2. Shows the results in real time
    in a different window. The new window is having 2 sliders to adjust the min
    and max threshold of the canny function.

    There are 4 instance attributes (min and max threshold for canny)
    and 4 class attributes for the limits of the window captured (x, y)
    """

    min_tl = 10     # Canny min threshold start point
    min_tr = 300    # Canny min threshold end point
    max_tl = 10     # Canny max threshold start point
    max_tr = 300    # Canny max threshold end point

    def __init__(self, left=100, top=200, width=1380, height=900):
        """
        Creates an infinite loop to capture an screen region and cannyfy
        User has to press q to exit
        Args:
            x1      left x point of the scren
            y1      up y point of the screen
            x2      width of the screen box
            y2      height of the screen box
        Returns:
            Nothing
        """
        self.bbox = (left, top, width, height)
        self.capture = Capture(bbox=self.bbox, monitor=1)
        self.min = Cannyfier.min_tl
        self.max = Cannyfier.max_tl
        self.count_down(3)

        cv2.namedWindow('Cannifier')
        cv2.createTrackbar("Min Thres", "Cannifier", self.min_tl, self.min_tr, self.change_min)
        cv2.createTrackbar("Max Thres", "Cannifier", self.max_tl, self.max_tr, self.change_max)
        self.change_min(self.min_tl)
        self.change_max(self.max_tl)

        last_time = time.time()
        count = 0
        mean = 0

        while(True):
            self.process_img()
            count += 1
            mean = (mean * (count - 1) + (time.time() - last_time)) / count
            last_time = time.time()
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print(f"Screens per second: {1/mean}")
                print('Min: %5d - Max: %5d' % (self.min, self.max))
                break

    def count_down(self, t=3):
        """
        Executes a count down that is printed in the default output
        Args:
            t       timer in secs
        Returns:
            Nothing
        """
        for i in list(range(t))[::-1]:
            print(i+1)
            time.sleep(1)

    def process_img(self):
        """
        Grabs the image from the screen and cannyfies it. Returns the image
        Args:
            None
        Returns:
            cv2 Image
        """
        # scr = np.array(ImageGrab.grab(bbox=(self.x1, self.y1, self.x2, self.y2)))
        scr = np.array(self.capture.grab())
        p_img = cv2.Canny(scr, threshold1=self.min, threshold2=self.max)
        cv2.imshow('window', p_img)
        return p_img

    def change_min(self, val):
        """
        This function is a callback from the slider. Changes the current value
        of the min threshold
        Args:
            val:        the value of the sliders
        Returns:
            Nothing
        """
        self.min = val

    def change_max(self, val):
        """
        This function is a callback from the slider. Changes the current value
        of the max threshold
        Args:
            val:        the value of the sliders
        Returns:
            Nothing
        """
        self.max = val


def capture_mouse_drag_box(event, x, y, flags, para):
    """
    Captures init x and y for a click + drag and drop event. Basically it gets
    the box inside a click and drag and drop of the mouse.
    This will work only when ix = left and iy = top
    Args:
        None
    Returns:
        Nothing
    Side Effect:
        Changes the values of global variables
        __IX__
        __FX__
        __IY__
        __FY__
        __DRAWING__
    """
    global __IX__, __FX__, __IY__, __FY__, __DRAWING__

    if event == cv2.EVENT_LBUTTONDOWN:
        __DRAWING__ = True
        __IX__ = x
        __IY__ = y
        __FX__ = 0
        __FY__ = 0
    elif event == cv2.EVENT_MOUSEMOVE:
        if __DRAWING__:
            __FX__ = x
            __FY__ = y
    elif event == cv2.EVENT_LBUTTONUP:
        __DRAWING__ = False
        __FX__ = x
        __FY__ = y
        print(f"Drop Button: {__IX__}, {__IY__}, {__FX__}, {__FY__}")


def get_capture_coords():
    """
    Helps to define a region in the screen to be captured. You need to click
    and then drag and release the mouse to define such region.
    A transparent rectangle will be drawn on top of the image captured by the
    window created.
    You can redefine that rectangle with a new drag and drop or once satisfied
    press q to end.
    Args:
        None
    Returns:
        __IX__
        __FX__
        __IY__
        __FY__
    Side Effect:
        Changes the values of global variables
        __IX__
        __FX__
        __IY__
        __FY__
        __DRAWING__
    """
    global __IX__, __FX__, __IY__, __FY__, __DRAWING__
    if __IX__ is None:
        __IX__ = __FX__ = __IY__ = __FY__ = 0
        __DRAWING__ = False

    my_region = Capture(monitor=1)
    img = np.array(my_region.grab())
    cv2.namedWindow("InitWindow")
    cv2.setMouseCallback("InitWindow", capture_mouse_drag_box)
    while True:
        img = np.array(my_region.grab())
        if (__IX__ > 0 and __IY__ > 0 and __FY__ > __IY__ and __FX__ > __IX__):
            sub_img = img[__IY__:__FY__, __IX__:__FX__]
            white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
            res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
            img[__IY__:__FY__, __IX__:__FX__] = res
        cv2.imshow("InitWindow", img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    return(__IX__, __FX__, __IY__, __FY__)


class Capture():
    """
    This class allows the user to define a window region on the screen and
    the the capture of that region can be executed. It uses the mss python
    package.
    For optimum performance the import in 2nd line must be changed to:
    # MacOS X
    from mss.darwin import MSS as mss

    # GNU/Linux
    from mss.linux import MSS as mss

    # Microsoft Windows
    from mss.windows import MSS as mss
    """

    def __init__(self, bbox=None, monitor=1):
        """
        Creates a new capturable region
        Args:
            bbox        A base box, with 4 coordinates, x, y, width, height
            monitor     The monitor number that will be captured
        Returns:
            Nothing
        """
        with mss() as sct:
            self.monitor = sct.monitors[monitor]
            if bbox:
                self.bbox = bbox
            else:
                img = sct.grab(self.monitor)
                self.bbox = (0, 0, img.size.width, img.size.height)
        print(f"Capture Init {self.bbox}")

    def grab(self):
        """
        This method grabs an image from the defined region during the init
        """
        with mss() as sct:
            img = sct.grab(self.bbox)
            # Converting to Pillow Image
            return(Image.frombytes('RGB', img.size, img.bgra, 'raw', 'RGBX'))


if __name__ == "__main__":
    ix, fx, iy, fy = get_capture_coords()

    my_cann = Cannyfier(ix, iy, fx, fy)
