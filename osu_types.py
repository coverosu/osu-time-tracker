from typing import TypedDict

# TODO: use pydantic models?


class RecentScore(TypedDict):
    beatmap_id: str
    score: str
    maxcombo: str
    count50: str
    count100: str
    count300: str
    countmiss: str
    countkatu: str
    countgeki: str
    perfect: str
    enabled_mods: str
    user_id: str
    date: str
    rank: str


class Beatmap(TypedDict):
    approved: str
    submit_date: str
    approved_date: str
    last_update: str
    artist: str
    beatmap_id: str
    beatmapset_id: str
    bpm: str
    creator: str
    creator_id: str
    difficultyrating: str
    diff_aim: str
    diff_speed: str
    diff_size: str
    diff_overall: str
    diff_approach: str
    diff_drain: str
    hit_length: str
    source: str
    genre_id: str
    language_id: str
    title: str
    total_length: str
    version: str
    file_md5: str
    mode: str
    tags: str
    favourite_count: str
    rating: str
    playcount: str
    passcount: str
    count_normal: str
    count_slider: str
    count_spinner: str
    max_combo: str
    storyboard: str
    video: str
    download_unavailable: str
    audio_unavailable: str
