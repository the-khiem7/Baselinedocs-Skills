import pytest

from helpers import ROOT, SKILL_NAMES, read_text

FAMILY_MAP = ROOT / "assets" / "source" / "family-map.html"


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_family_map_names_every_skill(name):
    """The family map is an image, so its HTML source is the only thing a test can read.
    A skill added without a chip there leaves the README picture silently incomplete."""
    assert f'data-skill="{name}"' in read_text(FAMILY_MAP), (
        f"assets/source/family-map.html has no data-skill=\"{name}\" chip; add one, "
        "then re-render family-map.webp and family-map-dark.webp"
    )
