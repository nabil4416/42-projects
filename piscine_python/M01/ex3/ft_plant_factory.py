#!/usr/bin/env python3

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

print("=== Plant Factory Output ===")

plants = [
    Plant("Rose", 25, 30),
    Plant("Oak", 200, 365),
    Plant("Cactus", 5, 90),
    Plant("Sunflower", 80, 45),
    Plant("Fern", 15, 120),
]

for p in plants:
    print(f"Created: {p.name} ({p.height}cm, {p.age} days)")

print()
print(f"Total plants created: {len(plants)}")

