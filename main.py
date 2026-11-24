#!/usr/bin/env python3
"""Write the alien field-notes entry to /output/entry.txt.

The entry is a single line: an alien tourist's review of Earth.
It is assembled from three fragments so the structure of the joke
stays visible in the code: an observation header, the remarkable
device the species built, and the underwhelming way they use it.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

# Fragment 1: the field-note header plus what the species invented.
HEADER = "Observation: the species invented a device"
# Fragment 2: what that device can do.
CAPABILITY = "to summon any fact instantly,"
# Fragment 3: what the device is actually used for.
USAGE = "and uses it mainly to argue with strangers and photograph soup."

MAX_CHARACTERS = 200


def build_entry() -> str:
    """Join the fragments with single spaces into one line."""
    return " ".join(part.strip() for part in (HEADER, CAPABILITY, USAGE))


def validate(text: str) -> None:
    """Check the entry against the bounty gate before writing it."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARACTERS:
        raise ValueError(f"entry is {len(text)} characters, over {MAX_CHARACTERS}")
    if not text.startswith("Observation:"):
        raise ValueError("entry must open with the observation header")
    if not text.endswith("."):
        raise ValueError("entry must end with a full stop")
    for phrase in ("summon any fact instantly", "argue with strangers", "photograph soup"):
        if phrase not in text:
            raise ValueError(f"entry is missing required phrase: {phrase}")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry does not round-trip as UTF-8")
    if len(encoded) != len(text):
        raise ValueError("entry is expected to be plain ASCII")


def main() -> None:
    text = build_entry()
    validate(text)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(text.encode("utf-8"))
    written = OUTPUT_PATH.read_bytes()
    if written != text.encode("utf-8"):
        raise SystemExit("read-back mismatch: /output/entry.txt differs from the entry")
    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
