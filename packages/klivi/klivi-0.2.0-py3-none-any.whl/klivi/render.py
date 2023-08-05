import tkinter as tk
from typing import Any, Dict

widget_alias: Dict[str, Any] = {
    "div": tk.Widget,
    "frame": tk.Frame,
    "button": tk.Button,
    "label": tk.Label,
    "text": tk.Text,
    "input": tk.Entry,
    "canvas": tk.Canvas,
    "radio-button": tk.Radiobutton,
    "menu": tk.Menu,
    "menu-button": tk.Menubutton,
    "check-button": tk.Checkbutton,
    "list-box": tk.Listbox,
}
