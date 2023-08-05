from dataclasses import dataclass


@dataclass
class Currency:
    name: str
    max_length: int
    decimal_length: int

    def __post_init__(self):
        if self.decimal_length >= self.max_length:
            raise ValueError(f"max_length should be bigger than decimal_length")
