

import dotenv
from novelmaster.notion_IO import Notion_IO, BOOK

'''
dotenv.set_key(".env", "token", (token))
'''

class Translate_Notion_IO(Notion_IO):
    def __init__(self):
        config = dotenv.dotenv_values(".env")
        Notion_IO.__init__(self, config.get("translate_notion_token"), 
                           config.get("translate_main_page_id"))
        del config
    
    def novelPageSearch(self, novel_title):
        novel_page_id = self.pageSearch(self.main_page_id, novel_title)
        return novel_page_id
    
    def langPageSearch(self, novel_title, lang):
        novel_page_id = self.novelPageSearch(novel_title)
        if not novel_page_id:
            return
        lang_page_id = self.pageSearch(novel_page_id, lang)
        return lang_page_id
    
    def episodePageSearch(self, novel_title, lang, episode):
        lang_page_id = self.langPageSearch(novel_title, lang)
        if not lang_page_id:
            return
        episode_page_id = self.pageSearch(lang_page_id, episode)
        return episode_page_id
    
    def novelPageCreate(self, novel_title, source_lang, target_lang):
        novel_page_id = self.createNewChildPage(self.main_page_id, novel_title, BOOK)
        self.createNewChildPage(novel_page_id, source_lang, BOOK)
        self.createNewChildPage(novel_page_id, target_lang, BOOK)
        return novel_page_id
    
    def episodePageCreate(self, novel_title, lang, episode):
        lang_page_id = self.langPageSearch(novel_title, lang, episode)
        episode_page_id = self.createNewChildPage(lang_page_id, lang, BOOK)
        return episode_page_id
    
    def episodeUpload(self, novel_title, lang, episode, episode_text):
        episode_page_id = self.novelPageSearch(novel_title)
        if not episode_page_id:
            return
        self.writeText(episode_page_id, episode_text)
        print(self.novel_title + " - episode " + episode + "(" + lang + ") : Notion_uploaded")
    
    def episodeDownload(self, novel_title, lang, episode):
        episode_page_id = self.novelPageSearch(novel_title)
        if not episode_page_id:
            return
        episode_text = self.readText(episode_page_id)
        return episode_text

#%%

'''
notion_client.blocks.children.list()
-> results -> paragraph -> rich_text -> {type:mention} -> plain_text / mention -> page -> id

response(retrieve) -> id

novel_title -> lang -> episode
'''

if __name__ == '__main__':
    io = Translate_Notion_IO()    
    io.createChildPage(
        page_id = io.main_page_id, 
        new_page_title = 'test1', 
        new_page_emoji = BOOK
    )