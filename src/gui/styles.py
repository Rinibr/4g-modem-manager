from tkinter import font

# Styling constants for the GUI components
class Styles:
    BUTTON_FONT = font.Font(family="Helvetica", size=12, weight="bold")
    LABEL_FONT = font.Font(family="Helvetica", size=10)
    ENTRY_FONT = font.Font(family="Helvetica", size=10)
    
    BUTTON_BG_COLOR = "#4CAF50"
    BUTTON_FG_COLOR = "#FFFFFF"
    ENTRY_BG_COLOR = "#FFFFFF"
    ENTRY_FG_COLOR = "#000000"
    LABEL_BG_COLOR = "#F0F0F0"
    LABEL_FG_COLOR = "#000000"
    
    @staticmethod
    def get_button_style():
        return {
            "font": Styles.BUTTON_FONT,
            "bg": Styles.BUTTON_BG_COLOR,
            "fg": Styles.BUTTON_FG_COLOR,
        }
    
    @staticmethod
    def get_label_style():
        return {
            "font": Styles.LABEL_FONT,
            "bg": Styles.LABEL_BG_COLOR,
            "fg": Styles.LABEL_FG_COLOR,
        }
    
    @staticmethod
    def get_entry_style():
        return {
            "font": Styles.ENTRY_FONT,
            "bg": Styles.ENTRY_BG_COLOR,
            "fg": Styles.ENTRY_FG_COLOR,
        }