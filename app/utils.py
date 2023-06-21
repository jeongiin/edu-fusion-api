from translate import Translator

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