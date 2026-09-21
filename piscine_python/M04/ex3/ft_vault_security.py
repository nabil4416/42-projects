"""
Exercise 3 - Vault Security (ft_vault_security.py)

Goals:
- Use `with` for ALL file operations (safe closing).
- Read classified data with mode "r".
- Write preservation data with mode "w".
- Handle an exception scenario (e.g., missing input file) without crashing.
- Keep outputs clear for evaluation.
"""

INPUT_FILE = "classified_data.txt"
OUTPUT_FILE = "security_protocols.txt"


def secure_vault_security() -> None:
    """Read classified data and preserve a protocol file safely."""
    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols\n")

    print("SECURE EXTRACTION:\n")

    try:
        # Reading test: must use `with open(..., 'r') as file:`
        with open(INPUT_FILE, "r") as file:
            content = file.read()

        print(content)
        print()

        print("SECURE PRESERVATION:")

        # Writing test: must use `with open(..., 'w') as file:`
        # "w" overwrites the file and creates it if it doesn't exist.
        with open(OUTPUT_FILE, "w") as file:
            file.write("Data preserved\n")
            file.write("Status: OK\n")

        print("Data preserved successfully.\n")

    except Exception as err:
        # Exception scenario: evaluator may delete the input file to test you
        print("ERROR: Vault operation failed.")
        print("Reason:", str(err))
        print()

    # This line must appear even if an exception happens
    print("Vault automatically sealed upon completion\n")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    secure_vault_security()
    print("All vault operations completed with maximum security.")
