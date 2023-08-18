from game_object import GameObject

class Player(GameObject):
    def __init__(self, x, y, width, height, image_path, speed):
        super().__init__(x, y, width, height, image_path)
        self.speed = speed

    def move(self, direction, max_height, max_width):
        vertical_direction, horizontal_direction = direction
        new_x = self.x + (horizontal_direction * self.speed)
        new_y = self.y + (vertical_direction * self.speed)
        if (0 <= new_y <= max_height - self.height):
            self.y = new_y
        if (0 <= new_x <= max_width - self.width):
            self.x = new_x
