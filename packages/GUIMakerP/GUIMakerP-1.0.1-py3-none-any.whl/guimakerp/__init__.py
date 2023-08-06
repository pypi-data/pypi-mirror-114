import json
import tkinter as tk

texts = {}
def get_text(text_name: str) -> str:
    return texts[text_name].get("1.0", tk.END)

class Application:
    def __init__(self):
        self.root = None
        self.settings = {}
    
    def create_settings(self) -> dict:
        try:
            self.settings = json.loads(open("settings.json", "r").read())
            return json.loads(open("settings.json", "r").read())
        except:
            print("Did not find settings.json file!")
            self.settings = {}
            return {}
    
    def create_window(self) -> None:
        if self.settings == {}:
            print("Settings were not created properly!")
            return
        if "window" in self.settings:
            self.root = tk.Tk()
            if "width" in self.settings["window"] and "height" in self.settings["window"]:
                self.root.geometry(f"{self.settings['window']['width']}x{self.settings['window']['height']}")
            else:
                print("Width or height was not defined!")
                return
            if "title" in self.settings["window"]:
                self.root.title(self.settings["window"]["title"])
            else:
                print("Title was not defined!")
            self.root.resizable(False, False)
            if "color" in self.settings["window"]:
                self.root.config(bg=self.settings["window"]["color"])
            else:
                self.root.config(bg="black")
    
    def place_widgets(self) -> None:  # sourcery no-metrics skip: extract-duplicate-method, merge-else-if-into-elif
        if self.settings == {}:
            print("Settings were not created properly!")
            return
        if self.root is None:
            print("Didnt create the window!")
            return
        if "window" in self.settings:
            if "widgets" in self.settings["window"]:
                for widget in self.settings["window"]["widgets"]:
                    if widget["type"] == "label":
                        label = tk.Label(self.root, text=widget["text"])
                        if "fgcolor" in widget:
                            label.config(fg=widget["fgcolor"])
                        else:
                            label.config(fg="white")
                        if "bgcolor" in widget:
                            label.config(bg=widget["bgcolor"])
                        else:
                            if "color" in self.settings["window"]:
                                label.config(bg=self.settings["window"]["color"])
                            else:
                                label.config(bg="black")
                        label.pack()
                    if widget["type"] == "button":
                        button = tk.Button(self.root, text=widget["text"], command=lambda: exec(widget["python"]))
                        if "fgcolor" in widget:
                            button.config(fg=widget["fgcolor"])
                        else:
                            button.config(fg="white")
                        if "bgcolor" in widget:
                            button.config(bg=widget["bgcolor"])
                        else:
                            if "color" in self.settings["window"]:
                                button.config(
                                    bg=self.settings["window"]["color"])
                            else:
                                button.config(bg="black")
                        button.pack()
                    if widget["type"] == "text":
                        text = tk.Text(self.root)
                        if "fgcolor" in widget:
                            text.config(fg=widget["fgcolor"])
                        else:
                            text.config(fg="black")
                        if "bgcolor" in widget:
                            text.config(bg=widget["bgcolor"])
                        else:
                            text.config(bg="white")
                        if "name" in widget:
                            texts[widget["name"]] = text
                        text.pack()
            else:
                print("No widgets to place!")
                return
    
    def run(self) -> None:
        if self.root is None:
            print("Didnt create the window!")
            return
        self.root.mainloop()