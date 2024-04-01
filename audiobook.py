import os

class AudioBook:
    def __init__(self, title, file_path):
        self.title = title
        self.file_path = file_path

    def play(self):
        print(f"Playing: {self.title}")
        os.system(f"open -a 'QuickTime Player' '{self.file_path}'")