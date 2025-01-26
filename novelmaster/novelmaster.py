

from typing import Optional
from novelmaster import line_control, Crawl, DeepL_IO, Translate_Local_IO, Translate_Notion_IO

class NovelMaster(Crawl, DeepL_IO, Translate_Local_IO, Translate_Notion_IO):
    def __init__(self, novel_title, target_lang):
        Translate_Local_IO.__init__(self, novel_title)
        Translate_Notion_IO.__init__(self)
        DeepL_IO.__init__(self)
        self.novel_title = novel_title
        # if self.isNew():
        #    self.newnovel(**novel_info)
        self.getInfo()
        if self.novel_title != self.info["novel_title"]:
            print("title invalid")
            return
        self.getGlossary()
        self.getProgress()
        self.target_lang = target_lang

    # isNew
    '''
    isNew():
    distinguish new or remaining novel, with novel_title
    
    newnovel():
    create info.json, progress.json, glossary.json file with setted form
    create new directory -> os.mkdir(), os.makedirs()
        
    -------
    # info
    {
        "novel_title": "(novel_title)"
        "novel_type": "(novel_type)" <- to determine crawl method. "syosetu"
        "target_url": "(target_url)" <- ex) "https://ncode.syosetu.com/n7637dj/"
        "episode_size": "(episode_size)" <- ex) 223
        "source_lang": "(source_lang" <- ex) "JA"
    }
    
    # progress
    {
        "episode_dict": {
            "(episode)": "(state)"
            ...
        }
    }
    
    #glossary
    {
        "entries": {
            "(source_word)": "(target_word)"
            ...
        }
    }
    -------
    '''

    # crawl
    def syosetuMultiCrawl(self):
        self.openBrowser()        
        for episode in self.progress["episode_dict"].keys(): 
            text = self.syosetuCrawl(self.info["target_url"], episode)
            self.writeEpisode(self.novel_title, "ORI", episode, text)
            self.progress["episode_dict"][episode] = "Crawled"
        self.closeBrowser()
    
    # postprocessing
    def postprocessing(self):
        for episode in self.progress["episode_dict"].keys():
            text = self.readEpisode(self.novel_title, "ORI", episode)
            lineList = line_control.textToLineList(text, self.info["source_lang"])
            for line in lineList:
                line.clearify()
            text = line_control.lineListToText(lineList)
            self.txtWrite(self.novel_title, self.info["source_lang"], episode, text)
            self.progress["episode_dict"][episode] = "Postprocessed"
            print(self.novel_title + " - episode " + episode + " : Postprocessed")
    
    #set target_lang | JA, KO, EN, etc
    def setTargetLang(self, target_lang):
        self.target_lang = target_lang
    
    # open translator
    def translateSetup(self):
        self.openTranslator()        
        self.setDeeplGlossary(
            self.novel_title, 
            self.glossary["entries"], 
            self.info["source_lang"], 
            self.target_lang)
        self.deepl_glossary = self.getDeeplGlossary(self.novel_title)
    
    def episodeTranslate(self, episode):
        text = self.readEpisode(self.info["source_lang"], episode)
        translated_text = self.textTranslate(text, self.info["source_lang"], 
                                             self.target_lang, self.deepl_glossary)
        self.writeEpisode(self.target_lang, episode, translated_text)
    
    # translate for automatic, with work count
    def novelTranslate_count(self, work_limit):
        work_count = 0
        for episode in self.progress["episode_dict"].keys():
            if work_count == work_limit:
                break
            if self.progress["episode_dict"][episode] == "Postprocessed":
                self.episodeTranslate(episode)
                self.progress["episode_dict"][episode] = "Translated"
                print(self.novel_title + " - episode " + episode + " : Translated")
                work_count += 1    
        self.setProgress()
    
    # append local glossary
    def appendGlossary(self, new_word_pairs: Optional[dict] = None):
        if new_word_pairs:
            self.glossary["entries"].update(new_word_pairs)
        else:
            source_word = input("source_word : ")
            target_word = input("target_word : ")
            word_pair = {source_word: target_word}
            self.appendGlossary(word_pair)
        self.setGlossary()
    
    #search local glossary
    def searchGlossary(self):
        source_word = input("source_word(or press Enter) : ")
        if source_word != "":
            if source_word in self.glossary["entries"].keys():
                print("<<target_word>>\n" + self.glossary["entries"][source_word])
            else:
                print("no such source_word")
                return
        target_word = input("target_word : ")
        source_word = [key for key, value in self.glossary["entries"].items() 
                       if value == target_word]
        if source_word != []:
            print("<<source_word>>")
            for word in source_word:
                print(word)
        else:
            print("no such target_word")
    
    '''
    # upload novel to notion page 
    def notion_novelUpload(self):
        for episode in self.progress["episode_dict"].keys():
            if self.progress["episode_dict"][episode] == "Postprocessed":
                self.episodeUpload(self.novel_title, self.info["source_lang"], episode)
    '''
