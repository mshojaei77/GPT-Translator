import streamlit as st
import fitz  # PyMuPDF
import g4f

def translate_text(text, language):
    prompt = f"""Translate the following text into Native {language},
    ensuring that you fully comprehend the context and accurately convey the intended meanings.
    Special names or technical terms, and paragraphs should remain Untouch.
    **Do not add any additional notes**
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



translated_texts = []
paragraphs_text = ''

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        paragraphs_text = extract_text_by_paragraph(uploaded_file)
    
    if paragraphs_text:
        paragraph_count = len(paragraphs_text)
        for text in paragraphs_text:
            st.write(''.join(text))
    


if paragraphs_text:
    language = st.selectbox('Choose Target Language:', ('Persian', 'English', 'Dutch'))
    if st.button("Translate"):
        progress_text = "Translation in progress. Please wait ..."
        my_bar = st.progress(0, text=progress_text)
        
        for i, text in enumerate(paragraphs_text):
            t_text = translate_text(text, language)
            translated_texts.extend(t_text)
            my_bar.progress((i + 1)/paragraph_count, text=progress_text)
            if language == "Persian":
                st.markdown(f"<div style='direction: rtl;'>{t_text}</div>", unsafe_allow_html=True)
            else:
                st.markdown(t_text)
                
        st.download_button("Download Translation", "".join(translated_texts) )
        
              


            
