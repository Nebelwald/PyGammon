import json

import yaml

from PyScreen.section import Section, Alignment, Orientation, ContentSection


class Parser:
    def parse_file(self, file_path: str, databinding: dict) -> Section:
        content_object = self._load_file_content(file_path)

        if not isinstance(content_object, dict):
            raise TypeError(f"The file extension {type(content_object)} is not supported.")

        main_section = self._parse_json_object(content_object, databinding)
        return main_section

    @staticmethod
    def _load_file_content(file_path: str):
        file_extension = file_path[file_path.rfind(".") + 1:]

        content_object = None
        with open(file_path, "r") as file:
            match file_extension:
                case "json":
                    content_object = json.load(file)
                case "yaml":
                    content_object = yaml.safe_load(file)
                case _:
                    raise TypeError(f"The file extension {file_extension} is not supported.")

        return content_object

    def _parse_json_object(self, json_object: dict, databinding: dict, sections_tree_depth=0):
        def transform_alignment_border_orientation(value, enum_to_match, match_assign_pairs):
            for value_to_match, value_to_assign in match_assign_pairs:
                if value == value_to_match:
                    return value_to_assign

            if isinstance(value, enum_to_match):
                return value

            raise TypeError(f"'{value}' is not a valid value for alignment/border")

        content = json_object["content"]

        width = json_object.get("width", "*")
        height = json_object.get("height", "*")

        head = json_object.get("head", "")
        head = databinding.get(head, head)

        # TODO: maybe get more attributes from databinding

        margin = json_object.get("margin", 0)
        border = json_object.get("border", False)
        padding = json_object.get("padding", 0)

        alignment_vertical = json_object.get("alignment_vertical", Alignment.TOP)
        alignment_vertical = transform_alignment_border_orientation(alignment_vertical, Alignment, tuple([
            tuple([Alignment.TOP.value, Alignment.TOP]),
            tuple([Alignment.CENTER.value, Alignment.CENTER]),
            tuple([Alignment.BOTTOM.value, Alignment.BOTTOM]),
        ]))

        alignment_horizontal = json_object.get("alignment_horizontal", Alignment.LEFT)
        alignment_horizontal = transform_alignment_border_orientation(alignment_horizontal, Alignment, tuple([
            tuple([Alignment.LEFT.value, Alignment.LEFT]),
            tuple([Alignment.CENTER.value, Alignment.CENTER]),
            tuple([Alignment.RIGHT.value, Alignment.RIGHT]),
        ]))

        orientation = json_object.get("orientation",
                                      Orientation.HORIZONTAL
                                      if sections_tree_depth % 2 == 0 and isinstance(content, list)
                                      else Orientation.VERTICAL)
        orientation = transform_alignment_border_orientation(orientation, Orientation, tuple([
            tuple([Orientation.VERTICAL.value, Orientation.VERTICAL]),
            tuple([Orientation.HORIZONTAL.value, Orientation.HORIZONTAL])
        ]))

        scrollable = json_object.get("scrollable", False)
        auto_split_content = json_object.get("auto_split", False)

        match content:
            case list():
                return self._parse_section(json_object, databinding, sections_tree_depth,
                                           width, height,
                                           head,
                                           margin, border, padding,
                                           alignment_vertical, alignment_horizontal,
                                           orientation,
                                           scrollable)

            case str():
                return self._parse_content_section(content, databinding,
                                                   width, height,
                                                   head,
                                                   margin, border, padding,
                                                   alignment_vertical, alignment_horizontal,
                                                   orientation,
                                                   scrollable,
                                                   auto_split_content)
            case _:
                raise TypeError(f"'{type(content)}' is not an valid type for a section content.")

    def _parse_section(self, json_object, databinding, sections_tree_depth,
                       width, height,
                       head,
                       margin, border, padding,
                       alignment_vertical, alignment_horizontal,
                       orientation,
                       scrollable) -> Section:

        section_content = [self._parse_json_object(child_object, databinding, sections_tree_depth + 1)
                           for child_object in json_object["content"]]

        return Section(section_content,
                       width, height,
                       head=head,
                       margin=margin, border=border, padding=padding,
                       alignment_vertical=alignment_vertical, alignment_horizontal=alignment_horizontal,
                       orientation=orientation,
                       scrollable=scrollable)

    @staticmethod
    def _parse_content_section(content, databinding,
                               width, height,
                               head,
                               margin, border, padding,
                               alignment_vertical, alignment_horizontal,
                               orientation,
                               scrollable, auto_split_content) -> ContentSection:

        content = databinding.get(content, content)

        content = content.split("\n") if "\n" in content else content
        # todo: necessary? could be covered by auto-split

        content = [content] if isinstance(content, str) and not auto_split_content else content
        # TODO: maybe better in section? /\

        return ContentSection(content,
                              width, height,
                              head=head,
                              margin=margin, border=border, padding=padding,
                              alignment_vertical=alignment_vertical, alignment_horizontal=alignment_horizontal,
                              orientation=orientation,
                              scrollable=scrollable,
                              auto_split_content=auto_split_content)
