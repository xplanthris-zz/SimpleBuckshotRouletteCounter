from enum import Enum


class Bullet(Enum):
    """
    An enumeration for representing the types of bullets in the SimpleBuckshotRouletteCounter.

    This enumeration distinguishes between live and blank bullets, as well as whether a bullet
    has been marked by using the burner phone feature, which requires special dealing with in the autofill function.
    """

    # Standard bullets that have not been marked through the burner phone.
    UNKNOWN = 0
    BLANK = 1
    LIVE = 2

    # Bullets that have been marked by the burner phone.
    # These special types allow the autofill function to differentiate between regular and marked bullets,
    # ensuring accurate autofill behavior.
    BLANK_MARKED = 3
    LIVE_MARKED = 4
