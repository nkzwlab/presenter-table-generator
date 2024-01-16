from datetime import datetime


def good_to_toke(
    present_time: datetime,
    next_end: datetime,
    after: datetime | None = None,
    before: datetime | None = None,
) -> bool:
    good = True

    if after is not None:
        good = good and after <= present_time

    if before is not None:
        good = good and present_time <= before < next_end

    return good
