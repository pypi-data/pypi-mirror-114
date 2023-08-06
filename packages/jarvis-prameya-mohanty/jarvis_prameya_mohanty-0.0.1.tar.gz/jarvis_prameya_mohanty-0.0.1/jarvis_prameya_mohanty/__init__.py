''' Package Name: jarvis_prameya_mohanty '''

# Imported Functions

import pyttsx3
import speech_recognition as sr
import wikipedia
import os
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Important Functions


def speak(audio):
    ''' This function makes python speak. You just need to give a string as argument and python will speak it. You need to select a voice. Two voices are available for windows. Male and Female. '''

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    voice = int(input("Enter 0 for Female Voice and 1 for Male Voice: "))
    engine.setProperty("voice", voices[voice].id)
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    ''' This function helps to take voice input from the user. It also prints what the user said. It prints 'Listening...' when its taking command and then it 'Recognises' and finally prints the command. '''

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognising...")
        query = r.recognize_google(audio, language="en-in")
        print("User Said: ", query)

    except Exception as e:
        speak(e)
        return "None"
    return query


def searchWiki(query):
    ''' This function takes a query, finds that query in wikipedia and then speaks and printes the result. You need to specify the number of sentences. '''

    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    sentence = int(input("Enter the number of sentences you need: "))
    results = wikipedia.summary(query, sentences=sentence)
    speak("According to wikipedia")
    print(results)
    speak(results)


def playMusic():
    ''' This functions play random music inside a specific directory which will be given by the user as input. '''

    dir = input("Enter the path for your music directory: ")
    dir = dir.replace('\\', '\\\\')
    songs = os.listdir(dir)
    i = random.randint(1, len(songs))
    print(f"Playing {songs[i]}...")
    os.startfile(os.path.join(dir, songs[i]))


def time():
    ''' This function gives the current local time. It will give the time in Hours and Minutes. '''

    strTimeH = datetime.now().strftime("%H")
    strTimeM = datetime.now().strftime("%M")
    if strTimeH > "12":
        speak(f"The time is {int(strTimeH) - 12}:{strTimeM}")
    else:
        speak(f"The time is {strTimeH}:{strTimeM}")


def sendMail(SENDER_EMAIL, SENDER_PWD, RECEIVER_EMAIL):
    ''' This function sends an E-Mail. You can also attach something in your E-Mail! '''

    try:
        speak("What should I say in the e-mail?")
        content = takeCommand()
        speak("What should I write in the subject of the e-mail? ")
        subject = takeCommand()
        speak("To whom should I send the E-Mail? ")
        email_user = SENDER_EMAIL
        email_password = SENDER_PWD
        email_send = RECEIVER_EMAIL

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_send
        msg["Subject"] = subject

        body = content
        msg.attach(MIMEText(body, "plain"))

        attach = input("Attachment Required? Yes(y), No(n)").lower()
        if attach == 'y':
            speak("Write the path of the file you want to attach")
            filename = input("Write Below \n")
            attachment = open(filename, "rb")

            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            "attachment; filename= " + filename)

            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()
            speak("E-Mail has been sent successfully!")
        elif attach == 'n':
            text = msg.as_string()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()
            speak("E-Mail has been sent successfully!")
    except Exception as error:
        speak("An error occurred which is printed on the console.")
        print(error)

def wish():
    ''' This function wishes the user according to the time. '''

    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    elif 18 <= hour < 21:
        speak("Good Evening!")
    else:
        speak("Good Late Evening!")