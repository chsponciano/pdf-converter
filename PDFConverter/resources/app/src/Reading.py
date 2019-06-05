import os
import re
import io
import unicodedata
from time import strftime
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from docx import Document
from docx.shared import Inches
from googletrans import Translator
from googletrans.gtoken import TokenAcquirer

class Reading:

    def select_file(self, directory):
        list_file = []

        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.pdf'):
                    t = os.path.join(directory, filename)
                    list_file.append(t)

        return list_file

    def convert_pdf_to_str(self, path, lang='pt'):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(fp, set(), maxpages=0, password="", caching=True, check_extractable=True):
            interpreter.process_page(page)

        text = self.translate(retstr.getvalue())
        
        fp.close()
        device.close()
        retstr.close()
        return text

    def translate(self, text_orig, src='en', dest='pt'):
        i_counter = 0
        f_counter = 0
        increment = False
        text_dest = ''

        while f_counter < len(text_orig):
            if increment:
                i_counter = f_counter + 1
            else:
                increment = True

            if (f_counter + 5000) > len(text_orig):
                f_counter = i_counter + (len(text_orig) % 5000)
            else:
                f_counter = f_counter + 5000

            text_inc = text_orig[i_counter:f_counter]
            translator = Translator()
            acquirer = TokenAcquirer()
            acquirer.do(text_inc)
            text_dest = text_dest + translator.translate(text_inc, src=src, dest=dest).text

        return text_dest


    def convert_str_to_docx(self, text, name_file):
        document = Document()
        document.add_paragraph(text)
        document.save(name_file)

    def remove_special_characters (self, text):
        return re.sub('[^a-zA-Z0-9áàéèêâãõóòúùíìÁÀÉÈÊÂÃÕÓÒÚÙÍÌ\n\.\,\!\?\%\&\" \\\]', '', text)

    def convert(self, dir_file):
        head, tail = os.path.split(dir_file)
        var = "\\"
        tail = tail.replace(".pdf", ".docx")
        name = head + var + tail
        content_list = self.remove_special_characters(self.convert_pdf_to_str(dir_file)).split("\n")
        content = ""

        for c in content_list:
            if len(c) > 2:
                content += c
                content += "\n" if c.endswith(".") else " "

        self.convert_str_to_docx(content, name)

        return strftime("%H:%M:%S") + " pdf -> docx | Novo Arquivo: " + tail
