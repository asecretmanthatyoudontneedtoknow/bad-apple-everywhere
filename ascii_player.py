import cv2
import time
import os
import sys
import pygame
import glob

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]

def resource_path():
    """Получает путь к ресурсам, распакованным внутри .exe/.sh"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        return sys._MEIPASS
    except Exception:
        # Если запускаем просто как скрипт (не скомпилированный)
        return os.path.abspath(".")

def resize_frame(frame, new_width=120):
    height, width, _ = frame.shape
    ratio = height / width * 0.45
    new_height = int(new_width * ratio)
    return cv2.resize(frame, (new_width, new_height))

def play_ascii_video():
    # Ищем файлы во временной директории экзешника
    base_dir = resource_path()
    video_files = glob.glob(os.path.join(base_dir, "*.mp4"))
    midi_files = glob.glob(os.path.join(base_dir, "*.mid"))
    
    if not video_files:
        print("Ошибка: MP4 файл не зашит в программу!")
        return
    
    video_path = video_files[0]
    midi_path = midi_files[0] if midi_files else None

    if midi_path:
        pygame.init()
        pygame.mixer.music.load(midi_path)
        pygame.mixer.music.play()

    cap = cv2.VideoCapture(video_path)
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            frame = resize_frame(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            ascii_str = "".join([ASCII_CHARS[min(p // 22, 11)] for p in gray.flatten()])
            img_width = gray.shape[1]
            ascii_img = "\n".join([ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)])

            sys.stdout.write('\033[H' + ascii_img)
            sys.stdout.flush()
            time.sleep(0.033)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if midi_path: pygame.mixer.music.stop()

if __name__ == '__main__':
    play_ascii_video()