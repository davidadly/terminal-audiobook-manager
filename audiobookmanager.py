import os
import subprocess
from audiobook import AudioBook

class AudioBookManager:
    def __init__(self, audiobook_folder):
        self.audiobook_folder = audiobook_folder
        self.log_file = os.path.join(self.audiobook_folder, "playback.log")

    def list_audiobooks(self):
        audiobooks = []
        for file_name in os.listdir(self.audiobook_folder):
            if file_name.endswith(".mp3"):
                file_path = os.path.join(self.audiobook_folder, file_name)
                audiobook = AudioBook(file_name[:-4], file_path)
                audiobooks.append(audiobook)
        return audiobooks

    def download_audiobook(self, audiobook_path):
        url = input("Enter the YouTube URL of the audio book: ")
        try:
            subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", f"{audiobook_path}/%(title)s.%(ext)s", url])
            print("Audio book downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading audio book: {str(e)}")

    def play_audiobook(self):
        print("\nSelect an option:")
        print("1. List all audiobooks")
        print("2. Search for an audiobook by name")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            audiobooks = self.list_audiobooks()
            if not audiobooks:
                print("No audiobooks found.")
                return
            print("\nAudio Books:")
            for i, audiobook in enumerate(audiobooks, start=1):
                print(f"{i}. {audiobook.title}")
        elif choice == "2":
            query = input("Enter the beginning of the audiobook name to search: ").lower()
            audiobooks = self.list_audiobooks()
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
                print("\nSelect the playback option:")
                print("1. Play in QuickTime Player")
                print("2. Play in Terminal")
                playback_choice = input("Enter your choice (1-2): ")
                if playback_choice == "1":
                    start_time = self.get_last_played_position(audiobook.title)
                    audiobook.play(start_time)
                    self.save_last_played_position(audiobook.title)
                elif playback_choice == "2":
                    start_time = self.get_last_played_position(audiobook.title)
                    audiobook.play_with_progress(start_time)
                    self.save_last_played_position(audiobook.title)
                else:
                    print("Invalid choice. Returning to the main menu.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def get_last_played_position(self, audiobook_title):
        if not os.path.exists(self.log_file):
            return None

        with open(self.log_file, "r") as file:
            for line in file:
                title, position = line.strip().split(",")
                if title == audiobook_title:
                    return position

        return None

    def save_last_played_position(self, audiobook_title):
        last_position = self.get_playback_position()
        if last_position:
            with open(self.log_file, "a") as file:
                file.write(f"{audiobook_title},{last_position}\n")

    def get_playback_position(self):
        try:
            output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-i", "pipe:0"], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            duration = float(output.decode().strip())
            return str(duration)
        except subprocess.CalledProcessError:
            return None