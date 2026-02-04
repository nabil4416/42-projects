#!/usr/bin/env python3
from typing import List


class Plant:
    """Represents a plant that can grow and age."""

    def __init__(self, name: str, height_cm: int, age_days: int) -> None:
        """
        Initialize a Plant instance.

        :param name: Name of the plant
        :param height_cm: Height in centimeters
        :param age_days: Age in days
        """
        self.name = name
        self.height_cm = height_cm
        self.age_days = age_days

    def grow(self, cm: int = 1) -> None:
        """Increase the plant height by the given centimeters."""
        self.height_cm += cm

    def age(self, days: int = 1) -> None:
        """Increase the plant age by the given number of days."""
        self.age_days += days

    def get_info(self) -> str:
        """Return formatted plant information."""
        return f"{self.name}: {self.height_cm}cm, {self.age_days} days old"


def simulate_week(plants: List[Plant]) -> None:
    """Simulate one week of growth for a list of plants."""
    print("=== Day 1 ===")
    for plant in plants:
        print(plant.get_info())

    for _ in range(6):
        for plant in plants:
            plant.grow()
            plant.age()

    print("=== Day 7 ===")
    for plant in plants:
        print(plant.get_info())


if __name__ == "__main__":
    plants = [
        Plant("Rose", 25, 30),
        Plant("Tulip", 10, 5),
    ]

    start_height = plants[0].height_cm
    simulate_week(plants)
    growth = plants[0].height_cm - start_height
    print(f"Growth this week: {growth}cm")
