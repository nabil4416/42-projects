#!/usr/bin/env python3

MIN_TEMP_C = 0
MAX_TEMP_C = 40

def check_temperature(temp_str):
    try:
        temp = int(temp_str)
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number.")
        return None

    if temp < MIN_TEMP_C:
        print(
                f"Error: {temp}°C is too cold for plants "
                f"(min {MIN_TEMP_C}°C)."
        )
        return None

    if temp > MAX_TEMP_C:
        print(
                f"Error: {temp}°C is too hot for plants "
                f"(max {MAX_TEMP_C}°C)."
        )
        return None

    return temp

def test_temperature_input():
    tests = ["25", "abc", "100", "-50"]

    print("=== Garden Temperature Checker ===")

    for value in tests:
        print(f"\nTesting temperature: {value}")
        temp = check_temperature(value)
        if temp is not None:
            print(f"Temperature {temp}°C is perfect for plants!")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature_input()
