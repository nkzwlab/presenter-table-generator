from typing import Any

import yaml

from ..presenter import Presenter, PresentationKind


def from_yaml(filename: str) -> list[Presenter]:
    data = None

    with open(filename, "r") as f:
        data = yaml.load(f)

    if isinstance(data, dict):
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
    title = None
    if isinstance(person, dict):
        loginname = person.keys()[0]
        title = person.get(loginname)

    presenter = Presenter(loginname, kg, kind, title=title)
    return presenter
