class CodiceAteco(object):

    def __init__(self, main: int, middle: int, end: int):
        self.main = main
        self.middle = middle
        self.end = end

    @classmethod
    def parse(cls, s: str) -> "CodiceAteco":
        return cls(*list(map(int, map(lambda x: x.strip(), s.split('.')))))

    def __str__(self) -> str:
        return f"{self.main:02d}.{self.middle:02d}.{self.end:02d}"
