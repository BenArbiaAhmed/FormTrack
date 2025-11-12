import threading
import pygame

pygame.mixer.init()
pygame.mixer.set_num_channels(1)


def play_go_lower_sound():
    try:
        sound = pygame.mixer.Sound('data/static/audio/go-lower.mp3')
        sound.play()
    except Exception as e:
        print(f"Audio error: {e}")


def play_bring_arms_colser_sound():
    try:
        sound = pygame.mixer.Sound('data/static/audio/bring-arms-closer.mp3')
        sound.play()
    except Exception as e:
        print(f"Audio error: {e}")
        print("An exception happened with audio play.")

def play_bring_legs_colser_sound():
    try:
        sound = pygame.mixer.Sound('data/static/audio/bring-legs-closer.mp3')
        sound.play()
    except Exception as e:
        print(f"Audio error: {e}")
        print("An exception happened with audio play.")

def play_straighten_your_back_sound():
    try:
        sound = pygame.mixer.Sound('data/static/audio/straighten-your-back.mp3')
        sound.play()
    except Exception:
        print("An exception happened with audio play.")

def play_feedback_sound(feedback):
    if(feedback == 'Bring arms closer !'):
        play_bring_arms_colser_sound()
    elif(feedback == 'Bring legs closer !'):
        play_bring_legs_colser_sound()
    elif(feedback == 'Straighten back !'):
        play_straighten_your_back_sound()