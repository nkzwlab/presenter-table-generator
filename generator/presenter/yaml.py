from datetime import timedelta
from typing import Any

import yaml

from .config import Break, Config
from lib.date import datetime_from_time
from .presenter import Presentation, Timetable, PresentationKind, FixedPresentation


def break_from_dict(data: dict) -> Break:
    before = data.get("before")
    after = data.get("after")

    if before is not None:
        before = datetime_from_time(before)
    if after is not None:
        after = datetime_from_time(after)

    length = int(data["length"])
    length = timedelta(minutes=length)

    title = data.get("title")

    return Break(length, before, after, title)


class YamlConfig(Config):
    def __init__(self, config: dict):
        root_path = config.get("presentation_page_root")

        start_time = config.get("start_time")
        if start_time is not None:
            start_time = datetime_from_time(start_time)

        presentation_time = config.get("presentation_time")
        if isinstance(presentation_time, int):
            presentation_time = timedelta(minutes=presentation_time)
        elif isinstance(presentation_time, dict):
            presentation_time = {
                kind: timedelta(minutes=minutes)
                for kind, minutes in presentation_time.items()
            }

        breaks = config.get("breaks")
        if breaks is not None:
            bs = []
            for brek in breaks:
                b = break_from_dict(brek)
                bs.append(b)
            breaks = bs

        super().__init__(
            page_root=root_path,
            start_time=start_time,
            presentation_time=presentation_time,
            breaks=breaks,
        )


def from_yaml(filename: str, randomize: bool = False) -> Timetable:
    data = None

    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise TypeError("Invalid yaml input. It must be a dict.")

    # Ensure dict type for completion while development
    data = dict(data)

    presenters_data = data["presenters"]

    config_dict = data.get("config")
    config = YamlConfig(config_dict)

    presenters_list = get_presenters(presenters_data, config)

    presenters = Timetable.create(presenters_list, config, randomize=randomize)

    return presenters


def get_presenters(data: dict[str, Any], config: Config) -> Timetable:
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

    presenter_list = []

    for kind, kgs in data.items():
        for kg, presenters in kgs.items():
            for person in presenters:
                presenter = per_person(kind, kg, person, config)
                presenter_list.append(presenter)

    return presenter_list


def per_person(
    kind: PresentationKind,
    kg: str,
    person: str | dict[str, str],
    config: Config,
) -> Presentation:
    loginname = person
    page_path = f"{config.page_root}/{loginname}"
    length = config.presentation_length(kind)
    presenter = None

    if isinstance(person, dict):
        # - name: "login name"
        #   before: "hh:mm" | null
        #   after: "hh:mm" | null
        #   title: "title" | null

        loginname = person["name"]
        after = person.get("after") or config.start_time
        before = person.get("before")
        title = person.get("title")
        if after or before:
            presenter = FixedPresentation(
                kind=kind,
                title=title,
                length=length,
                loginname=loginname,
                kg=kg,
                page_path=page_path,
                after=after,
                before=before,
            )
        else:
            presenter = Presentation(
                kind=kind,
                title=title,
                length=length,
                loginname=loginname,
                kg=kg,
                page_path=page_path,
            )
    else:
        presenter = Presentation(
            kind=kind, length=length, loginname=loginname, kg=kg, page_path=page_path
        )

    return presenter
