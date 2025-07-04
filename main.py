from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from openai import OpenAI
import webbrowser
import base64
import os

class Home(Screen):
    pass

class About(Screen):
    pass

class Diagnosis(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.doctor = ChatBot()
    
    def show_response(self, message):
        self.ids.response.text += message
        self.ids.response.parent.scroll_y = 0
    
    def text_inquiry(self):
        self.doctor.chat(self.ids.prompt.text)
        self.show_response(f"\n\n[color=FC0303]{self.ids.prompt.text}[/color]"+self.doctor.reply)
        self.ids.prompt.text = ""    

    def image_evaluation(self, file):
        self.doctor.image(file)
        self.show_response(f"\n\n[color=FC0303]You sent an image to the doctor[/color]"+self.doctor.reply)
        os.remove(file)
    
    def get_help(self, hospital):
        if "El Camino Health" == hospital:
            webbrowser.open_new("https://www.getcare.elcaminohealth.org/providers?location=San+Jose%2C+CA")
        elif "Valley Medical" == hospital:
            webbrowser.open_new("https://scvmc.scvh.org/find-provider")

class CameraScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
    def save_image(self):
        camera = self.ids['camera']
        file = f"captured_images/image.png"
        camera.export_to_png(file)
        print("Captured")
        App.get_running_app().root.get_screen("Diagnosis").image_evaluation(file)

class Menu(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class AIlmentsApp(App):
    def build(self):
        return kv

class ChatBot():
    def __init__(self):
        self.client = OpenAI(api_key="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")    
        self.inputList = [{"role": "system", "content": "A doctor that will give a diagnosis and self-treatment that can be done by low-income individuals based on user symptoms."},
                          {"role": "system", "content": "If doctor is not sure, it should ask about more common symptoms that could lead to a diagnosis. Keep the responses brief but useful."},
                          {"role": "system", "content": "When a diagnosis is reached, make sure your reply starts with 'My diagnosis is'. Also include some treatment that can be done at home by low-income individuals."},
                          {"role": "system", "content": "El Camino Health, which has a branch at 2500 Grant Road Cupertino, CA, use the following link: "},
                          {"role": "system", "content": "Valley Medical, which has a branch at 751 S Bascom Ave, San Jose, CA 95128"}]
        self.reply = ""
        
    def image(self, file):
        encoded_img = base64.b64encode(open(file, "rb").read()).decode('utf-8')
        data_url = f"data:image/jpeg;base64,{encoded_img}"

        self.inputList.append({"role": "user", "content": [{"type": "input_image", "image_url": data_url}]}) 
        response = self.client.responses.create(
                        model="gpt-4.1-mini",
                        input=self.inputList
                    )
        
        print(response.output_text)
        self.reply = f"\n\n[color=030FFC]{response.output_text}[/color]"
        self.inputList.append({"role": "assistant", "content": self.reply})
        if 'My diagnosis is' in response.output_text:
            self.recommend_doctor()
            
        return self.reply

    def chat(self, prompt):
        self.inputList.append({"role": "user", "content": [{"type": "input_text", "text": prompt}]}) 

        response = self.client.responses.create(
                        model="gpt-4.1-mini",
                        input=self.inputList
                    )

        self.reply = f"\n\n[color=030FFC]{response.output_text}[/color]"
        self.inputList.append({"role": "assistant", "content": self.reply})
        if 'My diagnosis is' in response.output_text:
            self.recommend_doctor()
            
        return self.reply

kv = Builder.load_file("s4.kv")#I'm always thirsty, experience more urination during night and am tired
AIlmentsApp().run()
