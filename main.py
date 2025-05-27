from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import json
import os

EVENTS_FILE = "events.json"

class EventPlanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.event_input = TextInput(hint_text='Event Title, Date (YYYY-MM-DD), Time, Description', multiline=False)
        self.add_widget(self.event_input)

        self.add_button = Button(text='Add Event')
        self.add_button.bind(on_press=self.add_event)
        self.add_widget(self.add_button)

        self.view_button = Button(text='View Events')
        self.view_button.bind(on_press=self.view_events)
        self.add_widget(self.view_button)

        self.output = Label(size_hint_y=3)
        self.add_widget(self.output)

    def add_event(self, instance):
        text = self.event_input.text.strip()
        parts = text.split(',')
        if len(parts) == 4:
            title, date, time, desc = [p.strip() for p in parts]
            events = self.load_events()
            events.append({
                'title': title,
                'date': date,
                'time': time,
                'description': desc
            })
            self.save_events(events)
            self.output.text = f"Added: {title}"
            self.event_input.text = ""
        else:
            self.output.text = "Please enter: title, date, time, description"

    def view_events(self, instance):
        events = self.load_events()
        if events:
            events_sorted = sorted(events, key=lambda e: f"{e['date']} {e['time']}")
            output = "\n".join([f"{e['title']} on {e['date']} at {e['time']}" for e in events_sorted])
        else:
            output = "No events found."
        self.output.text = output

    def load_events(self):
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_events(self, events):
        with open(EVENTS_FILE, 'w') as f:
            json.dump(events, f, indent=4)

class EventApp(App):
    def build(self):
        return EventPlanner()

if __name__ == '__main__':
    EventApp().run()
# Trigger build
