import re
from os import system, name as os_name
from os.path import join

from PyScreen.parser import Parser
from PyScreen.section import ContentSection, Orientation

IS_MS_WINDOWS = os_name == "nt"


class Screen:
    __width = 100
    __height = 20
    __prompt = "[ PyScreen ]"
    __title = "PyScreen"

    _ADDITIONAL_SCREEN_HEIGHT = 1

    __views_path = str()

    def __init__(self, view_file_path):
        ContentSection.reset_sections()
        self.__view_file_path = view_file_path

    @staticmethod
    def set_size(width, height):
        Screen.__width = width + Screen._ADDITIONAL_SCREEN_HEIGHT
        Screen.__height = height

    @staticmethod
    def set_view_paths(views_path):
        Screen.__views_path = views_path

    @staticmethod
    def set_title(new_title):
        Screen.__title = new_title

    @staticmethod
    def set_prompt(new_prompt):
        Screen.__prompt = new_prompt

    def display(self, databinding, prompt=None, title=None, skip_user_input=False):
        content = Parser().parse_file(join(Screen.__views_path, self.__view_file_path), databinding)

        def configure_screen():
            command_set_size = (
                f"mode con cols={Screen.__width} lines={Screen.__height}"
                if IS_MS_WINDOWS
                else f"resize -s {Screen.__height} {Screen.__width}")
            command_set_title = f'echo -ne "\033]0;{title}\007"'

            system(command_set_size)
            system(command_set_title)
            self.clear_console()

        prompt = prompt if prompt else Screen.__prompt
        title = title if title else Screen.__title

        while True:
            configure_screen()

            for line in content.transform(self.__width, self.__height - self._ADDITIONAL_SCREEN_HEIGHT):
                print(line)

            if skip_user_input:
                return

            user_input = input(prompt).strip()
            if not self.__scroll_section(user_input):
                return user_input

    @staticmethod
    def clear_console() -> None:
        system("cls") if IS_MS_WINDOWS else system("clear")

    @staticmethod
    def __scroll_section(user_input) -> bool:
        def reset_scroll():
            for section in ContentSection.sections:
                section.reset_scroll()

        def scroll_sections(user_input):
            input_list = user_input.split(" ")
            selected_section_id, scroll_orientation, scroll_width = input_list[1], input_list[2], int(input_list[3])
            # TODO: make v default to allow user to skip orientation

            for section in ContentSection.get_scrollable_sections():
                if selected_section_id.lower() in section.head.lower():
                    scroll_orientation = Orientation.VERTICAL if scroll_orientation == "v" else Orientation.HORIZONTAL
                    section.scroll(scroll_width,
                                   scroll_orientation)
                    return was_pyscreen_command_performed

            return not was_pyscreen_command_performed

        # TODO: rework commands. put something like ps ("pyscreen") at beginning
        was_pyscreen_command_performed = True

        if user_input == "sr":
            reset_scroll()
            return was_pyscreen_command_performed

        pyscreen_command_pattern = "s [0-9a-zA-z]+ [vh] [+-]?[0-9]+"
        if not re.search(pyscreen_command_pattern, user_input):
            return not was_pyscreen_command_performed

        was_pyscreen_command_performed = scroll_sections(user_input)
        return was_pyscreen_command_performed
