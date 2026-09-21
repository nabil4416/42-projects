def try_to_access() -> None:
    """
    Read the content of 'ancient_fragment.txt' and display it.

    Expected behavior:
    - Open the file in read mode ("r")
    - Read the entire content using read()
    - Print the recovered data
    - Close the file using close()
    - If the file doesn't exist, print the required ERROR message
    """
    filename: str = "ancient_fragment.txt"

    print(f"Accessing Storage Vault: {filename}")
    print("Connection established...\n")
    print("RECOVERED DATA:")

    try:
        file = open(filename, "r")
        content: str = file.read()
        print(content)
        file.close()
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")


def main() -> None:
    """
    Program entry point: displays the system header and runs the recovery.
    """
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    try_to_access()


if __name__ == "__main__":
    main()

