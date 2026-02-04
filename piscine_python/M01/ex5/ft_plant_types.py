#!/usr/bin/env python3
"""
Garden Plant Types - Inheritance demo.

Demonstrates inheritance + polymorphism with different plant types.
"""


class Plant:
    """Base class representing a generic plant."""

    def __init__(self, name: str, height_cm: int, age_days: int) -> None:
        """
        Initialize a plant.

        :param name: Plant name
        :param height_cm: Height in centimeters
        :param age_days: Age in days
        """
        self.name = name
        self.height_cm = height_cm
        self.age_days = age_days

    def describe(self, plant_type: str) -> None:
        """
        Print a one-line description of the plant.

        :param plant_type: A label describing the plant category (e.g. "Flower")
        """
        print(
            f"{self.name} ({plant_type}): "
            f"{self.height_cm}cm, {self.age_days} days"
        )


class Flower(Plant):
    """A specialized Plant that has a color and can bloom."""

    def __init__(self, name: str, height_cm: int, age_days: int, color: str) -> None:
        """
        Initialize a Flower.

        :param name: Flower name
        :param height_cm: Height in centimeters
        :param age_days: Age in days
        :param color: Flower color
        """
        super().__init__(name, height_cm, age_days)
        self.color = color

    def bloom(self) -> None:
        """Print a bloom message."""
        print(f"{self.name} is blooming beautifully!")

    def show(self) -> None:
        """Display flower information."""
        self.describe("Flower")
        print(f"Color: {self.color}")


class Tree(Plant):
    """A specialized Plant that has a trunk diameter and can produce shade."""

    def __init__(
        self,
        name: str,
        height_cm: int,
        age_days: int,
        trunk_diameter_cm: int,
    ) -> None:
        """
        Initialize a Tree.

        :param name: Tree name
        :param height_cm: Height in centimeters
        :param age_days: Age in days
        :param trunk_diameter_cm: Trunk diameter in centimeters
        """
        super().__init__(name, height_cm, age_days)
        self.trunk_diameter_cm = trunk_diameter_cm

    def produce_shade(self) -> float:
        """
        Compute and print the shade area produced by the tree.

        Note: The coefficient is arbitrary (demo purpose), not a real model.

        :return: Shade area as a float (square meters)
        """
        shade_area = self.trunk_diameter_cm * 1.56
        print(f"{self.name} provides {shade_area:.2f} square meters of shade")
        return shade_area

    def show(self) -> None:
        """Display tree information."""
        self.describe("Tree")
        print(f"Trunk diameter: {self.trunk_diameter_cm}cm")


class Vegetable(Plant):
    """A specialized Plant that has a harvest season and nutritional value."""

    def __init__(
        self,
        name: str,
        height_cm: int,
        age_days: int,
        harvest_season: str,
        nutritional_value: str,
    ) -> None:
        """
        Initialize a Vegetable.

        :param name: Vegetable name
        :param height_cm: Height in centimeters
        :param age_days: Age in days
        :param harvest_season: e.g. "summer", "autumn"
        :param nutritional_value: e.g. "vitamin C"
        """
        super().__init__(name, height_cm, age_days)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def show(self) -> None:
        """Display vegetable information."""
        self.describe("Vegetable")
        print(f"Harvest: {self.harvest_season}")
        print(f"{self.name} is rich in {self.nutritional_value}")


if __name__ == "__main__":
    # EN/FR: Demo (create at least 2 of each)
    print("=== Garden Plant Types ===\n")

    # Flowers (2)
    rose = Flower("Rose", 25, 30, "dred")
    tulip = Flower("Tulip", 20, 18, "yellow")

    rose.show()
    rose.bloom()
    print()
    tulip.show()
    tulip.bloom()
    print("\n---\n")

    # Trees (2)
    oak = Tree("Oak", 500, 1825, 50)
    pine = Tree("Pine", 420, 1500, 35)

    oak.show()
    oak.produce_shade()
    print()
    pine.show()
    pine.produce_shade()
    print("\n---\n")

    # Vegetables (2)
    tomato = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    carrot = Vegetable("Carrot", 30, 70, "autumn", "beta-carotene")

    tomato.show()
    print()
    carrot.show()
