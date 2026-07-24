class Shape:
    def __init__(self, side: int) -> None:
        self.side = side


class Square(Shape):
    def area(self) -> int:
        return self.side * self.side


def main() -> int:
    return 0
