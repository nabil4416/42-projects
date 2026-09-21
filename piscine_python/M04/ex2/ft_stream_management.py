import sys


def main() -> None:
    """
    Simulates a three-channel communication system.

    - Reads input from stdin using input()
    - Writes normal messages to sys.stdout
    - Writes alert messages to sys.stderr
    """

    # System header (stdout)
    sys.stdout.write("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n\n")

    # Collect user input (stdin)
    archivist_id: str = input(
        "Input Stream active. Enter archivist ID: "
    )
    status_report: str = input(
        "Input Stream active. Enter status report: "
    )

    # Standard output message (stdout)
    sys.stdout.write("\n")
    sys.stdout.write(
        "[STANDARD] Archive status from "
        + archivist_id
        + ": "
        + status_report
        + "\n"
    )

    # Alert message (stderr)
    sys.stderr.write(
        "[ALERT] System diagnostic: "
        "Communication channels verified\n"
    )

    # Final confirmation (stdout)
    sys.stdout.write(
        "[STANDARD] Data transmission complete\n\n"
    )
    sys.stdout.write(
        "Three-channel communication test successful.\n"
    )


if __name__ == "__main__":
    main()
