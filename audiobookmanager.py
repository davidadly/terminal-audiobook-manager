import os
import subprocess
from audiobook import AudioBook

class AudioBookManager:
    """
    A class to manage audio books.

    Attributes:
        audiobook_folder (str): The folder path where audio books are stored.
        log_file (str): The path to the log file for storing playback positions.
    """

    def __init__(self, audiobook_folder):
        """
        Initialize an AudioBookManager instance.

        Args:
            audiobook_folder (str): The folder path where audio books are stored.
        """
        self.audiobook_folder = audiobook_folder
        self.log_file = os.path.join(self.audiobook_folder, "playback.log")

    def list_audiobooks(self):
        """
        List all the audio books in the audiobook folder.

        Returns:
            list: A list of AudioBook objects representing the audio books.
        """
        audiobooks = []
        for file_name in os.listdir(self.audiobook_folder):
            if file_name.endswith(".mp3"):
                file_path = os.path.join(self.audiobook_folder, file_name)
                audiobook = AudioBook(file_name[:-4], file_path)
                audiobooks.append(audiobook)
        return audiobooks

    def download_audiobook(self, audiobook_path):
        """
        Download an audio book from a YouTube URL.

        Args:
            audiobook_path (str): The folder path where the downloaded audio book will be saved.
        """
        url = input("Enter the YouTube URL of the audio book: ")
        try:
            subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", f"{audiobook_path}/%(title)s.%(ext)s", url])
            print("Audio book downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading audio book: {str(e)}")

    def play_audiobook(self):
        """
        Play an audio book based on user selection.

        The user can choose to list all audio books or search for an audio book by name.
        After selecting an audio book, the user can choose to play it in QuickTime Player or in the terminal.
        """
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
        """
        Get the last played position of an audio book.

        Args:
            audiobook_title (str): The title of the audio book.

        Returns:
            str: The last played position of the audio book, or None if not found.
        """
        if not os.path.exists(self.log_file):
            return None

        with open(self.log_file, "r") as file:
            for line in file:
                title, position = line.strip().split(",")
                if title == audiobook_title:
                    return position

        return None

    def save_last_played_position(self, audiobook_title):
        """
        Save the last played position of an audio book.

        Args:
            audiobook_title (str): The title of the audio book.
        """
        last_position = self.get_playback_position()
        if last_position:
            with open(self.log_file, "a") as file:
                file.write(f"{audiobook_title},{last_position}\n")

    def get_playback_position(self):
        """
        Get the current playback position.

        Returns:
            str: The current playback position, or None if an error occurs.
        """
        try:
            output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-i", "pipe:0"], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            duration = float(output.decode().strip())
            return str(duration)
        except subprocess.CalledProcessError:
            return None