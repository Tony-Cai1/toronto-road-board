import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app, load_restrictions


def card_for(page: str, object_id: int) -> str:
    return page.split(f'data-object-id="{object_id}"', 1)[1].split("</article>", 1)[0]


def main() -> int:
    restrictions = {item["OBJECTID"]: item for item in load_restrictions()}
    app = create_app()

    with app.test_client() as client:
        response = client.get("/")
        page = response.get_data(as_text=True)

    full_closure = restrictions[2099]
    lane_restriction = restrictions[2088]
    full_card = card_for(page, full_closure["OBJECTID"])
    lane_card = card_for(page, lane_restriction["OBJECTID"])

    full_is_correct = (
        "full closure" in full_closure["DESCRIPTION"].lower()
        and "Road closed" in full_card
    )
    lane_bug_reproduced = (
        "lane blocked" in lane_restriction["DESCRIPTION"].lower()
        and "Road closed" in lane_card
    )

    print(
        "PASS - full closure: 'Road closed' is correct"
        if full_is_correct
        else "FAIL — full closure case did not render as expected"
    )
    print(
        "REPRODUCED - lane restriction: 'Road closed' is incorrect"
        if lane_bug_reproduced
        else "NOT REPRODUCED — lane restriction case changed"
    )

    return 0 if full_is_correct and lane_bug_reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
