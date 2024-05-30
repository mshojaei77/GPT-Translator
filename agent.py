import fitz  # PyMuPDF
import g4f
import openai
import groq


def translate_text(text, language, prov, model, key):
    prompt = f"""Translate the following text into Native {language}, 
    ensuring that you fully comprehend the context and accurately convey the intended meanings.
    **the output must be just translation**
    \n
    \n
    "{text}"
    \n
    \n
    """
    if prov == 'Free (Slow)':
        providers = [
            g4f.Provider.Bing, g4f.Provider.Liaobots,
            g4f.Provider.Aichatos, g4f.Provider.GeekGpt,
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
                return response
            except Exception as e:
                print(f"Translation failed with provider {provider}: {e}")
                continue
            
    elif prov == 'OpenAI':
        client = openai.OpenAI(api_key=key)
        completion = client.chat.completions.create(
            model= model,
            messages=[
                {"role": "system", "content": "you are a professional translator"},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    elif prov == 'Groq':
        client = groq.Groq(api_key=key)
        completion = client.chat.completions.create(
            model= model,
            messages=[
                {"role": "system", "content": "you are a professional translator"},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    
    

def extract_text_by_paragraph(uploaded_file):
    try:
        document = fitz.open(uploaded_file)
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