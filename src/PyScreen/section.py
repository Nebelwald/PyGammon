from enum import Enum
from itertools import chain


class Alignment(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Style(Enum):
    INVISIBLE = "invisible"
    SINGLE = "single"
    DOUBLE = "double"


class ContentSection:
    sections = []

    @property
    def head(self):
        return self._head

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def preferred_width(self):
        return self._preferred_width

    @property
    def preferred_height(self):
        return self._preferred_height

    @staticmethod
    def get_scrollable_sections():
        return [section for section in ContentSection.sections if section.is_scrollable]

    @property
    def is_scrollable(self):
        return (True
                if self._scrollable[Orientation.VERTICAL] or self._scrollable[Orientation.HORIZONTAL]
                else False)

    @staticmethod
    def reset_sections():
        ContentSection.sections = []

    def __init__(self, content, width: int, height: int,
                 head="",
                 margin=0, border=0, padding=0,
                 alignment_vertical=Alignment.TOP, alignment_horizontal=Alignment.LEFT,
                 orientation=Orientation.VERTICAL, scrollable=None,
                 auto_split_content=False):
        def preprocess_margin_or_padding_or_border(my_list, allowed_range=None) -> dict:
            match my_list:
                case int():
                    my_list = [my_list]
                case list():
                    my_list = my_list
                case _:
                    raise TypeError(f"The value '{my_list}' is not allowed for margin, border or padding.")

            if allowed_range:
                for value in my_list:
                    if value not in allowed_range:
                        raise TypeError(f"The value '{value}' is not allowed for margin, border or padding.")

            if len(my_list) == 1:
                my_list = my_list * 4
            elif len(my_list) == 2:
                my_list = my_list * 2

            return {
                Direction.LEFT: my_list[0],
                Direction.BOTTOM: my_list[1],
                Direction.RIGHT: my_list[2],
                Direction.TOP: my_list[3]
            }

        self._content = content

        self._margin = preprocess_margin_or_padding_or_border(margin)
        self._border = preprocess_margin_or_padding_or_border(border, range(0, 2))
        self._padding = preprocess_margin_or_padding_or_border(padding)

        match scrollable:
            case None:
                scrollable = [False, False]
            case bool():
                scrollable = [scrollable] * 2
            case list():
                scrollable = scrollable
            case _:
                raise TypeError(f"The value '{scrollable}' is not allowed for scrollable.")

        self._scrollable = {
            Orientation.HORIZONTAL: scrollable[0],
            Orientation.VERTICAL: scrollable[1]
        }

        if scrollable[0] or scrollable[1]:
            alignment_vertical = Alignment.TOP
            # TODO: add scrollbars (-1 for width or/and height, calculate percentage of scroll, make bar with "."/"o")

        self._offset_horizontal = 0
        self._offset_vertical = 0

        self._preferred_width, self._preferred_height = self.get_preferred_width_and_height()

        # TODO: autosplit and preferred width/height schließen sich gegenseitig aus! preferred height muss nach autoplit
        #  ermittelt werden!
        # idee: erst preffered width berechnen, dann autosplitten, dann preffered height berechnen.

        self._width = self.preferred_width if width == -1 else width  # ToDo: maybe make enum for -1 and "*"
        self._height = self._preferred_height if height == -1 else height

        self._alignment_vertical = alignment_vertical
        self._alignment_horizontal = alignment_horizontal

        self._orientation = orientation

        ContentSection.sections.append(self)

        self._head = head

        self.__auto_split_content = auto_split_content

    def get_preferred_width_and_height(self):
        return (self._calculate_preferred_width_or_height(max([len(line) for line in self._content]),
                                                          Direction.LEFT, Direction.RIGHT),
                self._calculate_preferred_width_or_height(len(self._content),
                                                          Direction.TOP, Direction.BOTTOM))

    def _calculate_preferred_width_or_height(self, content_width_or_height, direction_one, direction_two):
        margin_direction_one = self._margin[direction_one]
        margin_direction_two = self._margin[direction_two]
        border_direction_one = int(self._border[direction_one])
        border_direction_two = int(self._border[direction_two])
        padding_direction_one = self._padding[direction_one]
        padding_direction_two = self._padding[direction_two]

        calculated_value = (content_width_or_height +
                            margin_direction_one +
                            margin_direction_two +
                            border_direction_one +
                            border_direction_two +
                            padding_direction_one +
                            padding_direction_two)
        return calculated_value

    def scroll(self, value, scroll_orientation) -> None:
        if scroll_orientation == Orientation.VERTICAL:
            self._offset_vertical += value
            print(self._offset_vertical)
            print(self)
        else:  # scroll_orientation == Orientation.HORIZONTAL
            self._offset_horizontal += value

    def _get_scrollable_length(self, orientation: Orientation, number_of_remaining_characters: int):
        if orientation == Orientation.VERTICAL:
            return len(self._content) - number_of_remaining_characters
        else:  # orientation == Orientation.HORIZONTAL
            return len(" ".join(self._content)) - number_of_remaining_characters

    def reset_scroll(self) -> None:
        self._offset_vertical = 0
        self._offset_horizontal = 0

    def transform(self, width_with_margin: int, height_with_margin: int) -> list:
        def subtract_padding_or_margin_from_width_and_height(value_set, width, height):
            return (width - value_set[Direction.LEFT] - value_set[Direction.RIGHT],
                    height - value_set[Direction.TOP] - value_set[Direction.BOTTOM])

        width_with_border, height_with_border = \
            subtract_padding_or_margin_from_width_and_height(self._margin,
                                                             width_with_margin,
                                                             height_with_margin)
        width_with_padding, height_with_padding = \
            subtract_padding_or_margin_from_width_and_height(self._border,
                                                             width_with_border,
                                                             height_with_border)
        width_content, height_content = \
            subtract_padding_or_margin_from_width_and_height(self._padding,
                                                             width_with_padding,
                                                             height_with_padding)

        content = (self.__automatically_split_content(self._content, width_content)
                   if self.__auto_split_content and isinstance(self._content, str)
                   else self._content)

        content = self._orientate_content(content, width_content, height_content)

        if self._scrollable:
            content = self._scroll_content(content, width_content, height_content)

        content = self._align_content_vertical(content, self._alignment_vertical, width_content, height_content)
        content = self._align_content_horizontal(content, self._alignment_horizontal, width_content)

        content = self._add_margin_or_padding(content, width_content, self._padding)
        content = self._add_border_to_content(content, width_with_border)
        content = self._add_margin_or_padding(content, width_with_border, self._margin)

        return content

    @staticmethod
    def __automatically_split_content(content: str, content_width: int):
        def process_paragraph(paragraph: str) -> list:
            content_elements = paragraph.split(" ")
            split_paragraph = []
            new_line = ""

            for word in content_elements:
                if len(f"{new_line} {word}") > content_width:
                    split_paragraph.append(new_line)
                    new_line = word
                else:
                    new_line = f"{new_line} {word}" if new_line else f"{word}"

            split_paragraph.append(new_line)
            return split_paragraph

        paragraphs = content.split("\\n")
        split_content = []

        for paragraph in paragraphs:
            split_paragraph = process_paragraph(paragraph)
            split_content += split_paragraph

        return split_content

    def _orientate_content(self, content: list, width_content: int, height_content: int) -> list:
        match self._orientation:
            case Orientation.VERTICAL:
                return content
            case Orientation.HORIZONTAL:
                return [" ".join(content)]

    def _scroll_content(self, content: list, width_content: int, height_content: int) -> list:
        number_of_remaining_characters = 1

        if self._scrollable[Orientation.VERTICAL]:
            start_index = max(0, min(len(content) - number_of_remaining_characters, self._offset_vertical))
            end_index = height_content + start_index

            content = content[start_index:end_index]

        if self._scrollable[Orientation.HORIZONTAL]:
            max_content_length = max([len(line) for line in content])

            start_index = max(0, min(max_content_length - number_of_remaining_characters, self._offset_horizontal))
            end_index = width_content + start_index

            content = [line[start_index:end_index]
                       for line in content]

        return content

    @staticmethod
    def _align_content_vertical(content: list, alignment: Alignment, width_content: int, height_content: int) -> list:
        def _create_empty_lines(count):
            return [" " * width_content for _ in range(count)]

        empty_lines_count = max(0, height_content - len(content))

        if alignment == Alignment.TOP:
            content = content + _create_empty_lines(empty_lines_count)

        elif alignment == Alignment.BOTTOM:
            content = _create_empty_lines(empty_lines_count) + content

        else:  # if alignment == Alignment.CENTER:
            empty_lines_top = empty_lines_count // 2
            content = (_create_empty_lines(empty_lines_top) +
                       content +
                       _create_empty_lines(empty_lines_count - empty_lines_top))

        return content[:height_content]

    def _align_content_horizontal(self, content: list, alignment: Alignment, width_content: int) -> list:
        return [self._align_line_horizontal(line, alignment, width_content)
                for line in content]

    @staticmethod
    def _align_line_horizontal(line: str, alignment: Alignment, width_content: int) -> str:
        if alignment == Alignment.LEFT:
            aligned_content = line.ljust(width_content)
        elif alignment == Alignment.RIGHT:
            aligned_content = line.rjust(width_content)
        else:  # if alignment == Alignment.CENTER:
            aligned_content = line.center(width_content)

        return aligned_content[:width_content]

    @staticmethod
    def _add_margin_or_padding(content, width_content: int, value_set: dict) -> list:
        def add_margin_or_padding_vertical():
            return ([" " * width_content for _ in range(value_top)] +
                    content +
                    [" " * width_content for _ in range(value_bottom)])

        def add_margin_padding_horizontal():
            return [(" " * value_left) + line + (" " * value_right)
                    for line in content]

        value_left = value_set[Direction.LEFT]
        value_bottom = value_set[Direction.BOTTOM]
        value_right = value_set[Direction.RIGHT]
        value_top = value_set[Direction.TOP]

        content = add_margin_or_padding_vertical()
        content = add_margin_padding_horizontal()
        return content

    def _add_border_to_content(self, content: list, available_width: int) -> list:
        def create_border_top_bottom_line(head_or_foot,
                                          border_symbol_horizontal,
                                          border_symbol_corner_left, border_symbol_corner_right,
                                          border_separator_symbol_left, border_separator_symbol_right) -> str:
            count_border_edges_characters = 2
            header_or_footer_width = count_border_edges_characters + 4

            insertion = (f"{border_separator_symbol_left} "
                         f"{head_or_foot[:available_width - header_or_footer_width]} "
                         f"{border_separator_symbol_right}"
                         if head_or_foot
                         else border_symbol_horizontal)
            insertion = insertion.center(available_width - count_border_edges_characters, border_symbol_horizontal)

            return ((border_symbol_corner_left if is_border_left else border_symbol_horizontal) +
                    insertion +
                    (border_symbol_corner_right if is_border_right else border_symbol_horizontal))

        is_border_left = self._border[Direction.LEFT]
        is_border_bottom = self._border[Direction.BOTTOM]
        is_border_right = self._border[Direction.RIGHT]
        is_border_top = self._border[Direction.TOP]

        (border_symbol_left, border_symbol_bottom, border_symbol_right, border_symbol_top,
         border_symbol_left_top, border_symbol_left_bottom,
         border_symbol_right_bottom, border_symbol_right_top,
         border_symbol_head_left, border_symbol_head_right,
         border_symbol_foot_left, border_symbol_foot_right) = self._get_border_symbols()

        content = [(border_symbol_left if is_border_left else "") +
                   line +
                   (border_symbol_right if is_border_right else "")
                   for line in content]

        if is_border_top:
            border_top_line = create_border_top_bottom_line(self._head, border_symbol_top,
                                                            border_symbol_left_top, border_symbol_right_top,
                                                            border_symbol_head_left, border_symbol_head_right)
            content = [border_top_line] + content

        if is_border_bottom:
            # TODO: decide if to dot something with "foot"
            border_bottom_line = create_border_top_bottom_line("", border_symbol_bottom,
                                                               border_symbol_left_bottom, border_symbol_right_bottom,
                                                               border_symbol_foot_left, border_symbol_foot_right)
            content = content + [border_bottom_line]

        return content

    def _get_border_symbols(self) -> (str, str, str, str, str, str, str, str, str, str):
        """ Returns a tuple for the border symbols (left, bottom, right, top,
        left top, left bottom, right bottom, right top,
        head seperator left, head seperator right, foot seperator left, foot seperator right). """

        none = ["" for _ in range(8)]
        single = ["│", "─", "╭", "╰", "╯", "╮", "┤", "├"]

        def get_list_by_value(value):
            if value == 0:
                return none
            if value == 1:
                return single

        left = get_list_by_value(self._border[Direction.LEFT])[0]
        bottom = get_list_by_value(self._border[Direction.BOTTOM])[1]
        right = get_list_by_value(self._border[Direction.RIGHT])[0]
        top = get_list_by_value(self._border[Direction.TOP])[1]

        # TODO: only "│" or "─" if left/right or top/bottom is none or invisible
        left_top = get_list_by_value(
            min(self._border[Direction.LEFT], self._border[Direction.TOP])
        )[2]
        left_bottom = get_list_by_value(
            min(self._border[Direction.LEFT], self._border[Direction.BOTTOM])
        )[3]

        right_bottom = get_list_by_value(
            min(self._border[Direction.RIGHT], self._border[Direction.BOTTOM])
        )[4]
        right_top = get_list_by_value(
            min(self._border[Direction.RIGHT], self._border[Direction.TOP])
        )[5]

        head_separator_left = get_list_by_value(self._border[Direction.TOP])[6]
        head_separator_right = get_list_by_value(self._border[Direction.TOP])[7]

        foot_separator_left = get_list_by_value(self._border[Direction.BOTTOM])[6]
        foot_separator_right = get_list_by_value(self._border[Direction.BOTTOM])[7]

        return (left, bottom, right, top, left_top, left_bottom, right_bottom, right_top,
                head_separator_left, head_separator_right, foot_separator_left, foot_separator_right)


class Section(ContentSection):
    def get_preferred_width_and_height(self):
        preferred_width, preferred_height = 0, 0
        for section in self._content:
            section_preferred_width, section_preferred_height = section.get_preferred_width_and_height()
            preferred_width += section_preferred_width
            preferred_height += section_preferred_height

        # TODO: rework! depending on orientation, width/height must not be the sum, but the max()

        return (self._calculate_preferred_width_or_height(preferred_width, Direction.LEFT, Direction.RIGHT),
                self._calculate_preferred_width_or_height(preferred_height, Direction.TOP, Direction.BOTTOM))

    def _get_scrollable_length(self, orientation: Orientation, number_of_remaining_characters: int):
        if orientation == Orientation.VERTICAL:
            return len(self._content) - number_of_remaining_characters
        else:  # orientation == Orientation.HORIZONTAL
            return len(" ".join(self._content)) - number_of_remaining_characters

    def _orientate_content(self, sections_raw: list, width_content: int, height_content: int) -> list:
        content = []

        sections_transformed = self._preprocess_children(sections_raw, width_content, height_content)

        if self._orientation == Orientation.VERTICAL:
            for section in sections_transformed:
                content += section

        else:  # orientation == Orientation.HORIZONTAL
            max_section_height = max(len(section) for section in sections_transformed)
            sections_transformed_aligned = []

            for section in sections_transformed:
                missing_lines = max_section_height - len(section)
                section_width = len(section[0])
                section = section + [" " * section_width for _ in range(missing_lines)]
                sections_transformed_aligned.append(section)

            content_zipped = list(zip(*chain(sections_transformed_aligned)))
            for zipped_contents in content_zipped:
                content.append("".join(zipped_contents))

        return content

    def _preprocess_children(self, sections_raw: list, width_content: int, height_content: int) -> list:
        error_code_star = -1
        stars_height, stars_width = self._get_stars_width_and_height(sections_raw, width_content, height_content,
                                                                     error_code_star)
        sections_transformed = []

        for section in sections_raw:
            section_width = self._calculate_section_width_or_height(section.width, section.preferred_width,
                                                                    width_content, Orientation.HORIZONTAL,
                                                                    stars_width, error_code_star)
            section_height = self._calculate_section_width_or_height(section.height, section.preferred_height,
                                                                     height_content, Orientation.VERTICAL,
                                                                     stars_height, error_code_star)

            sections_transformed.append(section.transform(section_width, section_height))

        return sections_transformed

    def _get_stars_width_and_height(self, sections_raw: list, width_content: int, height_content: int,
                                    error_code_star: int) -> (int, int):
        static_width, static_height, stars_width_count, stars_height_count = \
            self._get_static_width_and_height_and_stars_counts(sections_raw, width_content, height_content,
                                                               error_code_star)
        if self._orientation is Orientation.VERTICAL:
            stars_height = max(0, (height_content - static_height) // max(1, stars_height_count))
            stars_width = width_content
        else:  # orientation == Orientation.HORIZONTAL
            stars_height = height_content
            stars_width = max(0, (width_content - static_width) // max(1, stars_width_count))
        return stars_height, stars_width

    def _get_static_width_and_height_and_stars_counts(self, sections_raw: list, parent_width: int, parent_height: int,
                                                      error_code_star: int) -> (int, int, int, int):
        static_width = sum([self._get_section_width_or_height_value(section.width, parent_width, error_code_star)
                            for section in sections_raw
                            if section.width != "*"])
        static_height = sum([self._get_section_width_or_height_value(section.height, parent_height, error_code_star)
                             for section in sections_raw
                             if section.height != "*"])

        stars_width_count = len([section for section in sections_raw if section.width == "*"])
        stars_height_count = len([section for section in sections_raw if section.height == "*"])

        return static_width, static_height, stars_width_count, stars_height_count

    @staticmethod
    def _get_section_width_or_height_value(value, parent_value: int, error_code_star: int) -> int:
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(parent_value * value)

        if value == "*":
            return error_code_star

        raise ValueError("Value must be int or float")

    def _calculate_section_width_or_height(self, section_width_or_height_value, section_preferred_value,
                                           width_or_height_value, orientation, star_value, error_code_star):
        if self._scrollable[orientation]:
            return section_preferred_value

        calculated_section_width_or_height = (
            self._get_section_width_or_height_value(section_width_or_height_value, width_or_height_value,
                                                    error_code_star))

        return (star_value
                if calculated_section_width_or_height == error_code_star
                else calculated_section_width_or_height)
