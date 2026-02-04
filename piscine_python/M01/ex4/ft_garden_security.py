#!/usr/bin/env python3


class SecurePlant:
    """A plant with protected data and validated updates."""

    def __init__(self, name: str) -> None:
        """
        Create a new SecurePlant with default height and age.

        :param name: Plant name
        """
        self.name = name
        self._height_cm = 0
        self._age_days = 0

    def set_height(self, height_cm: int) -> None:
        """
        Update plant height (cm) if the value is valid.

        Negative values are rejected.
        """
        if height_cm < 0:
            print(
                f"Invalid operation attempted: height {height_cm}cm "
                "[REJECTED]"
            )

            print("Security: Negative height rejected")
            return
        self._height_cm = height_cm
        print(f"Height updated: {self._height_cm}cm [OK]")

    def set_age(self, age_days: int) -> None:
        """
        Update plant age (days) if the value is valid.

        Negative values are rejected.
        """
        if age_days < 0:
            print(
                f"Invalid operation attempted: age {age_days} "
                "days [REJECTED]"
            )

            print("Security: Negative age rejected")
            return
        self._age_days = age_days
        print(f"Age updated: {self._age_days} days [OK]")

    def get_height(self) -> int:
        """Return the plant height in centimeters."""
        return self._height_cm

    def get_age(self) -> int:
        """Return the plant age in days."""
        return self._age_days

    def __str__(self) -> str:
        """Return a human-readable representation of the plant."""
        return f"{self.name} ({self._height_cm}cm, {self._age_days} days)"


if __name__ == "__main__":
    print("=== Garden Security System ===")

    plant = SecurePlant("Rose")
    print("Plant created:", plant.name)

    plant.set_height(25)
    plant.set_age(30)

    print()
    plant.set_height(-5)

    print()
    print("Current plant:", plant)
