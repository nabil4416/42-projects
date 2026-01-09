#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height_cm: int, age_days: int):
        self.name = name
        self.height_cm = height_cm
        self.age_days = age_days

    def grow(self, cm: int = 1) -> None:
        self.height_cm += cm

    def age(self, days: int = 1) -> None:
        self.age_days += days

    def get_info(self) -> str:
        return f"{self.name}: {self.height_cm}cm, {self.age_days} days old"


def simulate_week(plants: list) -> None:
    print("=== Day 1 ===")
    for p in plants:
        print(p.get_info())

    for _ in range(6):
        for p in plants:
            p.grow(1)
            p.age(1)

    print("=== Day 7 ===")
    for p in plants:
        print(p.get_info())


# Création des plantes
plants = [
    Plant("Rose", 25, 30),
    Plant("Tulip", 10, 5),
]

# Calcul de la croissance hebdomadaire de la première plante
start_height = plants[0].height_cm

simulate_week(plants)

growth = plants[0].height_cm - start_height
print(f"Growth this week: +{growth}cm")
