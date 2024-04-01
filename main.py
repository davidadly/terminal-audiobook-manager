from audiobookapp import AudioBookApp
from startup_animation import startup_animation

if __name__ == "__main__":
    startup_animation()
    app = AudioBookApp()
    app.run()