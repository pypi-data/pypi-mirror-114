import PySimpleGUI as sg
from typing import Any
from schemdule.prompters import Prompter, PromptResult

class MessageBoxPrompter(Prompter):
    def __init__(self, auto_close=False) -> None:
        super().__init__()
        self.auto_close = auto_close

    def prompt(self, message: str, payload: Any) -> Any:
        sg.popup_scrolled(str(payload), title=f"Attention {message}", auto_close=self.auto_close,
                          keep_on_top=True, background_color='white', text_color='black')

        return PromptResult.Resolved