

import os
import json

class Local_IO():
    def __init__(self):
        return
    
    def txtRead(self, file_dir):
        if not os.path.isfile(file_dir):
            return
        f = open(file_dir, 'r', encoding = 'UTF8')
        lines = f.readlines()
        f.close()
        text = ""
        for line in lines:
            text += line
        return text
    
    def txtWrite(self, file_dir, text):
        f = open(file_dir, 'w', encoding = 'UTF8')
        f.write(text)
        f.close()
    
    def jsonRead(self, file_dir):
        if not os.path.isfile(file_dir):
            return
        with open(file_dir, encoding= 'UTF-8') as f:
            data = json.load(f)
        f.close()
        return data
    
    def jsonWrite(self, file_dir, data):
        with open(file_dir, 'w', encoding= 'UTF-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        f.close()
    
    def join(self, path, *paths):
        return os.path.join(path, *paths)
