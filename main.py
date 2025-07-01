from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from openai import OpenAI
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
        self.inputList = [{"role": "system", "content": "A doctor that will give a diagnosis based on user symptoms."},
                          {"role": "system", "content": "If doctor is not sure, it should ask about more common symptoms that could lead to a diagnosis. Keep the responses brief but useful."},
                          {"role": "system", "content": "When a diagnosis is reached, recommend a doctor they could go to and make sure to end your response with 'any other doctor you feel comfortable with.'"},
                          {"role": "system", "content": "To choose a doctor from El Camino Health, which has a branch at 2500 Grant Road Cupertino, CA, use the following link: https://www.getcare.elcaminohealth.org/providers?location=San+Jose%2C+CA"},
                          {"role": "system", "content": "To choose a doctor from Valley Medical, which has a branch at 751 S Bascom Ave, San Jose, CA 95128, use the following link: "}]
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

        os.remove(file)
            
        return self.reply

    def chat(self, prompt):
        self.inputList.append({"role": "user", "content": [{"type": "input_text", "text": prompt}]}) 

        response = self.client.responses.create(
                        model="gpt-4.1-mini",
                        input=self.inputList
                    )

        self.reply = f"\n\n[color=030FFC]{response.output_text}[/color]"
        self.inputList.append({"role": "assistant", "content": self.reply})
            
        return self.reply

kv = Builder.load_file("s4.kv")
AIlmentsApp().run()
