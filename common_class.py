class Position:
    def __init__(self, x, y, speed_x=10, speed_y=10, gravity=9.8, direction=1, wind=0):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = direction
        self.gravity = gravity
        self.wind = wind
