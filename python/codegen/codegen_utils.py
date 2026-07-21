def pointer_to(obj: str):
    return f"ptr(new {obj})"


def list_of(elements: list[str]):
    if elements:
        return pointer_to(f"list({{{', '.join(elements)}}})")
    else:
        assert False, "We don't support empty lists for now"
