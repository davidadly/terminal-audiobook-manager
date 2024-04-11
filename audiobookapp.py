import os
import sys
from audiobookmanager import AudioBookManager

class AudioBookApp:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.script_path, "config.txt")
        self.audiobook_path = os.path.join(self.script_path, "audiobooks")
        os.makedirs(self.audiobook_path, exist_ok=True)
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config_path = file.read().strip()
                if os.path.exists(config_path):
                    self.audiobook_path = config_path
                else:
                    print(f"Configured path '{config_path}' does not exist. Using default path.")
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
        if os.path.exists(path):
            self.audiobook_path = path
            self.save_config()
            print("Audio book path updated successfully.")
        else:
            print("Invalid path. Path does not exist.")

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
                    self.manager.download_audiobook()  # Remove the argument here
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
                print("\033[91m\nAre you sure you want to exit? Press Ctrl+C again to exit or Enter to go back.\033[0m")
                try:
                    input()
                except KeyboardInterrupt:
                    print("\nExiting the application...")
                    sys.exit(0)