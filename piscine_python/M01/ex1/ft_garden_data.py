#!/usr/bin/env python3


class Plant:
    """Represents a plant in the garden."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """
        Initialize a Plant object.

        :param name: Name of the plant
        :param height: Height in centimeters
        :param age: Age in days
        """
        self.name = name
        self.height = height
        self.age = age

    def display(self) -> None:
        """Display plant information."""
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main() -> None:
    """Main execution function."""
    print("=== Garden Plant Registry ===")

    rose = Plant("Rose", 25, 30)
    sunflower = Plant("Sunflower", 80, 45)
    cactus = Plant("Cactus", 15, 120)

    rose.display()
    sunflower.display()
    cactus.display()


if __name__ == "__main__":
    main()
