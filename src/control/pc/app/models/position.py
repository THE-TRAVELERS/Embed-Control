class Position:
    """
    Represents a position with x and y coordinates ranging from -1 to 1.
    """

    def __init__(self, x: float, y: float):
        self.x = max(min(x, 1.0), -1.0)
        self.y = max(min(y, 1.0), -1.0)

    def __str__(self):
        return f"{self.x};{self.y}"
