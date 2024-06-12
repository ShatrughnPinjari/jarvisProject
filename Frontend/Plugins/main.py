try:
    # importing prebuilt modules
    from django.conf import settings
    import os
    import wave
    import logging
    import pyttsx3
    import subprocess
    logging.disable(logging.WARNING)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disabling warnings for gpu requirements
    import time
    from keras_preprocessing.sequence import pad_sequences
    import numpy as np
    from keras.models import load_model
    from pickle import load
    import speech_recognition as sr
    import sys
    # importing modules made for assistant
    from Frontend.Plugins.database import *
    from Frontend.Plugins.image_generation import generate_image 
    from Frontend.Plugins.gmail import *  
    from Frontend.Plugins.API_functionalities import *
    from Frontend.Plugins.system_operations import *
    from Frontend.Plugins.browser import *
    from Frontend.Plugins.text import *
except (ImportError, SystemError, Exception, KeyboardInterrupt) as e:
    print(f"ERROR OCCURRED WHILE IMPORTING THE MODULES ,{e}")
    exit(0)

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id)
        self.sys_ops = SystemTasks()
        self.tab_ops = TabOpt()
        self.win_ops = WindowOpt()
        self.model = load_model('Frontend\\Data\\chat_model')
        with open('Frontend\\Data\\tokenizer.pickle', 'rb') as handle:
            self.tokenizer = load(handle)
        with open('Frontend\\Data\\label_encoder.pickle', 'rb') as enc:
            self.lbl_encoder = load(enc)
        self.recognizer = sr.Recognizer()

    def resp():
        return "hello world"   

    def speak(self, text):
        print("ASSISTANT -> " + text)
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except KeyboardInterrupt or RuntimeError:
            pass

    def chat(self, text):
        max_len = 20
        result = self.model.predict(pad_sequences(self.tokenizer.texts_to_sequences([text]),
                                                  truncating='post', maxlen=max_len), verbose=False)
        intent = self.lbl_encoder.inverse_transform([np.argmax(result)])[0]
        return intent
    
    def record(self):
        input_file_path = 'D:\\integration1\\integration\\media\\audio\\temp.wav'
        temp_output_file_path = 'D:\\integration1\\integration\\media\\audio\\temp_converted.wav'

        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"The file {input_file_path} does not exist")

        if convert_audio(input_file_path, temp_output_file_path):
            os.replace(temp_output_file_path, input_file_path)
            transcript = recognize_speech(input_file_path)
            return transcript.lower() if transcript else None
        else:
            return None
        
    def listen_audio(self):
        try:
            while True:
                print("listening")
                response = self.record()
                print("recording")
                if response is None:
                    break
                else:
                    self.main(response)
                    break
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)  
            
    def main(self, query):
        add_data(query)
        intent = self.chat(query)
        done = False
        response_text = None
        if ("google" in query and "search" in query) or ("google" in query and "how to" in query) or "google" in query:
            googleSearch(query)
            return
        elif ("youtube" in query and "search" in query) or "play" in query or ("how to" in query and "youtube" in query):
            youtube(query)
            return
        elif "distance" in query or "map" in query:
            get_map(query)
            return
        if intent == "joke" and "joke" in query:
            joke = get_joke()
            if joke:
                response_text = joke
                done = True
        elif intent == "news" and "news" in query:
            news = get_news()
            if news:
                response_text = news
                done = True
        elif intent == "ip" and "ip" in query:
            ip = get_ip()
            if ip:
                response_text = ip
                done = True
        elif intent == "movies" and "movies" in query:
            response_text = "Some of the latest popular movies are as follows :"
            movies = get_popular_movies()
            if movies:
                response_text += "\n" + movies
                done = True
        elif intent == "tv_series" and "tv series" in query:
            response_text = "Some of the latest popular tv series are as follows :"
            tv_series = get_popular_tvseries()
            if tv_series:
                response_text += "\n" + tv_series
                done = True
        elif intent == "weather" and "weather" in query:
            city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
            if city:
                city = city[2]
                weather = get_weather(city)
                response_text = weather
            else:
                weather = get_weather()
                response_text = weather
            done = True
        elif intent == "internet_speedtest" and "internet" in query:
            response_text = "Getting your internet speed, this may take some time"
            speed = get_speedtest()
            if speed:
                response_text += "\n" + speed
                done = True
        elif intent == "system_stats" and "stats" in query:
            stats = system_stats()
            response_text = stats
            done = True
        elif intent == "image_generation" and "image" in query:
            response_text = "what kind of image you want to generate?"
            self.speak(response_text)
            text = self.record()
            response_text = "Generating image please wait.."
            generate_image(text)
            done = True
        elif intent == "system_info" and ("info" in query or "specs" in query or "information" in query):
            info = systemInfo()
            response_text = info
            done = True
        elif intent == "email" and "email" in query:
            response_text = "Type the Receiver Email-id : "
            self.speak(response_text)
            receiver_id = input()
            while not check_email(receiver_id):
                response_text = "Invalid email id\nType receiver id again : "
                self.speak(response_text)
                receiver_id = input()
            response_text = "Tell the subject of email"
            self.speak(response_text)
            subject = self.record()
            response_text = "tell the body of email"
            self.speak(response_text)
            body = self.record()
            success = send_email(receiver_id, subject, body)
            if success:
                response_text = 'Email sent successfully'
            else:
                response_text = "Error occurred while sending email"
            done = True
        elif intent == "select_text" and "select" in query:
            self.sys_ops.select()
            done = True
        elif intent == "copy_text" and "copy" in query:
            self.sys_ops.copy()
            done = True
        elif intent == "paste_text" and "paste" in query:
            self.sys_ops.paste()
            done = True
        elif intent == "delete_text" and "delete" in query:
            self.sys_ops.delete()
            done = True
        elif intent == "new_file" and "new" in query:
            self.sys_ops.new_file()
            done = True
        elif intent == "switch_tab" and "switch" in query and "tab" in query:
            self.tab_ops.switchTab()
            done = True
        elif intent == "close_tab" and "close" in query and "tab" in query:
            self.tab_ops.closeTab()
            done = True
        elif intent == "new_tab" and "new" in query and "tab" in query:
            self.tab_ops.newTab()
            done = True
        elif intent == "close_window" and "close" in query:
            self.win_ops.closeWindow()
            done = True
        elif intent == "switch_window" and "switch" in query:
            self.win_ops.switchWindow()
            done = True
        elif intent == "minimize_window" and "minimize" in query:
            self.win_ops.minimizeWindow()
            done = True
        elif intent == "maximize_window" and "maximize" in query:
            self.win_ops.maximizeWindow()
            done = True
        elif intent == "screenshot" and "screenshot" in query:
            self.win_ops.Screen_Shot()
            done = True
        elif intent == "stopwatch":
            pass        
        elif intent == "wikipedia" and ("tell" in query or "about" in query):
            description = tell_me_about(query)
            if description:
                response_text = description
            else:
                googleSearch(query)
            done = True
        elif intent == "math":
            answer = get_general_response(query)
            if answer:
                response_text = answer
                done = True
        elif intent == "open_website":
            completed = open_specified_website(query)
            if completed:
                done = True
        elif intent == "open_app":
            completed = open_app(query)
            if completed:
                done = True
        elif intent == "note" and "note" in query:
            response_text = "what would you like to take down?"
            self.speak(response_text)
            note = self.record()
            take_note(note)
            done = True
        elif intent == "get_data" and "history" in query:
            get_data()
            done = True
        elif intent == "exit" and ("exit" in query or "terminate" in query or "quit" in query):
            exit(0)
        if not done:
            answer = get_general_response(query)
            if answer:
                response_text = answer
            else:
                response_text = "Sorry, not able to answer your query"

        if response_text:
            self.speak(response_text)

def start():
    jarvis = Jarvis()
    try:
        jarvis.listen_audio()
    except Exception as e:
        print(f"EXITED: {e}")
        
if __name__ == "__main__":
    start()