import time
import sys
import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/macOS
        os.system('clear')

def animate_text(text):
    delay = 0.001  # Reduced delay for faster animation
    clear_screen()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    time.sleep(0.5)  # Shortened pause at the end of the animation

def startup_animation():
    ascii_art = r"""
   _____            .___.__         __________               __        _____                                             
  /  _  \  __ __  __| _/|__| ____   \______   \ ____   ____ |  | __   /     \ _____    ____ _____     ____   ___________ 
 /  /_\  \|  |  \/ __ | |  |/  _ \   |    |  _//  _ \ /  _ \|  |/ /  /  \ /  \\__  \  /    \\__  \   / ___\_/ __ \_  __ \
/    |    \  |  / /_/ | |  (  <_> )  |    |   (  <_> |  <_> )    <  /    Y    \/ __ \|   |  \/ __ \_/ /_/  >  ___/|  | \/
\____|__  /____/\____ | |__|\____/   |______  /\____/ \____/|__|_ \ \____|__  (____  /___|  (____  /\___  / \___  >__|   
        \/           \/                     \/                   \/         \/     \/     \/     \//_____/      \/       
"""
    animate_text(ascii_art)

if __name__ == "__main__":
    startup_animation()