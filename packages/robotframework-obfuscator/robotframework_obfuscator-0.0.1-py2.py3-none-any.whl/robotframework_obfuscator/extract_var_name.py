from typing import Optional


def get_inner_variable_name(text: str) -> Optional[str]:
    """
    Something as `@{var}=` would return `var`.

    If the text is not from a variable, None is returned.
    """
    from robotframework_ls.impl import robot_constants

    text = text.strip()
    if text.endswith("="):
        text = text[:-1].strip()

    for p in robot_constants.VARIABLE_PREFIXES:
        if text.startswith(p + "{") and text.endswith("}"):
            return text[2:-1]
    return None
