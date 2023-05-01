import kivy
import openai
import json

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.window import Window

Window.softinput_mode = "below_target"

Builder.load_file("open_ai.kv")
kivy.require("2.1.0")

# Update Option here if added new key to the json.
dropOptions = [
    "Custom Request",
    "Q&A",
    "Grammar correction",
    "Summarize for a 2nd grader",
    "Text to command",
    "English to other languages",
    "Python to natural language",
    "Calculate Time Complexity",
    "Translate programming languages",
    "Explain code",
    "Science fiction book list maker",
    "Essay outline",
    "Interview questions",
]


class OpenAI(Widget):
    """
    Root class of our APP.
    """

    def __init__(self, **kwargs):
        """
        Add Variables, Methods here for direct access. Or
        You can write the APP logic here. After super().Pass "instance" to function outside.
        """
        super().__init__(**kwargs)
        with open("openai_data.json", encoding="utf-8") as models:
            self.data = json.load(models)
        self.drop_down(dropOptions)

    def generate(self):
        # print(self.data[self.ids.dropdown.text])
        response = self.openai_request()
        if response:
            self.ids.resp.text = response

    def openai_request(self):
        # self.ids.resp.foreground_color = (15, 15, 15)
        try:
            model = "text-davinci-003"
            prompt = self.ids.prompt.text
            temperature = float(self.ids.temp.text)
            max_tokens = int(self.ids.max.text)
            top_p = float(self.ids.top.text)
            frequency_penalty = float(self.ids.freq.text)
            presence_penalty = float(self.ids.pre.text)
            stop = self.ids.stop.text

            if self.ids.stop.text.startswith("\\"):
                # fixed value, for newline.
                stop = ["\n"]
            else:
                stop = [self.ids.stop.text]
            print(stop)
            openai.api_key = self.ids.key.text
            if self.data[self.ids.dropdown.text].get("stop"):
                response = openai.Completion.create(
                    model=model,
                    prompt=self.ids.prompt.text,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop,
                )
            else:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )
            return response
        except openai.error.Timeout as e:
            # Handle timeout error, e.g. retry or log
            self.ids.resp.text = f"OpenAI API request timed out:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except openai.error.APIError as e:
            # Handle API error, e.g. retry or log
            self.ids.resp.text = f"OpenAI API returned an API Error:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except openai.error.APIConnectionError as e:
            # Handle connection error, e.g. check network or log
            self.ids.resp.text = f"OpenAI API request failed to connect:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except openai.error.InvalidRequestError as e:
            # Handle invalid request error, e.g. validate parameters or log
            self.ids.resp.text = f"OpenAI API request was invalid:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except openai.error.AuthenticationError as e:
            # Handle authentication error, e.g. check credentials or log
            self.ids.resp.text = f"OpenAI API request was not authorized:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except openai.error.PermissionError as e:
            # Handle permission error, e.g. check scope or log
            self.ids.resp.text = f"OpenAI API request was not permitted:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except openai.error.RateLimitError as e:
            # Handle rate limit error, e.g. wait or log
            self.ids.resp.text = f"OpenAI API request exceeded rate limit:\n {e}"
            # self.ids.resp.foreground_color = (1, 0, 0, 1)
        except ValueError:
            self.ids.resp.text = """Please:
                Use non decimal value for Max tokens (100 not 100.0 or `100.2).
                And Decimal value for remaining, For New line write '\\n'"""

    def update(self, instance):
        self.ids.prompt.text = str(self.data[self.ids.dropdown.text]["Prompt"])
        self.ids.resp.text = str(self.data[self.ids.dropdown.text]["Response"])

        self.ids.max.text = str(self.data[self.ids.dropdown.text]["Max tokens"])
        self.ids.temp.text = str(self.data[self.ids.dropdown.text]["Temperature"])
        self.ids.top.text = str(self.data[self.ids.dropdown.text]["Top p"])
        self.ids.freq.text = str(self.data[self.ids.dropdown.text]["Frequency penalty"])
        self.ids.pre.text = str(self.data[self.ids.dropdown.text]["Presence penalty"])
        if self.data[self.ids.dropdown.text].get("stop"):
            self.ids.stop.disabled = False
            self.ids.stop.text = str(self.data[self.ids.dropdown.text]["stop"])
        else:
            self.ids.stop.text = str(self.data[self.ids.dropdown.text].get("stop"))
            self.ids.stop.disabled = True

    def drop_down(self, dropValue=None):
        dropdown_x = DropDown()
        dropBtn = self.ids.dropdown
        for value in dropValue:
            btn = Button(
                text=value, on_release=self.update, size_hint_y=None, height="30sp"
            )
            btn.bind(on_release=lambda btn: dropdown_x.select(btn.text))
            dropdown_x.add_widget(btn)

        dropBtn.bind(on_release=dropdown_x.open)
        dropdown_x.bind(on_select=lambda instance, x: setattr(dropBtn, "text", x))


class OpenApp(App):
    """
    Build APP
    """

    def build(self):
        return OpenAI()


if __name__ == "__main__":
    OpenApp().run()
