import cv2
import models


class Drawer:
    image = None
    window_name = None

    def __init__(self, image, window_name="OUTPUT", code=None):
        """
        Drawer utility for drawing usual shapes
        :param image:
        :param window_name:
        :param code: should be the same code for cv2.cvtColor()
        """
        self.image = image
        if code is not None:
            self.convert(code)

        self.window_name = window_name

    def draw_text(self, text, position=(50, 50), color=(0, 0, 255), size=0.9):
        """
        Draws text on specified position
        :param text:
        :param position:
        :param color:
        :param size:
        :return: Drawer
        """
        cv2.putText(self.image, text, position, cv2.FONT_HERSHEY_COMPLEX, size, color)
        return self

    def draw_circle(self, center, radius, color=(0, 0, 255), thickness=2):
        cv2.circle(self.image, center, radius, color, thickness)
        return self

    def draw_contour(self, contour, color=(0, 255, 0), thickness=2):
        cv2.drawContours(self.image, contour, -1, color, thickness)
        return self

    def draw_rect(self, pt1, pt2, color=(0, 0, 255), thickness=1):
        cv2.rectangle(self.image, pt1, pt2, color, thickness)
        return self

    def draw_marker(self, point, color=(255,0,0)):
        cv2.drawMarker(self.image, point, color)
        return self

    def draw_model(self, model):
        """
        Draws model
        :param model: models.BaseModel
        :return:
        """
        model.render(self.image)
        return self

    def show(self):
        cv2.imshow(self.window_name, self.image)

    def convert(self, code):
        self.image = cv2.cvtColor(self.image, code)
        return self
