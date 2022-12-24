from typing import Union

from pydantic import BaseModel
from pydantic.color import Color
from pydantic import Field


class ColorsModel(BaseModel):
    combos: dict[str, Color]


class DifficultyModel(BaseModel):
    hp_drain_rate: Union[int, float]
    circle_size: Union[int, float]
    overall_difficulty: Union[int, float]
    approach_rate: Union[int, float]
    slider_multiplier: Union[int, float]
    slider_tick_rate: Union[int, float]


class EditorModel(BaseModel):
    bookmarks: list[int] = Field(..., min_items=1)
    distance_spacing: int
    beat_divisor: int
    grid_size: int


class GeneralModel(BaseModel):
    audio_filename: str
    audio_lead_in: int
    preview_time: int
    countdown: int
    sample_set: str
    stack_leniency: float
    mode: int
    letterbox_in_breaks: int


class MetaDataModel(BaseModel):
    title: str
    artist: str
    creator: str
    version: str
    source: str
    tags: list[str] = Field(..., min_items=1)
