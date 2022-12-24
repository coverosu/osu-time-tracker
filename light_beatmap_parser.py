"""
This is a update from my old ass package called 'coover'
"""

from typing import Any
from functools import cached_property
from enum import IntEnum
from typing import Optional
from pathlib import Path
from typing import Union

from beatmap_models import ColorsModel
from beatmap_models import DifficultyModel
from beatmap_models import EditorModel
from beatmap_models import GeneralModel
from beatmap_models import MetaDataModel


class LabelParsingType(IntEnum):
    KEY_VALUE = 1
    SPLIT_BY_COMMA = 2
    SPLIT_BY_PIPE = 3


def split_by_caps(s: str) -> list[str]:
    result = []
    acc = []
    for c in s:
        if c.isupper():
            result.append("".join(acc))
            acc = []
        acc.append(c)
    result.append("".join(acc))
    return [x for x in result if x]


def camel_to_snake(camel_name: str) -> str:
    snake_case = []

    if camel_name.startswith("HP"):
        snake_case.append("hp")
        camel_name = camel_name.replace("HP", "")

    for word in split_by_caps(camel_name):
        snake_case.append(word.lower())

    return "_".join(snake_case)


class LightBeatmapParser:
    def __init__(self, osu_map_content: str) -> None:
        self.osu_map_content = osu_map_content
        self.osu_file_format_version: Optional[int] = None
        self.general: Optional[GeneralModel] = None
        self.editor: Optional[EditorModel] = None
        self.colors: Optional[ColorsModel] = None
        self.meta_data: Optional[MetaDataModel] = None
        self.events: Optional[list[list[str]]] = None
        self.timing_points: Optional[list[list[str]]] = None
        self.difficulty: Optional[DifficultyModel] = None
        self.hit_objects: Optional[list[list[str]]] = None

    @cached_property
    def content_split(self) -> list[str]:
        return self.osu_map_content.splitlines()

    def parse_data_as_key_value(self, data: str, label: str) -> dict[str, Any]:
        data_as_dictionary = {}
        key, value = data.split(":")
        key = key.strip()
        value = value.strip()
        if not key:
            breakpoint()  # TODO: can the key be blank?

        key_snake_case = camel_to_snake(key)

        if label == "[Metadata]" and key == "Tags":
            data_as_dictionary[key_snake_case] = value.split(" ")
        elif label == "[General]" and key == "Mode":
            data_as_dictionary[key_snake_case] = int(value)
        elif label == "[Editor]" and key == "Bookmarks":
            data_as_dictionary[key_snake_case] = value.split(",")
        elif label == "[Colours]":
            data_as_dictionary[key_snake_case] = f"rgb({value.replace(',', ', ')})"
        else:
            data_as_dictionary[key_snake_case] = value

        return data_as_dictionary

    def parse_from_label(self, label: str, parsing_type: LabelParsingType) -> list[Any]:
        label_index = self.content_split.index(label)
        list_of_label_data = self.content_split[label_index + 1 :]
        list_of_label_data_striped = [
            label_data.strip() for label_data in list_of_label_data
        ]

        parsed_data: list[Any] = []
        for label_data in list_of_label_data_striped:
            if label_data.startswith("["):
                break  # this hits another label so stop parsing

            if label_data == "":
                continue  # no data, skip line

            if label_data.startswith("//"):
                continue  # comment, skip line
            elif "//" in label_data:
                breakpoint()  # TODO: can there be comments after valid data?
                continue

            if parsing_type == LabelParsingType.KEY_VALUE:
                parsed_data.append(
                    self.parse_data_as_key_value(label_data, label),
                )
                continue
            elif parsing_type == LabelParsingType.SPLIT_BY_COMMA:
                parsed_data.append(
                    label_data.split(","),
                )
            elif parsing_type == LabelParsingType.SPLIT_BY_PIPE:
                parsed_data.append(
                    label_data.split("|"),
                )

        return parsed_data

    def parse_meta_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[Metadata]",
            LabelParsingType.KEY_VALUE,
        )
        full_data = {}
        for dictionary in parsed_data:
            full_data.update(dictionary)

        self.meta_data = MetaDataModel(**full_data)

    def parse_general_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[General]",
            LabelParsingType.KEY_VALUE,
        )
        full_data = {}
        for dictionary in parsed_data:
            full_data.update(dictionary)

        self.general = GeneralModel(**full_data)

    def parse_event_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[Events]",
            LabelParsingType.SPLIT_BY_COMMA,
        )
        self.events = parsed_data

    def parse_timing_point_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[TimingPoints]",
            LabelParsingType.SPLIT_BY_COMMA,
        )
        self.timing_points = parsed_data

    def parse_difficulty_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[Difficulty]",
            LabelParsingType.KEY_VALUE,
        )
        full_data = {}
        for dictionary in parsed_data:
            full_data.update(dictionary)

        self.difficulty = DifficultyModel(**full_data)

    def parse_editor_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[Editor]",
            LabelParsingType.KEY_VALUE,
        )
        full_data = {}
        for dictionary in parsed_data:
            full_data.update(dictionary)

        self.editor = EditorModel(**full_data)

    def parse_combo_color_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[Colours]",
            LabelParsingType.KEY_VALUE,
        )
        full_data = {}
        for dictionary in parsed_data:
            full_data.update(dictionary)

        self.colors = ColorsModel(combos=full_data)

    def parse_hit_objects_data(self) -> None:
        parsed_data = self.parse_from_label(
            "[HitObjects]",
            LabelParsingType.SPLIT_BY_PIPE,
        )
        self.hit_objects = parsed_data

    def parse_full_file(self) -> None:
        self.parse_meta_data()
        self.parse_difficulty_data()
        self.parse_general_data()
        self.parse_editor_data()
        self.parse_event_data()
        self.parse_timing_point_data()
        self.parse_combo_color_data()
        self.parse_hit_objects_data()

    @classmethod
    def from_path(cls, path: Union[str, Path]) -> "LightBeatmapParser":
        if isinstance(path, str):
            with open(path) as f:
                return cls(f.read())
        else:
            return cls(path.read_text())

    @classmethod
    def from_file_content(cls, content: str) -> "LightBeatmapParser":
        return cls(content)
