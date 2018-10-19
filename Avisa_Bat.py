#Avisa_Bat
#13/10/2018
#OdinPT

import subprocess
import time
import battery as battery

import pygame as pg
import power
from datetime import datetime

from tkinter import *


music_file = "audiox.wav"
volume = 1.0

def read_status():  #verifica estado da bateria

    command = "upower -i $(upower -e | grep BAT) | grep --color=never -E percentage|xargs|cut -d' ' -f2|sed s/%//"
    get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    return get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")

def play_music(music_file, volume):     #Reproduz se a musica existir

    pg.init()

    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        #print("Music file {} loaded!".format(music_file))
    except pg.error:
        print("File {} not found! ({})".format(music_file, pg.get_error()))
        return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


def take_action(music_file,volume,horaBegin,horaEnd,atual):    #notificacao da percentagem da bateria

   command_above = "notify-send 'Bateria acima de 60'%"
   command_below = "notify-send 'Bateria abaixo de 60%'"
   command_Corrente = "notify-send 'Em modo Corrente'"
   command_bat = "notify-send 'Em modo Bateria'"
   times = 0

   ans = power.PowerManagement().get_providing_power_source_type()
   if not ans:
        #Modo Corrente
        subprocess.Popen(["/bin/bash", "-c", command_Corrente])
        charge = int(read_status())
        times = 0
        time.sleep(30)
        take_action(music_file,volume,horaBegin,horaEnd,atual)

   else:
        #Modo Bateria
    subprocess.Popen(["/bin/bash", "-c", command_bat])
    charge = int(read_status())
    time.sleep(10)


    if horaBegin == atual > horaEnd:
        if charge > 60:
            time.sleep(10)
            take_action(music_file,volume,horaBegin,horaEnd,atual)

            if times == 0:
                subprocess.Popen(["/bin/bash", "-c", command_above])
                times = 1

        elif charge < 60:
            time.sleep(10)
            take_action(music_file,volume,horaBegin,horaEnd,atual)
            play_music(music_file, volume)

            if times == 0:
                subprocess.Popen(["/bin/bash", "-c", command_below])
                times = 1
            else:
                times = 0
                time.sleep(10)
                take_action(music_file,volume,horaBegin,horaEnd,atual)
    else :
        time.sleep(15)
        take_action(music_file,volume,horaBegin,horaEnd,atual)
        #print "else nao desperta"

# Main
time.sleep(10)

#valores entre as quais o programa se mantem silencioso
date = datetime.now()
horaBegin = 22
horaEnd = 07

#atual
now = datetime.now()
atual = now.hour
take_action(music_file,volume,horaBegin,horaEnd,atual)

