import fitz  # PyMuPDF
import os
import g4f

class PDFTranslator:
    def __init__(self, pdf_filename, output_txt_filename):
        self.pdf_filename = pdf_filename
        self.output_txt_filename = output_txt_filename
        self.script_dir = os.path.dirname(__file__)
        self.pdf_path = os.path.join(self.script_dir, self.pdf_filename)
        self.output_txt_path = os.path.join(self.script_dir, self.output_txt_filename)

    def translate_text(self, text, language):
        prompt = f"""Translate the following text into Native {language},
        ensuring that you fully comprehend the context and accurately convey the intended meanings.
        Special names, technical or professional terms, and paragraphs should remain in English.
        \n
        \n
        "{text}"
        \n
        \n 
        **Do not add any additional notes**
        """
        providers = [
            g4f.Provider.Bing, g4f.Provider.Aichatos,
            g4f.Provider.GeekGpt, g4f.Provider.Liaobots,
            g4f.Provider.Phind, g4f.Provider.HuggingChat
        ]
        for provider in providers:
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    provider=provider,
                    messages=[{"role": "system", "content": "you are a professional translator"},
                              {"role": "user", "content": prompt}],
                )
                translated_text = response
                return translated_text
            except Exception as e:
                print(f"Translation failed with provider {provider}: {e}")
                continue
        return "Translation failed"

    def extract_text_by_paragraph(self):
        try:
            document = fitz.open(self.pdf_path)
            
            all_text = []
            
            for page_num in range(document.page_count):
                page = document.load_page(page_num)
                text = page.get_text()
                paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by two newline characters
                all_text.extend(paragraphs)
            
            return all_text
        
        except Exception as e:
            print(f"Error occurred while extracting text from PDF: {e}")
            return []


    def write_to_txt(self, translated_texts):
        try:
            if os.path.exists(self.output_txt_path):
                print("Output TXT file already exists. Skipping writing to prevent overwrite.")
                return

            with open(self.output_txt_path, 'w', encoding='utf-8') as txt_file:
                for text in translated_texts:
                    txt_file.write(text + '\n')
            print(f"Translated text written to {self.output_txt_path}")
        except Exception as e:
            print(f"Error occurred while writing to TXT: {e}")

    def translate_pdf_to_txt(self):
        if not os.path.exists(self.pdf_path):
            print(f"File not found: {self.pdf_path}")
            return

        try:
            paragraphs_text = self.extract_text_by_paragraph()
            if not paragraphs_text:
                print("No text found in the PDF.")
                return

            paragraph_count = len(paragraphs_text)
            print(f"Total number of paragraphs: {paragraph_count}")

            translated_texts = []
            for i, paragraph_text in enumerate(paragraphs_text):
                print(f"Translating paragraph {i + 1}/{paragraph_count} ...")
                translated_text = self.translate_text(paragraph_text, "Persian (Farsi)")
                translated_texts.append(translated_text)

            if translated_texts:
                self.write_to_txt(translated_texts)
            else:
                print("No translated text to write to TXT.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    pdf_filename = 'example.pdf'
    output_txt_filename = f"{pdf_filename}_translated.txt"
    translator = PDFTranslator(pdf_filename, output_txt_filename)
    translator.translate_pdf_to_txt()