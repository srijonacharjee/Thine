import urllib.request
import json
import ssl
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

API_KEY = "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"

class ThineTutor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        self.title = Label(text="Thine - AI Tutor", font_size='24sp', size_hint_y=0.1, bold=True)
        self.add_widget(self.title)
        
        self.scroll = ScrollView(size_hint_y=0.7)
        self.answer_label = Label(
            text="Hello! Ask me any question about your studies.",
            font_size='18sp',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.answer_label.bind(width=lambda *x: self.answer_label.setter('text_size')(self.answer_label, (self.answer_label.width, None)))
        self.answer_label.bind(texture_size=self.answer_label.setter('size'))
        self.scroll.add_widget(self.answer_label)
        self.add_widget(self.scroll)
        
        self.input_box = TextInput(hint_text="Type your question here...", size_hint_y=0.12, font_size='18sp')
        self.add_widget(self.input_box)
        
        self.ask_btn = Button(text="Ask Thine", size_hint_y=0.1, font_size='20sp', background_color=(0.1, 0.5, 0.8, 1))
        self.ask_btn.bind(on_press=self.get_answer)
        self.add_widget(self.ask_btn)

    def get_answer(self, instance):
        question = self.input_box.text.strip()
        if not question:
            return
        self.answer_label.text = "Thine is thinking..."
        url = "https://groq.com"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are Thine, a helpful and friendly tutor for a high school student. Explain simply."},
                {"role": "user", "content": question}
            ]
        }
        try:
            ctx = ssl._create_unverified_context()
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, context=ctx) as response:
                result = json.loads(response.read().decode('utf-8'))
                reply = result['choices']['message']['content']
                self.answer_label.text = reply
        except Exception as e:
            self.answer_label.text = f"Error: {str(e)}"

class ThineApp(App):
    def build(self):
        return ThineTutor()

if __name__ == '__main__':
    ThineApp().run()
