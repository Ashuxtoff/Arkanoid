class Button:
    def __init__(self, coords, size,
                 text, base_color, active_color, number):
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.size = size
        self.height = size[1]
        self.width = size[0]
        self.text = text
        self.base_color = base_color
        self.active_color = active_color
        self.number = number
