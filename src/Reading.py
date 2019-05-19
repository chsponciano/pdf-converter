import io
import os
import re
import unicodedata
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from os import chdir, getcwd, listdir, path
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from py_translator import TEXTLIB
from time import strftime
from docx import Document
from docx.shared import Inches

class Reading:

    def convert_pdf_to_str(self, path, lang='pt'):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(fp, set(), maxpages=0, password="", caching=True, check_extractable=True):
            interpreter.process_page(page)

        text = TEXTLIB().translator(is_html=False, text=retstr.getvalue(), lang_to=lang, proxy=False)
        
        fp.close()
        device.close()
        retstr.close()
        return text

    def convert_str_to_docx(self, text, name_file):
        document = Document()
        document.add_paragraph(text)
        document.save(name_file)

    def remove_special_characters (self, text):
        return re.sub('[^a-zA-Z0-9áàéèêâãõóòúùíìÁÀÉÈÊÂÃÕÓÒÚÙÍÌ\n\.\,\!\?\%\&\" \\\]', '', text)

    def select_file(self, directory):
        list_file = []

        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.pdf'):
                    t = os.path.join(directory, filename)
                    list_file.append(t)

        return list_file

    def convert(self, dir_file):
        head, tail = os.path.split(dir_file)
        var = "\\"
        tail = tail.replace(".pdf", ".docx")
        name= head + var + tail
        content_list = self.remove_special_characters(self.convert_pdf_to_str(dir_file)).split("\n")
        content = ""

        for c in content_list:
            if len(c) > 2:
                content += c
                content += "\n" if c.endswith(".") else " "

        self.convert_str_to_docx(content, name)

        return strftime("%H:%M:%S") + "pdf -> docx | Novo Arquivo: " + tail
