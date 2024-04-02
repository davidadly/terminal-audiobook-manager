import os
import subprocess
import time
import sys
import select
import tty
import termios

class AudioBook:
    def __init__(self, title, file_path):
        self.title = title
        self.file_path = file_path

    def play(self, start_time=None):
        print(f"Playing: {self.title}")
        if start_time:
            subprocess.Popen(["open", "-a", "QuickTime Player", self.file_path, "--args", "-ss", start_time],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["open", "-a", "QuickTime Player", self.file_path],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def get_duration(self):
        try:
            output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", self.file_path])
            duration = float(output.decode().strip())
            return duration
        except subprocess.CalledProcessError:
            return None

    def display_play_bar(self, current_time, duration):
        bar_width = 50
        filled_width = int(bar_width * current_time / duration)
        empty_width = bar_width - filled_width

        filled_bar = "█" * filled_width
        empty_bar = "░" * empty_width
        play_bar = f"{filled_bar}{empty_bar}"

        sys.stdout.write(f"\r[{play_bar}] {current_time:.2f}/{duration:.2f}")
        sys.stdout.flush()

    def get_keypress(self):
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            if select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                if key == "\x1b":  # Arrow keys start with "\x1b"
                    key += sys.stdin.read(2)
                return key
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return None

    def play_with_progress(self, start_time=None):
        duration = self.get_duration()
        if duration is None:
            print("Unable to retrieve the duration of the audiobook.")
            return

        process = None
        if start_time:
            process = subprocess.Popen(["ffplay", "-ss", start_time, "-nodisp", self.file_path],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            process = subprocess.Popen(["ffplay", "-nodisp", self.file_path],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        current_time = float(start_time) if start_time else 0.0
        while process.poll() is None:
            self.display_play_bar(current_time, duration)
            key = self.get_keypress()
            if key == "q":
                process.terminate()
                break
            elif key == "\x1b[D":  # Left arrow key
                current_time = max(0, current_time - 5)
                process.terminate()
                process = subprocess.Popen(["ffplay", "-ss", str(current_time), "-nodisp", self.file_path],
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif key == "\x1b[C":  # Right arrow key
                current_time = min(duration, current_time + 5)
                process.terminate()
                process = subprocess.Popen(["ffplay", "-ss", str(current_time), "-nodisp", self.file_path],
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            current_time += 1

        sys.stdout.write("\n")
        sys.stdout.flush()