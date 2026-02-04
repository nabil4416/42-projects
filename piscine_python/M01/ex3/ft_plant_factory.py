#!/usr/bin/env python3


class Plant:
    """Represents a plant created by the factory."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """
        Initialize a Plant instance.

        :param name: Name of the plant
        :param height: Height in centimeters
        :param age: Age in days
        """
        self.name = name
        self.height = height
        self.age = age


if __name__ == "__main__":
    print("=== Plant Factory Output ===")

    plants = [
        Plant("Rose", 25, 30),
        Plant("Oak", 200, 365),
        Plant("Cactus", 5, 90),
        Plant("Sunflower", 80, 45),
        Plant("Fern", 15, 120),
    ]

    for plant in plants:
        print(f"Created: {plant.name} ({plant.height}cm, {plant.age} days)")

    print()
    print(f"Total plants created: {len(plants)}")
