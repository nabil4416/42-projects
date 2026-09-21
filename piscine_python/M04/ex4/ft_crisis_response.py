def crisis_handler(filename: str) -> None:
    """
    Attempt to access an archive file and handle possible crisis scenarios.

    Parameters:
        filename (str): The name of the file to access.

    Returns:
        None
    """
    if filename == "standard_archive.txt":
        print("ROUTINE ACCESS: Attempting access to '{}'...".format(filename))
    else:
        print("CRISIS ALERT: Attempting access to '{}'...".format(filename))

    try:
        with open(filename, "r") as file:
            content: str = file.read()

        content = content.strip()

        print("SUCCESS: Archive recovered - '{}'".format(content))
        print("STATUS: Normal operations resumed")

    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")

    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")

    except Exception:
        print("RESPONSE: Unexpected system anomaly detected")
        print("STATUS: Crisis handled, system stable")

    print("")


def main() -> None:
    """
    Entry point of the Crisis Response system.

    Simulates multiple archive access attempts
    to demonstrate crisis management handling.
    """
    print("*** CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ***")
    print("")

    crisis_handler("lost_archive.txt")
    crisis_handler("classified_vault.txt")
    crisis_handler("standard_archive.txt")

    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    main()
