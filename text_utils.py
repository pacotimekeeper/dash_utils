
def join_lines(raw_text: str) -> str:
    lines = [line for line in raw_text.splitlines() if line.strip()]
    return "; ".join(lines)


def masked_pattern(numbers: list[str]) -> str:
    """
    Build a pattern from a list of equal-length strings where the common prefix is kept
    and the differing suffix is replaced with 'X' characters.
    """
    if not numbers:
        raise ValueError("numbers must contain at least one element")

    prefix = numbers[0]
    for s in numbers[1:]:
        max_idx = min(len(prefix), len(s))
        i = 0
        while i < max_idx and prefix[i] == s[i]:
            i += 1
        prefix = prefix[:i]
        if not prefix:
            break

    variation_length = len(numbers[0]) - len(prefix)
    return prefix + "X" * variation_length


if __name__ == "__main__":
    strs = """
    a
    b
    c
    """
    print(join_lines(strs))
