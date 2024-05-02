class PhysicsObject:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update_position(self, delta_time, width, height):
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        if self.x <= 0 or self.x >= width:
            self.vx *= -1
        if self.y <= 0 or self.y >= height:
            self.vy *= -1

class TargetPhysics(PhysicsObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
