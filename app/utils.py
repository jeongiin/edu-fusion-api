from translate import Translator
import os

def ko_to_en(text : str):
    translator = Translator(from_lang="ko", to_lang="en")
    
    return translator.translate(text)

def en_to_ko(text : str):
    translator = Translator(from_lang="en", to_lang="ko")

    return translator.translate(text)

def save_txt_file(save_path : str,text : str):
    with open(save_path, "w") as file:
        file.write(text)
    file.close()

def create_base_path(edu_class_folder_name, edu_title_file_name):
    base_path = os.path.join(os.getcwd(), "app", "data", edu_class_folder_name, edu_title_file_name)   # docker
    # base_path = os.path.join(os.getcwd(), "data", edu_class_folder_name, edu_title_file_name)   # docker
    
    return base_path