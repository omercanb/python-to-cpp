def pointer_to(obj: str):
    return f"ptr(new {obj})"


def list_of(elements: list[str]):
    return f"list({', '.join(elements)})"
