from kivy.uix.actionbar import BoxLayout
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
from selenium import webdriver#type: ignore
from selenium.webdriver.common.by import By #type: ignore
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.common.keys import Keys#type: ignore
from selenium.webdriver.chrome.service import Service
from openai import OpenAI
import io
import base64
from PIL import Image
import base64
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Home(Screen):
    pass

class About(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.logo_path = resource_path(os.path.join("images", "logo.png"))
        self.person1_path = (resource_path(os.path.join("images", "person1.png")))
        self.person2_path = (resource_path(os.path.join("images", "person2.png")))
        self.person3_path = (resource_path(os.path.join("images", "person3.png")))

class Diagnosis(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.doctor = ChatBot()
        self.logo_path = resource_path(os.path.join("images", "logo.png"))
        self.doc_image_path = (resource_path(os.path.join("images", "doctor.png")))
        self.cam_image_path = (resource_path(os.path.join("images", "camera.png")))
        self.call_image_path = (resource_path(os.path.join("images", "call.png")))
        Clock.schedule_once(self.get_api, 0)
    
    def open_help_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=8, padding=8)

        b1 = Button(text='El Camino Health', size_hint_y=None, height='48dp')
        def on_elcamino(btn):
            self.get_help("El Camino Health")
            popup.dismiss()
        b1.bind(on_release=on_elcamino)

        b2 = Button(text='Valley Medical', size_hint_y=None, height='48dp')
        def on_valley(btn):
            self.get_help("Valley Medical")
            popup.dismiss()
        b2.bind(on_release=on_valley)

        layout.add_widget(b1)
        layout.add_widget(b2)

        popup = Popup(
            title="Choose a hospital",
            content=layout,
            size_hint=(0.6, 0.2),
            pos_hint={"x": 0.2, "top": 0.9},
            auto_dismiss=False
        )
        popup.open()
    
    def get_api(self, instance):
        self.text_input = TextInput(hint_text="Enter your OpenAI Api key", size_hint_y=None, height='48dp')
        submit_button = Button(text="Submit", size_hint_y=None, height='48dp', on_press=self.submit_api)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.text_input)
        layout.add_widget(submit_button)

        self.popup = Popup(title="Enter Api key",
                            content=layout,
                            size_hint=(0.6, 0.2),
                            pos_hint={"x": 0.2, "top": 0.9},)
        self.popup.open()
        
    def submit_api(self, instance):
        self.doctor.api_key = self.text_input.text
        self.doctor.client = OpenAI(api_key=self.doctor.api_key)

        self.popup.dismiss()

    def show_response(self, message):
        self.ids.response.text += message
        self.ids.response.parent.scroll_y = 0
    
    def text_inquiry(self):
        self.doctor.chat(self.ids.prompt.text)
        self.show_response(f"\n\n[color=FC0303]{self.ids.prompt.text}[/color] \n\n[color=030FFC]{self.doctor.reply}[/color]")
        self.ids.prompt.text = ""    

    def image_evaluation(self, data_url):
        self.doctor.image(data_url)
        self.show_response(f"\n\n[color=FC0303]You sent an image to the doctor[/color] \n\n[color=030FFC]{self.doctor.reply}[/color]")
    
    def get_help(self, hospital):
        global driver

        if not driver:
            driver = webdriver.Chrome(service=Service(executable_path=resource_path('chromedriver.exe')))
            driver.get("https://www.dhcs.ca.gov/services/medi-cal/Pages/Transportation.aspx")
            driver.switch_to.new_window(WindowTypes.TAB)
        else:
            driver.switch_to.new_window(WindowTypes.TAB)    
        if "El Camino Health" == hospital:
            driver.get("https://www.getcare.elcaminohealth.org/providers?location=San+Jose%2C+CA")
            condition = self.doctor.chat("What is my condition? resposne should be only the name of the condition. If you have no clue what my condition is, respond with only 'None'")
            if condition != "None":
                print(condition)
                input_field = driver.find_element(By.XPATH, "//input[@aria-label='Refine your search' and @id='clinicianInput']")
                input_field.send_keys(condition)
                input_field.send_keys(Keys.ENTER)
        elif "Valley Medical" == hospital:
            categories = ['Anesthesiology', 'Anesthesiology: Critical Care Medicine', 'Anesthesiology: Pain Medicine', 'Anesthesiology: Pediatric Anesthesiology', 'Audiologist', 'Cardiothoracic Vascular Surgery', 'Dentist', 'Dentist: General Practice', 'Dentist: Oral and Maxillofacial Surgery', 'Dentistry', 'Dermatology', 'Emergency Medicine', 'Family Medicine', 'Family Medicine: Geriatric Medicine', 'Family Medicine: Hospice and Palliative Medicine', 'General Practice', 'Hospice & Palliative Medicine', 'Internal Medicine', 'Internal Medicine: Addiction Medicine', 'Internal Medicine: Adolescent Medicine', 'Internal Medicine: Allergy & Immunology', 'Internal Medicine: Cardiovascular Disease', 'Internal Medicine: Critical Care Medicine', 'Internal Medicine: Endocrinology, Diabetes and Metabolism', 'Internal Medicine: Gastroenterology', 'Internal Medicine: Geriatric Medicine', 'Internal Medicine: Hematology & Oncology', 'Internal Medicine: Hospice and Palliative Medicine', 'Internal Medicine: Infectious Disease', 'Internal Medicine: Interventional Cardiology', 'Internal Medicine: Nephrology', 'Internal Medicine: Pulmonary Disease', 'Internal Medicine: Rheumatology', 'Internal Medicine: Sleep Medicine', 'Maternal Fetal Medicine', 'Medical Genetics: Clinical Genetics (M.D.)', 'Neurological Surgery', 'Neurophysiologist', 'Neuropsychologist: Clinical', 'Nuclear Medicine', 'Nurse Anesthetist: Certified Registered', 'Nurse Practitioner', 'Nurse Practitioner: Acute Care', 'Nurse Practitioner: Adult Health', 'Nurse Practitioner: Community Health', 'Nurse Practitioner: Family', 'Nurse Practitioner: Gerontology', 'Nurse Practitioner: Neonatal, Critical Care', 'Nurse Practitioner: Obstetrics & Gynecology', 'Nurse Practitioner: Occupational Health', 'Nurse Practitioner: Pediatrics', 'Nurse Practitioner: Perinatal', 'Nurse Practitioner: Psych/Mental Health', 'Nurse Practitioner: Womens Health', 'Obstetrics & Gynecology', 'Obstetrics & Gynecology: Gynecologic Oncology', 'Ophthalmology', 'Optometrist', 'Orthopaedic Surgery', 'Orthopaedic Surgery: Orthopaedic Trauma', 'Orthopaedic Surgery: Pediatric Orthopaedic Surgery', 'Otolaryngology', 'Otolaryngology: Facial Plastic Surgery', 'Pathology', 'Pathology: Anatomic Pathology', 'Pathology: Clinical Pathology/Laboratory Medicine', 'Pediatrics', 'Pediatrics: Adolescent Medicine', 'Pediatrics: Developmental & Behavioral Pediatrics', 'Pediatrics: Neonatal-Perinatal Medicine', 'Pediatrics: Neurodevelopmental Disabilities', 'Pediatrics: Pediatric Cardiology', 'Pediatrics: Pediatric Critical Care Medicine', 'Pediatrics: Pediatric Endocrinology', 'Pediatrics: Pediatric Gastroenterology', 'Pediatrics: Pediatric Infectious Diseases', 'Pediatrics: Pediatric Nephrology', 'Pediatrics: Pediatric Pulmonology', 'Perfusionist', 'Physical Medicine & Rehabilitation', 'Physical Medicine & Rehabilitation: Pediatric Rehabilitatio', 'Physical Medicine & Rehabilitation: Spinal Cord Injury Medi', 'Physician Assistant', 'Physician Assistant: Medical', 'Physician Assistant: Surgical', 'Plastic Surgery', 'Podiatry', 'Podiatry: Foot & Ankle Surgery', 'Preventive Medicine: Clinical Informatics', 'Psychiatry', 'Psychiatry & Neurology, Clinical Neurophysiology', 'Psychiatry & Neurology: Child & Adolescent', 'Psychiatry & Neurology: Child & Adolescent Psychiatry', 'Psychiatry & Neurology: Neurocritical Care', 'Psychiatry & Neurology: Neurology', 'Psychiatry & Neurology: Neurology with Special Qualificatio', 'Psychiatry & Neurology: Psychiatry', 'Psychiatry & Neurology: Sleep Medicine', 'Psychiatry & Neurology: Vascular Neurology', 'Psychiatry and Neurology: Neurology', 'Psychologist', 'Psychologist: Clinical', 'Radiology', 'Radiology: Diagnostic Radiology', 'Radiology: Interventional Radiology and Diagnostic Radiology -General', 'Radiology: Neuroradiology', 'Radiology: Pediatric Radiology', 'Radiology: Radiation Oncology', 'Radiology: Vascular and Interventional Radiology', 'Social Worker', 'Social Worker: Clinical', 'Student in an Organized Health Care Education/Training Progr', 'Surgery', 'Surgery: General Surgery', 'Surgery: Pediatric Surgery', 'Surgery: Plastic and Reconstructive Surgery', 'Surgery: Surgical Critical Care', 'Surgery: Trauma Surgery', 'Surgery: Vascular Surgery', 'Surgical Critical Care', 'Teleradiology', 'Thoracic Surgery', 'Thoracic Surgery: Cardiothoracic Vascular Surgery', 'Urology']
            driver.get("https://scvmc.scvh.org/find-provider")
            self.doctor.chat(f"of the folowing categories, apply to my condition? The response should be only space seperated integers representing the indexes of the ones that apply in the 0-indexed list:{categories}")
            driver.find_element(By.XPATH, "(//button[contains(@class, 'usa-accordion-button') and contains(@class, 'usa-accordion__button')])[1]").click()
            for i in self.doctor.reply.split():
                driver.find_elements(By.XPATH, "(//div[contains(@class, 'form-checkboxes') and contains(@class, 'bef-checkboxes')])[1]//div//label")[int(i)].click()


class CameraScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.logo_path = resource_path(os.path.join("images", "logo.png"))
        
    def save_image(self):
        camera = self.ids['camera']
        texture = camera.texture
        
        pixels = texture.pixels 
        width, height = texture.size
        image = Image.frombytes('RGBA', (width, height), pixels)
        image = image.convert('RGB')

        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        jpeg_bytes = buffer.getvalue()
        buffer.close()

        encoded_img = base64.b64encode(jpeg_bytes).decode('utf-8')
        data_url = f"data:image/jpeg;base64,{encoded_img}"
        App.get_running_app().root.get_screen("Diagnosis").image_evaluation(data_url)

class WindowManager(ScreenManager):
    pass

class DiagnoSysApp(App):
    def build(self):
        return kv

class ChatBot():
    def __init__(self):
        self.inputList = [{"role": "system", "content": "A doctor that will give a diagnosis and self-treatment that can be done by low-income individuals based on user symptoms."},
                          {"role": "system", "content": "If doctor is not sure, it should ask about more common symptoms that could lead to a diagnosis. Keep the responses brief but useful."},
                          {"role": "system", "content": "When a diagnosis is reached, make sure your reply starts with 'My diagnosis is'. Also include some treatment that can be done at home by low-income individuals."},
                          {"role": "system", "content": "Your name is DiagnoSys"},
                          ]
        self.reply = ""
        
    def image(self, data_url):
        self.inputList.append({"role": "user", "content": [{"type": "input_image", "image_url": data_url}]}) 
        response = self.client.responses.create(
                        model="gpt-4.1-mini",
                        input=self.inputList
                    )
        
        print(response.output_text)
        self.reply = response.output_text
        self.inputList.append({"role": "assistant", "content": self.reply})
            
        return self.reply

    def chat(self, prompt):
        self.inputList.append({"role": "user", "content": [{"type": "input_text", "text": prompt}]}) 

        response = self.client.responses.create(
                        model="gpt-4.1-mini",
                        input=self.inputList
                    )

        self.reply = response.output_text
        self.inputList.append({"role": "assistant", "content": self.reply})
            
        return self.reply

driver = None
try:
    kv = Builder.load_file(resource_path("diagnosys.kv"))
    DiagnoSysApp().run()
except KeyboardInterrupt:
    try:
        driver.close()
    except AttributeError:
        pass
    os.system('clear')
    exit(0)