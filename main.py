from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from selenium import webdriver#type: ignore
from selenium.webdriver.common.by import By #type: ignore
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.common.keys import Keys#type: ignore
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
        self.show_response(f"\n\n[color=FC0303]{self.ids.prompt.text}[/color] \n\n[color=030FFC]{self.doctor.reply}[/color]")
        self.ids.prompt.text = ""    

    def image_evaluation(self, file):
        self.doctor.image(file)
        self.show_response(f"\n\n[color=FC0303]You sent an image to the doctor[/color] \n\n[color=030FFC]{self.doctor.reply}[/color]")
        os.remove(file)
    
    def get_help(self, hospital):
        global driver

        if not driver:
            driver = webdriver.Chrome()
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
        
    def save_image(self):
        camera = self.ids['camera']
        file = f"captured_images/image.png"
        camera.export_to_png(file)
        print("Captured")
        App.get_running_app().root.get_screen("Diagnosis").image_evaluation(file)

class WindowManager(ScreenManager):
    pass

class DiagnoSysApp(App):
    def build(self):
        return kv

class ChatBot():
    def __init__(self):
        self.client = OpenAI(api_key="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")    
        self.inputList = [{"role": "system", "content": "A doctor that will give a diagnosis and self-treatment that can be done by low-income individuals based on user symptoms."},
                          {"role": "system", "content": "If doctor is not sure, it should ask about more common symptoms that could lead to a diagnosis. Keep the responses brief but useful."},
                          {"role": "system", "content": "When a diagnosis is reached, make sure your reply starts with 'My diagnosis is'. Also include some treatment that can be done at home by low-income individuals."},
                          ]
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
    kv = Builder.load_file("s4.kv")#I'm always thirsty, experience more urination during night and am tired. I also have blurry vision and have trouble catching my breath
    DiagnoSysApp().run()
except KeyboardInterrupt:
    try:
        driver.close()
    except AttributeError:
        pass
    os.system('clear')
    exit(0)