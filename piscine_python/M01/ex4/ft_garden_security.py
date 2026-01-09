#!/usr/bin/env python3

class SecurePlant:
    def __init__(self, name: str):
        self.name = name
        self._height = 0
        self._age = 0

    # --- Getters (safe access) ---
    def get_height(self) -> int:
        return self._height

    def get_age(self) -> int:
        return self._age

    # --- Setters (controlled modification + validation) ---
    def set_height(self, new_height: int) -> None:
        if new_height < 0:
            print("Security: Negative height rejected")
            return
        self._height = new_height
        print(f"Height updated: {self._height}cm [OK]")

    def set_age(self, new_age: int) -> None:
        if new_age < 0:
            print("Security: Negative age rejected")
            return
        self._age = new_age
        print(f"Age updated: {self._age} days [OK]")

    def __str__(self) -> str:
        return f"{self.name} ({self._height}cm, {self._age} days)"


def main() -> None:
    print("=== Garden Security System ===")

    plant = SecurePlant("Rose")
    print(f"Plant created: {plant.name}")

    plant.set_height(25)
    plant.set_age(30)

    print("\nInvalid operation attempted: height -5cm [REJECTED]")
    plant.set_height(-5)

    print(f"\nCurrent plant: {plant}")


if __name__ == "__main__":
    main()
