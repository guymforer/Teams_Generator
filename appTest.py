from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import random
import os
import notify

class TeamGeneratorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.participants_layout = BoxLayout(orientation='vertical')

        self.label = Label(text='Enter the number of teams:')
        self.num_teams_input = TextInput(hint_text='Enter number of teams', multiline=False, input_type='number')
        self.submit_teams_button = Button(text='Submit', on_press=self.submit_teams)

        # Add participant label
        self.add_participant_label = Label(text='Add Participant:')
        
        self.name_input = TextInput(hint_text='Name')
        self.skill_input = TextInput(hint_text='Skill Rank')

        self.add_participant_button = Button(text='Add Participant', on_press=self.add_participant)
        self.generate_teams_button = Button(text='Generate Teams', on_press=self.generate_teams)
        self.go_back_button = Button(text='Go Back', on_press=self.go_back)
        self.clear_all_button = Button(text='Clear All', on_press=self.clear_all)
        self.clear_last_button = Button(text='Clear Last Participant', on_press=self.clear_last_participant)
        self.clear_first_button = Button(text='Clear First Participant', on_press=self.clear_first_participant)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.num_teams_input)
        self.layout.add_widget(self.submit_teams_button)

        self.participants = []
        return self.layout

    def submit_teams(self, instance):
        try:
            self.num_teams = int(self.num_teams_input.text)
            if self.num_teams <= 0:
                raise ValueError("Number of teams must be greater than 0")
        except ValueError:
            self.label.text = "Please enter a valid number of teams."
            return

        self.layout.clear_widgets()
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.add_participant_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.skill_input)
        self.layout.add_widget(self.add_participant_button)
        self.layout.add_widget(self.participants_layout)
        self.layout.add_widget(self.generate_teams_button)
        self.layout.add_widget(self.clear_all_button)
        self.layout.add_widget(self.clear_last_button)
        self.layout.add_widget(self.clear_first_button)
        self.layout.add_widget(self.go_back_button)

    def add_participant(self, instance):
        name = self.name_input.text.strip()
        skill = self.skill_input.text.strip()

        if name and skill:
            participant_data = f"{name},{skill}\n"
            self.participants.append({name: int(skill)})
            self.participants_layout.add_widget(Label(text=f"Added: {name}, Skill: {skill}"))
            self.name_input.text = ''
            self.skill_input.text = ''

            # Save participants to file
            with open("participants.txt", "a") as file:
                file.write(participant_data)

    def generate_teams(self, instance):
        total_skill = sum([int(sum(player.values())) for player in self.participants])

        if self.participants and len(self.participants) % self.num_teams == 0:
            teams = self.create_teams(self.num_teams, self.participants, total_skill)
            self.display_teams(teams)
        else:
            self.label.text = "Invalid number of participants or teams."

    def go_back(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.add_participant_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.skill_input)
        self.layout.add_widget(self.add_participant_button)
        self.layout.add_widget(self.participants_layout)
        self.layout.add_widget(self.generate_teams_button)
        self.layout.add_widget(self.clear_all_button)
        self.layout.add_widget(self.clear_last_button)
        self.layout.add_widget(self.clear_first_button)
        self.layout.add_widget(self.go_back_button)

    def clear_all(self, instance):
        self.participants_layout.clear_widgets()
        self.participants = []
        self.label.text = 'Click the button to generate teams!'
        file_path = "participants.txt"
        with open(file_path, "w"):
            pass

    def clear_last_participant(self, instance):
        if self.participants:
            last_participant = self.participants.pop()
            last_participant_name = list(last_participant.keys())[0]
            self.participants_layout.remove_widget(self.participants_layout.children[-1])  # Remove last label
            self.label.text = f'Removed last participant: {last_participant_name}'

            # Remove last participant from file
            with open("participants.txt", "r+") as file:
                lines = file.readlines()
                lines.pop()
                file.seek(0)
                file.writelines(lines)
                file.truncate()

    def clear_first_participant(self, instance):
        if self.participants:
            first_participant = self.participants.pop(0)
            first_participant_name = list(first_participant.keys())[0]
            self.participants_layout.remove_widget(self.participants_layout.children[0])  # Remove first label
            self.label.text = f'Removed first participant: {first_participant_name}'

            # Remove first participant from file
            with open("participants.txt", "r+") as file:
                lines = file.readlines()
                lines.pop(0)
                file.seek(0)
                file.writelines(lines)
                file.truncate()

    def create_teams(self, num_teams, participants, total_skills):
        random.shuffle(participants)

        while True:
            random.shuffle(participants)

            teams = [participants[i:i + len(participants)//num_teams] for i in range(0, len(participants), len(participants)//num_teams)]
            average_skill = total_skills / num_teams
            teams_skills = []

            for team in teams:
                total = 0
                for player in team:
                    total += int(sum(player.values()))

                teams_skills.append(total)

            if all(average_skill - 1 <= total_skill <= average_skill + 1 for total_skill in teams_skills):
                break

        return teams

    def display_teams(self, teams):
        self.layout.clear_widgets()  # Clear all widgets on the layout
        self.layout.add_widget(Label(text='The generated teams are:'))

        for i, team in enumerate(teams):
            result_dict = {key: value for d in team for key, value in d.items()}
            keys_list = list(result_dict.keys())
            team_label = Label(text=f"Team {i + 1}: {keys_list}")
            self.layout.add_widget(team_label)

        self.layout.add_widget(self.go_back_button)
        notify.send_message(self.generate_message(teams))

    def generate_message(self, teams):
        message_body = 'The generated teams are:\n'

        for i, team in enumerate(teams):
            result_dict = {key: value for d in team for key, value in d.items()}
            keys_list = list(result_dict.keys())
            message_body = message_body + f"Team {i + 1}: {keys_list}\n"

        return message_body

if __name__ == '__main__':
    TeamGeneratorApp().run()
