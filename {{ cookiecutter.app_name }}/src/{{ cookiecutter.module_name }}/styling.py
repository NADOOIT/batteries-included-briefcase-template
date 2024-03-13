import sys
from toga.style import Pack

class StandardStyling:
    @staticmethod
    def _get_style_for_platform():
        if sys.platform == "win32":
            # Windows styles
            return {
                "standard_label_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=25, font_size=7),
                "standard_input_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=25, font_size=15),
                "standard_selection_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=30, font_size=15),
                "standard_button_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=30, font_size=7),
                "standard_switch_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=30, font_size=7),
                "standard_highlighted_input_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=25, font_size=15, background_color="red"),
            }
        elif sys.platform == "darwin":
            # macOS styles
            return {
                "standard_label_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=25, font_size=15),
                "standard_input_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=30, font_size=17),
                "standard_selection_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=30, font_size=16),
                "standard_button_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=30, font_size=9),
                "standard_switch_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=30, font_size=9),
                "standard_highlighted_input_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=30, font_size=17, background_color="blue"),
                "standard_box_style": Pack(flex=1, padding_top=12, padding_bottom=12, height=30, font_size=17),
            }
        elif sys.platform == "linux":
            # Linux styles
            return {
                "standard_label_style": Pack(flex=1, padding_top=11, padding_bottom=11, height=25, font_size=8),
                "standard_input_style": Pack(flex=1, padding_top=11, padding_bottom=11, height=25, font_size=16),
                "standard_selection_style": Pack(flex=1, padding_top=11, padding_bottom=11, height=30, font_size=16),
                "standard_button_style": Pack(flex=1, padding_top=11, padding_bottom=11, height=30, font_size=8),
                "standard_switch_style": Pack(flex=1, padding_top=11, padding_bottom=11, height=30, font_size=8),
                "standard_highlighted_input_style": Pack(flex=1, padding_top=11, padding_bottom=11, height=25, font_size=16, background_color="green"),
            }
        else:
            # Default styles for any other platform
            return {
                "standard_label_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=25, font_size=7),
                "standard_input_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=25, font_size=15),
                "standard_selection_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=30, font_size=15),
                "standard_button_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=30, font_size=7),
                "standard_switch_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=30, font_size=7),
                "standard_highlighted_input_style": Pack(flex=1, padding_top=10, padding_bottom=10, height=25, font_size=15, background_color="red"),
            }


    @staticmethod
    def standard_label_style():
        return StandardStyling._get_style_for_platform()["standard_label_style"]

    @staticmethod
    def standard_input_style():
        return StandardStyling._get_style_for_platform()["standard_input_style"]

    @staticmethod
    def standard_selection_style():
        return StandardStyling._get_style_for_platform()["standard_selection_style"]

    @staticmethod
    def standard_button_style():
        return StandardStyling._get_style_for_platform()["standard_button_style"]

    @staticmethod
    def standard_switch_style():
        return StandardStyling._get_style_for_platform()["standard_switch_style"]
   
    @staticmethod
    def standard_box_style():
        return StandardStyling._get_style_for_platform()["standard_box_style"]
    
    @staticmethod
    def standard_highlighted_input_style():
        return StandardStyling._get_style_for_platform()["standard_highlighted_input_style"]
    
