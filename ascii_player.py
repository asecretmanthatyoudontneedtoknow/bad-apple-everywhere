import cv2
import time
import os
import sys
import pygame
import glob

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]

def resize_frame(frame, new_width=120):
    height, width, _ = frame.shape
    ratio = height / width * 0.45
    new_height = int(new_width * ratio)
    return cv2.resize(frame, (new_width, new_height))

def play_ascii_video():
    # Автоматический поиск файлов
    video_files = glob.glob("*.mp4")
    midi_files = glob.glob("*.mid")
    
    if not video_files:
        print("Ошибка: MP4 файл не найден!")
        return
    
    video_path = video_files[0]
    midi_path = midi_files[0] if midi_files else None

    # Инициализация звука
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
