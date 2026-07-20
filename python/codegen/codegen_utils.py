def pointer_to(obj: str):
    return f"ptr(new {obj})"


def list_of(elements: list[str]):
    return pointer_to(f"list({{{', '.join(elements)}}})")
