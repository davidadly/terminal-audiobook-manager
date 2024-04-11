import os
import subprocess
import json
from audiobook import AudioBook

class AudioBookManager:
    def __init__(self, audiobook_folder):
        self.audiobook_folder = audiobook_folder
        self.log_file = os.path.join(self.audiobook_folder, "playback.json")
        self.last_selected_file = os.path.join(self.audiobook_folder, "last_selected.json")
        self.create_log_file()

    def create_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                json.dump({}, file)
        if not os.path.exists(self.last_selected_file):
            with open(self.last_selected_file, "w") as file:
                json.dump({}, file)

    def list_audiobooks(self):
        audiobooks = []
        for file_name in os.listdir(self.audiobook_folder):
            if file_name.endswith(".mp3"):
                file_path = os.path.join(self.audiobook_folder, file_name)
                audiobook = AudioBook(file_name[:-4], file_path)
                audiobooks.append(audiobook)
        return audiobooks

    def download_audiobook(self):
        youtube_url = input("Enter the YouTube URL of the audio book: ")
        try:
            subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", f"{self.audiobook_folder}/%(title)s.%(ext)s", youtube_url], check=True)
            print("Audio book downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading audio book: {str(e)}")

    def get_last_played_position(self, audiobook_title):
        try:
            with open(self.log_file, "r") as file:
                playback_data = json.load(file)
                return playback_data.get(audiobook_title, "0")
        except Exception as e:
            print(f"Error loading last played position: {str(e)}")
            return "0"

    def save_last_played_position(self, audiobook):
        try:
            with open(self.log_file, "r") as file:
                playback_data = json.load(file)
            playback_data[audiobook.title] = str(audiobook.current_position)
            with open(self.log_file, "w") as file:
                json.dump(playback_data, file)
        except Exception as e:
            print(f"Error saving last played position: {str(e)}")

    def play_audiobook(self):
        print("\nSelect an option:")
        print("1. List all audiobooks")
        print("2. Search for an audiobook by name")
        choice = input("Enter your choice (1-2): ")

        audiobooks = self.list_audiobooks()

        # Load last selected audiobook if exists
        try:
            with open(self.last_selected_file, "r") as file:
                last_selected = json.load(file)
                last_selected_title = last_selected.get("last_selected_title", "")
                if last_selected_title:
                    audiobooks.sort(key=lambda x: x.title != last_selected_title)
        except Exception as e:
            print(f"Error loading last selected audiobook: {str(e)}")

        if choice == "1":
            if not audiobooks:
                print("No audiobooks found.")
                return
            print("\nAudio Books:")
            for i, audiobook in enumerate(audiobooks, start=1):
                print(f"{i}. {audiobook.title}")
        elif choice == "2":
            query = input("Enter the beginning of the audiobook name to search: ").lower()
            filtered_audiobooks = [ab for ab in audiobooks if ab.title.lower().startswith(query)]
            
            if not filtered_audiobooks:
                print("No audiobooks found matching your query.")
                return
                
            print("\nFiltered Audio Books:")
            for i, audiobook in enumerate(filtered_audiobooks, start=1):
                print(f"{i}. {audiobook.title}")
        else:
            print("Invalid choice.")
            return

        selection = input("Enter the number of the audiobook you want to play: ")
        try:
            index = int(selection) - 1
            selected_audiobooks = audiobooks if choice == "1" else filtered_audiobooks
            if 0 <= index < len(selected_audiobooks):
                audiobook = selected_audiobooks[index]

                # Save last selected audiobook
                with open(self.last_selected_file, "w") as file:
                    json.dump({"last_selected_title": audiobook.title}, file)

                print("\nSelect the playback option:")
                print("1. Play in QuickTime Player")
                print("2. Play in Terminal")
                playback_choice = input("Enter your choice (1-2): ")
                if playback_choice == "1":
                    start_time = self.get_last_played_position(audiobook.title)
                    audiobook.play(start_time)
                elif playback_choice == "2":
                    start_time = self.get_last_played_position(audiobook.title)
                    audiobook.play_with_progress(start_time)
                    self.save_last_played_position(audiobook)
                else:
                    print("Invalid choice. Returning to the main menu.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")