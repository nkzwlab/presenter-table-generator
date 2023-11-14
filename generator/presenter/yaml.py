from typing import Any

import yaml

from .presenter import Presenter, PresentationKind


def from_yaml(filename: str) -> list[Presenter]:
    data = None

    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise TypeError("Invalid yaml input. It must be a dict.")

    # Ensure dict type for completion while development
    data = dict(data)

    presenters = from_dict(data)
    return presenters


def from_dict(data: dict[str, Any]) -> list[Presenter]:
    """

    Args:
        data (dict[str, Any]):
        ```
        wip:
            kg1:
                - presenter1
                - presenter2
            kg2:
                - presenter3: "研究タイトル"
        term:
            kg1:
                - presenter5
        ```

    Returns:
        list[Presenter]
    """

    output = []

    for kind, kgs in data.items():
        for kg, presenters in kgs.items():
            for person in presenters:
                presenter = per_person(kind, kg, person)
                output.append(presenter)

    return output


def per_person(
    kind: PresentationKind, kg: str, person: str | dict[str, str]
) -> Presenter:
    loginname = person
    presenter = None

    if isinstance(person, dict):
        # It must be `"loginname": "title"` form
        keys = list(person.keys())
        loginname = keys[0]
        title = person.get(loginname)

        presenter = Presenter(loginname, kg, kind, title=title)
    else:
        presenter = Presenter(loginname, kg, kind)

    return presenter
