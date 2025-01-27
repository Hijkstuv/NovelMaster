

from novelmaster.local_IO import Local_IO

class Translate_Local_IO(Local_IO):
    def __init__(self, novel_title):
        Local_IO.__init__(self)
        self.novel_title = novel_title
        self.base_dir = "C://Task//Translate" # Change this directory, if you need

    def readEpisode(self, lang, episode):
        file_dir = self.join(self.base_dir, self.novel_title, lang, episode + ".txt")
        episode_text = self.txtRead(file_dir)
        return episode_text
    
    def writeEpisode(self, lang, episode, episode_text):
        file_dir = self.join(self.base_dir, self.novel_title, lang, episode + ".txt")
        self.txtWrite(file_dir, episode_text)
    
    def getGlossary(self):
        self.glossary = self.jsonRead(self.join(self.base_dir, self.novel_title, "glossary.json"))
    
    def setGlossary(self):
        self.jsonWrite(self.join(self.base_dir, self.novel_title, "glossary.json"), self.glossary)
    
    def getInfo(self):
        self.info = self.jsonRead(self.join(self.base_dir, self.novel_title, "info.json"))
    
    def setInfo(self):
        self.jsonWrite(self.join(self.base_dir, self.novel_title, "info.json"), self.info)

    def getProgress(self):
        self.progress = self.jsonRead(self.join(self.base_dir, self.novel_title, "progress.json"))
    
    def setProgress(self):
        self.jsonWrite(self.join(self.base_dir, self.novel_title, "progress.json"), self.progress)
