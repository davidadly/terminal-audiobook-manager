import os
import subprocess
from audiobook import AudioBook

class AudioBookManager:
    def __init__(self, audiobook_folder):
        self.audiobook_folder = audiobook_folder

    def list_audiobooks(self):
        audiobooks = []
        for file_name in os.listdir(self.audiobook_folder):
            file_path = os.path.join(self.audiobook_folder, file_name)
            audiobook = AudioBook(file_name, file_path)
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
        audiobooks = self.list_audiobooks()
        print("Audio Books:")
        for i, audiobook in enumerate(audiobooks, start=1):
            print(f"{i}. {audiobook.title}")
        selection = input("Enter the number of the audiobook you want to play: ")
        try:
            index = int(selection) - 1
            if 0 <= index < len(audiobooks):
                audiobook = audiobooks[index]
                audiobook.play()
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")