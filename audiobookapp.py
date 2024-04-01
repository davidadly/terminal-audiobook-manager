# pylint: disable=missing-module-docstring
import os
from audiobookmanager import AudioBookManager

class AudioBookApp:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.script_path, "config.txt")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                self.audiobook_path = file.read().strip()
        else:
            self.audiobook_path = os.path.join(self.script_path, "audio books")
            os.makedirs(self.audiobook_path, exist_ok=True)
            self.save_config()

    def save_config(self):
        with open(self.config_file, "w") as file:
            file.write(self.audiobook_path)

    def set_config_path(self):
        path = input("Enter the new path for the configuration file: ")
        self.config_file = path
        self.load_config()
        print("Configuration file path updated successfully.")

    def set_audiobook_path(self):
        path = input("Enter the new path for audio books: ")
        self.audiobook_path = path
        self.save_config()
        print("Audio book path updated successfully.")

    def run(self):
        self.manager = AudioBookManager(self.audiobook_path)
        while True:
            try:
                print("\nAudio Book Manager")
                print("1. List Audio Books")
                print("2. Download Audio Book")
                print("3. Play Audio Book")
                print("4. Set Audio Book Path")
                print("5. Set Configuration Path")
                print("6. Quit")
                choice = input("Enter your choice (1-6): ")

                if choice == "1":
                    audiobooks = self.manager.list_audiobooks()
                    print("Audio Books:")
                    for audiobook in audiobooks:
                        print(audiobook.title)
                elif choice == "2":
                    self.manager.download_audiobook(self.audiobook_path)
                elif choice == "3":
                    self.manager.play_audiobook()
                elif choice == "4":
                    self.set_audiobook_path()
                elif choice == "5":
                    self.set_config_path()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\nReturning to main menu...")
                continue