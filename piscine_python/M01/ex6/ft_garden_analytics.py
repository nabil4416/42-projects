#!/usr/bin/env python3
"""
ft_garden_analytics.py

A compact "garden analytics platform" built to demonstrate:
- A manager that handles multiple gardens
- A nested statistics helper class
- An inheritance chain (Plant -> FloweringPlant -> PrizeFlower)
- Instance methods, class methods, and static utility methods
"""

from __future__ import annotations

from typing import Dict, List, Tuple


class Plant:
    """Base plant with a name and a height in centimeters."""

    def __init__(self, name: str, height_cm: int) -> None:
        """Initialize a plant with its name and current height."""
        self.name: str = name
        self.height_cm: int = height_cm

    def grow(self, cm: int = 1) -> None:
        """Increase the plant height by `cm` centimeters."""
        self.height_cm += cm

    def get_info(self) -> str:
        """Return a human-readable description for reports."""
        return f"{self.name}: {self.height_cm}cm"


class FloweringPlant(Plant):
    """A plant that has flowers and can be in a blooming state."""

    def __init__(
        self,
        name: str,
        height_cm: int,
        flower_color: str,
        is_blooming: bool = True,
    ) -> None:
        """Initialize a flowering plant with color and bloom status."""
        super().__init__(name, height_cm)
        self.flower_color: str = flower_color
        self.is_blooming: bool = is_blooming

    def get_info(self) -> str:
        """Return a report line including flower details."""
        blooming = "blooming" if self.is_blooming else "not blooming"
        return (
            f"{self.name}: {self.height_cm}cm, {self.flower_color} "
            f"flowers ({blooming})"
        )


class PrizeFlower(FloweringPlant):
    """A flowering plant that can earn prize points."""

    def __init__(
        self,
        name: str,
        height_cm: int,
        flower_color: str,
        prize_points: int,
        is_blooming: bool = True,
    ) -> None:
        """Initialize a prize flower with prize points."""
        super().__init__(name, height_cm, flower_color, is_blooming)
        self.prize_points: int = prize_points

    def get_info(self) -> str:
        """Return a report line including prize points."""
        base = super().get_info()
        return f"{base}, Prize points: {self.prize_points}"


class GardenManager:
    """Manage multiple gardens and compute analytics via a nested helper."""

    class Garden:
        """A single garden containing a collection of plants."""

        def __init__(self, owner: str) -> None:
            """Initialize an empty garden for `owner`."""
            self.owner: str = owner
            self._plants: List[Plant] = []
            self._total_growth_cm: int = 0

        def add_plant(self, plant: Plant) -> None:
            """Add one plant to this garden."""
            self._plants.append(plant)

        def plants(self) -> List[Plant]:
            """Return a copy of the plant collection to preserve encapsulation."""
            return list(self._plants)

        def register_growth(self, cm: int) -> None:
            """Accumulate growth statistics for this garden."""
            self._total_growth_cm += cm

        def total_growth_cm(self) -> int:
            """Return the total recorded growth in this garden."""
            return self._total_growth_cm

    class GardenStats:
        """Compute statistics for a garden (helper nested inside manager)."""

        def __init__(self, garden: GardenManager.Garden) -> None:
            """Bind stats helper to one garden."""
            self._garden: GardenManager.Garden = garden

        def plants_added(self) -> int:
            """Return the number of plants currently in the garden."""
            return len(self._garden.plants())

        def total_growth_cm(self) -> int:
            """Return the garden total growth."""
            return self._garden.total_growth_cm()

        def plant_type_counts(self) -> Tuple[int, int, int]:
            """Return counts: (regular, flowering, prize)."""
            regular = 0
            flowering = 0
            prize = 0
            for plant in self._garden.plants():
                if isinstance(plant, PrizeFlower):
                    prize += 1
                elif isinstance(plant, FloweringPlant):
                    flowering += 1
                else:
                    regular += 1
            return regular, flowering, prize

    def __init__(self) -> None:
        """Initialize the manager with zero gardens."""
        self._gardens: Dict[str, GardenManager.Garden] = {}

    def add_garden(self, owner: str) -> None:
        """Create a garden for `owner` if it doesn't exist."""
        if owner not in self._gardens:
            self._gardens[owner] = GardenManager.Garden(owner)

    def add_plant(self, owner: str, plant: Plant) -> None:
        """Add a plant to `owner`'s garden (creates the garden if needed)."""
        self.add_garden(owner)
        self._gardens[owner].add_plant(plant)
        print(f"Added {plant.name} to {owner}'s garden")

    def help_plants_grow(self, owner: str, cm: int = 1) -> None:
        """Grow every plant in `owner`'s garden by `cm` centimeters."""
        garden = self._gardens.get(owner)
        if garden is None:
            return
        if cm < 0:
            return
        print(f"\n{owner} is helping all plants grow...")
        for plant in garden.plants():
            plant.grow(cm)
            garden.register_growth(cm)
            print(f"{plant.name} grew {cm}cm")

    def print_garden_report(self, owner: str) -> None:
        """Print a report for `owner`'s garden with computed statistics."""
        garden = self._gardens.get(owner)
        if garden is None:
            return

        stats = GardenManager.GardenStats(garden)
        print(f"\n--- {owner}'s Garden Report ---")
        print("Plants in garden:")
        for plant in garden.plants():
            print(f"- {plant.get_info()}")

        regular, flowering, prize = stats.plant_type_counts()
        print(
            f"\nPlants added: {stats.plants_added()}, "
            f"Total growth: {stats.total_growth_cm()}cm"
        )
        print(
            "Plant types: "
            f"{regular} regular, {flowering} flowering, {prize} prize flowers"
        )

    def garden_score(self, owner: str) -> int:
        """Compute a simple score for one garden."""
        garden = self._gardens.get(owner)
        if garden is None:
            return 0

        score = 0
        plants = garden.plants()
        for plant in plants:
            score += plant.height_cm
            if isinstance(plant, PrizeFlower):
                score += plant.prize_points
        score += len(plants) * 10
        return score

    @staticmethod
    def validate_height(height_cm: int) -> bool:
        """Utility: return True if `height_cm` is a valid plant height."""
        return height_cm >= 0

    @classmethod
    def create_garden_network(cls, manager: GardenManager) -> int:
        """
        Return the number of gardens managed by `manager`.

        Note: The name is defined by the exercise statement; this method
        does not create anything, it reports the current network size.
        """
        return len(manager._gardens)


if __name__ == "__main__":
    print("--- Garden Management System Demo ---\n")

    manager = GardenManager()

    manager.add_plant("Alice", Plant("Oak Tree", 100))
    manager.add_plant("Alice", FloweringPlant("Rose", 25, "red"))
    manager.add_plant("Alice", PrizeFlower("Sunflower", 50, "yellow", 10))

    manager.add_plant("Bob", Plant("Cactus", 82))

    manager.help_plants_grow("Alice", 1)
    manager.print_garden_report("Alice")

    valid = GardenManager.validate_height(10)
    print(f"\nHeight validation test: {valid}")

    alice_score = manager.garden_score("Alice")
    bob_score = manager.garden_score("Bob")
    print(f"Garden scores - Alice: {alice_score}, Bob: {bob_score}")

    total = GardenManager.create_garden_network(manager)
    print(f"Total gardens managed: {total}")
