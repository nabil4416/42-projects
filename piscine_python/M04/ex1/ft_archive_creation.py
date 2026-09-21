def create_archive() -> None:
    """
    Create a new archive file named 'new_discovery.txt'
    and write three preservation entries into it.
    """

    filename: str = "new_discovery.txt"

    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===")
    print()
    print("Initializing new storage unit:", filename)

    file = open(filename, "w")
    print("Storage unit created successfully...")
    print()
    print("Inscribing preservation data...")

    entry1: str = "[ENTRY 001] New quantum algorithm discovered\n"
    entry2: str = "[ENTRY 002] Efficiency increased by 347%\n"
    entry3: str = "[ENTRY 003] Archived by Data Archivist trainee\n"

    file.write(entry1)
    print(entry1.strip())

    file.write(entry2)
    print(entry2.strip())

    file.write(entry3)
    print(entry3.strip())

    file.close()

    print()
    print("Data inscription complete. Storage unit sealed.")
    print("Archive '" + filename + "' ready for long-term preservation.")


def main() -> None:
    """
    Entry point of the program.
    """
    create_archive()


main()

