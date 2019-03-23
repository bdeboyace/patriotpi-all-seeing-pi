from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime
from overlay_functions import *
from guizero import App, PushButton, Text, Picture, TextBox
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )
import random
import os

def next_overlay():
    global overlay
    overlay = next(all_overlays)
    preview_overlay(camera, overlay)

def take_picture():
    global output
    output = strftime("/home/pi/allseeingpi/image-%d-%m %H:%M.png", gmtime())
    camera.capture(output)
    camera.stop_preview()
    remove_overlays(camera)
    output_overlay(output, overlay)
    size = 400, 400
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    gif_img.save(latest_photo, 'gif')
    your_pic.set(latest_photo)

def screen_keyboard():
    os.system("matchbox-keyboard")
    
def new_picture():
    #os.system("pkill matchbox-keyboard")
    twitter_username.value = "@"
    camera.start_preview()
    preview_overlay(camera, overlay)

def send_tweet():
    #os.system("pkill matchbox-keyboard")
    twitter_handle = twitter_username.value
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
        )
    message = random.choice(messages)
    if twitter_handle !="@":
        tweet = message + str(" " + twitter_handle)
    else:
        tweet = message
    with open(output, 'rb') as photo:
        twitter.update_status_with_media(status=tweet, media=photo)

messages = [
    "This #PatriotPi Party is particularly preposterous #rjam #cvspatriots",
    "This #PatriotPi Party is pure pandemonium #rjam #cvspatriots",
    "I find this #PatriotPi Party particulary pleasant #rjam #cvspatriots",
    "I did not prepare my people for the pandemonium this #PatriotPi Party put unto me #rjam #cvspatriots",
    "The #PatriotPi Picture Pi program took this picture #rjam #cvspatriots",
    "I have been proscribed participation is the most preposterously pleasant #PatriotPi party #rjam #cvspatriots",
    "The people at this #PatriotPi Party are particulary pleasant and polite #rjam #cvspatriots",
    "This #PatriotPi party may pique my purchases of Pi property, paraphernalia and panoply #rjam #cvspatriots",
    "This #PatriotPi party provokes pleasant presentiments #rjam #cvspatriots",
    "I perceive prestigious participation as I partake in this #PatriotPi party #rjam #cvspatriots",
    "It's pertient that this phenomenal #PatriotPi picture project is presented to the public #rjam #cvspatriots"
    
    ]

    
next_overlay_btn = Button(23)
take_pic_btn = Button(25)

camera = PiCamera()
camera.resolution = (800,480)
camera.hflip = True
camera.rotation = 90
camera.start_preview()

output = ""
latest_photo = '/home/pi/allseeingpi/latest.gif'

next_overlay_btn.when_pressed = next_overlay
take_pic_btn.when_pressed = take_picture

app = App("The All-Seeing Pi", 800, 480, bg = "#6ABF4B")
app.tk.attributes("-fullscreen", True)
header_pic = Picture(app, image="pprjam.png")
your_pic = Picture(app, latest_photo)
new_pic = PushButton(app, new_picture, text = "New picture")
new_pic.bg= "#B61845"
text = Text(app, text = "Enter your Twitter Handle below (optional)")
twitter_username = TextBox(app, width = 17)
twitter_username.value = "@"
#twitter_username.when_clicked = screen_keyboard
tweet_pic = PushButton(app, send_tweet, text="Tweet picture")
tweet_pic.bg = "#1DA1F2"
app.display()
