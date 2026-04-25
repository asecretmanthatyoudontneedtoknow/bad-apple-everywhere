import cv2
import time
import os
import sys
import glob
import shutil

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

if os.name == 'nt':
    import ctypes
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, 3)
    except Exception:
        pass

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]

def resource_path():
    try:
        return sys._MEIPASS
    except Exception:
        return os.path.abspath(".")

def resize_frame(frame, term_width, term_height):
    height, width, _ = frame.shape
    ratio = height / width * 0.45 
    
    max_w = max(10, term_width - 2)
    max_h = max(10, term_height - 2)
    
    new_width = max_w
    new_height = int(new_width * ratio)
    
    if new_height > max_h:
        new_height = max_h
        new_width = int(new_height / ratio)
        
    resized = cv2.resize(frame, (new_width, new_height))
    return resized, new_width, new_height

def get_centered_frame(ascii_str, img_w, img_h, term_w, term_h):
    lines = [ascii_str[i:(i + img_w)] for i in range(0, len(ascii_str), img_w)]
    pad_left = max(0, (term_w - img_w) // 2)
    pad_top = max(0, (term_h - img_h) // 2)
    padded_lines = [(" " * pad_left) + line for line in lines]
    return ("\n" * pad_top) + "\n".join(padded_lines)

def play_ascii_video():
    base_dir = resource_path()
    video_files = glob.glob(os.path.join(base_dir, "*.mp4"))
    midi_files = glob.glob(os.path.join(base_dir, "*.mid"))
    
    if not video_files:
        print("Error: MP4 file not found inside binary!")
        return
    
    video_path = video_files[0]
    midi_path = midi_files[0] if midi_files else None

    if midi_path:
        pygame.init()
        pygame.mixer.music.load(midi_path)

    cap = cv2.VideoCapture(video_path)
    os.system('cls' if os.name == 'nt' else 'clear')

    start_time = time.time()
    music_started = False

    try:
        while cap.isOpened():
            current_time = time.time()
            
            if midi_path and not music_started:
                if (current_time - start_time) >= 0.5:
                    pygame.mixer.music.play()
                    music_started = True

            ret, frame = cap.read()
            if not ret:
                break

            term_size = shutil.get_terminal_size((80, 24))
            term_w = term_size.columns
            term_h = term_size.lines

            frame, img_w, img_h = resize_frame(frame, term_w, term_h)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            ascii_str = "".join([ASCII_CHARS[min(p // 22, 11)] for p in gray.flatten()])
            ascii_img = get_centered_frame(ascii_str, img_w, img_h, term_w, term_h)

            sys.stdout.write('\033[H' + ascii_img)
            sys.stdout.flush()
            
            time.sleep(0.033)
            
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if midi_path:
            pygame.mixer.music.stop()
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    play_ascii_video()