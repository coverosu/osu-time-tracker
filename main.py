"""osu! time tracker: Tracks the amount of time spent playing the actual game"""
from __future__ import annotations

import requests
import time

from typing import Any
from typing import Optional

import config
import osu_types

from light_beatmap_parser import LightBeatmapParser

REQUEST_SESSION = requests.Session()


def seconds_to_time_stamp_string(seconds: int) -> str:
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def is_valid_status_code(status_code: int) -> bool:
    return status_code in range(200, 300)


def request_osu_api_v1(
    path: str,
    parameters: dict[str, Any],
) -> None | list[dict[str, Any]]:
    if path.startswith("/"):
        path = path.removeprefix("/")

    response = REQUEST_SESSION.get(
        f"https://osu.ppy.sh/api/{path}",
        params=parameters,
    )

    if not is_valid_status_code(response.status_code):
        return None

    json_response = response.json()
    if not json_response:
        return None

    return json_response


def get_recent_play_from_user_name(
    osu_user_name: str,
    osu_mode: int,
) -> Optional[osu_types.RecentScore]:
    recent_plays = request_osu_api_v1(
        path="/get_user_recent",
        parameters={
            "k": config.osu_api_v1_key,
            "u": osu_user_name,
            "m": osu_mode,
            "type": "string",
        },
    )

    if not recent_plays:
        return None

    most_recent_play = recent_plays[0]
    return most_recent_play  # type: ignore


def get_beatmap_from_id(
    beatmap_id: str,
    osu_mode: int,
) -> Optional[osu_types.Beatmap]:
    beatmaps = request_osu_api_v1(
        path="/get_beatmaps",
        parameters={"k": config.osu_api_v1_key, "b": beatmap_id, "m": osu_mode},
    )

    if not beatmaps:
        return None

    return beatmaps[0]  # type: ignore


def get_beatmap_content_from_id(
    beatmap_id: str,
) -> Optional[str]:
    response = REQUEST_SESSION.get(f"https://osu.ppy.sh/osu/{beatmap_id}")

    if not is_valid_status_code(response.status_code):
        return None

    return response.text


def main() -> int:
    current_time_passed: int = 0
    last_recent_score: Optional[osu_types.RecentScore] = get_recent_play_from_user_name(
            config.osu_user_name,
            config.osu_mode,
        )

    print("Timer has started!")

    while True:
        time.sleep(5)

        most_recent_play = get_recent_play_from_user_name(
            config.osu_user_name,
            config.osu_mode,
        )

        if most_recent_play == last_recent_score:
            continue

        if most_recent_play is None:
            continue

        beatmap = get_beatmap_from_id(
            most_recent_play["beatmap_id"],
            config.osu_mode,
        )

        if not beatmap:
            continue

        completed_map = most_recent_play["rank"] != "F"

        if completed_map:
            current_time_passed += int(beatmap["total_length"])
        else:
            beatmap_file = get_beatmap_content_from_id(beatmap["beatmap_id"])

            if not beatmap_file:
                continue

            beatmap_parser = LightBeatmapParser(beatmap_file)
            beatmap_parser.parse_hit_objects_data()
            assert beatmap_parser.hit_objects

            total_objects_seen = (
                int(most_recent_play["count300"])
                + int(most_recent_play["count100"])
                + int(most_recent_play["count50"])
                + int(most_recent_play["countmiss"])
            )

            map_progress = total_objects_seen / len(beatmap_parser.hit_objects)
            current_time_passed += round(int(beatmap["total_length"]) * map_progress)

        last_recent_score = most_recent_play

        print(
            "Time spent playing maps since the program's launch:",
            seconds_to_time_stamp_string(current_time_passed),
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
