

import dotenv
import deepl

class DeepL_IO():
    def __init__(self):
        return
    
    def openTranslator(self):
        config = dotenv.dotenv_values(".env")
        self.translator = deepl.Translator(auth_key = config.get("translate_deepl_token"),)
        del config
    
    def closeTranslator(self):
        self.translator.close()
    
    def textTranslate(self, text, source_lang, target_lang, glossary):
        if target_lang == "EN":
            target_lang = "EN-US"
        translate_result = self.translator.translate_text(
            text= text, 
            source_lang= source_lang, 
            target_lang= target_lang, 
            glossary= glossary
        )
        return translate_result.text
    
    def setDeeplGlossary(self, novel_title, entries, source_lang, target_lang):
        glossaries = self.translator.list_glossaries()
        for glossary in glossaries:
            if glossary.name == novel_title:
                self.translator.delete_glossary(glossary)
        self.translator.create_glossary(
            novel_title, source_lang, target_lang, entries
        )
    
    def getDeeplGlossary(self, novel_title):
        glossary_list = self.translator.list_glossaries()
        for glossary in glossary_list:
            if glossary.name == novel_title:
                return glossary
    
