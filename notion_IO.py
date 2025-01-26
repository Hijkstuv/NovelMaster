

from notion_client import Client

BOOK = "📖"

'''
notion_client = notion_IO.Client(auth = notion_token)
'''

class Notion_IO(Client):
    def __init__(self, auth: str, main_page_id: str):
        Client.__init__(self, auth = auth)
        self.main_page_id = main_page_id
    
    def childBlockForm(line):
        child_block_form = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": line
                        }
                    }
                ]
            }
        }
        return child_block_form
    
    def writeLine(self, page_id, line):
        self.blocks.children.append(
            block_id = page_id,
            children = [Notion_IO.childBlockForm(line)]
        )
    
    def writeText(self, page_id, text):
        lineList = text.split("\n")
        for line in lineList:
            self.writeLine(line)
    
    def readText(self, page_id):
        text = ""
        child_list = self.blocks.children.list(block_id = page_id)["results"]
        for child in child_list:
            if child["type"] == "paragraph":
                lines = child["paragraph"]["rich_text"]
                for line in lines:
                    text += line["plain_text"]; text += "\n"
        return text
    
    def childPageForm(parent_page_id, new_page_title, new_page_emoji = None):
        child_page_form = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": [
                    {"text": {"content": new_page_title}}
                ]
            }
        }
        if new_page_emoji:
            child_page_form["icon"] = {
                "type": "emoji",
                "emoji": new_page_emoji
            }
        
        return child_page_form
    
    def getChildPageList(self, page_id):
        if not page_id:
            return
        child_list = self.blocks.children.list(block_id = page_id)["results"]
        return child_list
    
    def pageSearch(self, page_id, page_title):
        child_page_list = self.getChildPageList(page_id)
        if not child_page_list:
            return
        for page in child_page_list:
            if page[page["type"]]["title"] == page_title:
                return page["id"]
        return
    
    # create child page and return 
    def createChildPage(self, page_id, new_page_title, new_page_emoji):
        new_page = Notion_IO.childPageForm(page_id, new_page_title, new_page_emoji)
        response = self.pages.create(**new_page)
        return response
    
    # return child page id, if not exist : create child page and return its id
    def createNewChildPage(self, page_id, new_page_title, new_page_emoji):
        child_id = self.pageSearch(page_id, new_page_title)
        if child_id:
            return child_id
        return self.createChildPage(page_id, new_page_title, new_page_emoji)

#%%

'''
paragraph -> rich_text -> {type:mention} -> plain_text / mention -> page -> id
'''
