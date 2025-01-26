

class Line():
    EndMark = {"JA": "。", "EN": ".", "KO": "."}
    QuestionMark = {"JA": "？", "EN": "?", "KO": "?"}
    ExclamationMark = {"JA": "！", "EN": "!", "KO": "!"}
    
    def __init__(self, text, lang):
        self.text = text
        self.lang = lang
        
    def getText(self):
        return self.text

    def putEndmark(self):
        if len(self.text) < 2:
            return
        if self.text[-1] == "\"" and (not self.text[-2] in [
                Line.EndMark[self.lang], 
                Line.QuestionMark[self.lang], 
                Line.ExclamationMark[self.lang]
                ]):
            tempText = ""
            for i in range(len(self.text)):
                if i < len(self.text) - 1:
                    char = self.text[i]
                    tempText += char
                else:
                    tempText += Line.EndMark[self.lang] + "\""
            self.text = tempText
            return

    def transChar(char):
        if char in ["「", "」"]:
            return "\"" 
        if char in ["【", "『"]:
            return "["
        elif char in ["】", "』"]:
            return "]"
        elif char == "　": # 일본어 공백
            return " "
        else:
            return char

    def transLine(self):
        temptext = ""
        for char in self.text:
            char = Line.transChar(char)
            temptext += char
        self.text = temptext

    def clearify(self):
        self.transLine()
        self.putEndmark()

def textToLineList(text, lang):
    lineList = []
    lines = text.split('\n')
    for line in lines:
        lineList.append(Line(line, lang))
    return lineList

def lineListToText(lineList):
    text = ""
    for line in lineList:
        text += line.text
        text += "\n"
    return text