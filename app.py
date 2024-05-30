import streamlit as st
from agent import extract_text_by_paragraph, translate_text



st.set_page_config(
    page_title="GPT-Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'http://t.me/mshojaei77',
        'Report a bug': "http://t.me/shojaeireal",
    }
)

translated_texts = []
paragraphs_text = ''
btn = False

tab1, tab2= st.tabs(["Translation" , "Orginal Text"])

with st.sidebar:
    st.header("Settings", divider='gray')
    prov = st.selectbox('Choose Translation Provider:', ('Free (Slow)', 'OpenAI', 'Groq'))
    if prov == 'OpenAI':
        key = st.text_input("Enter Your API key", type="password")
        model =  st.selectbox('Choose LLM Model:', ('gpt-3.5-turbo', 'gpt-4o', 'gpt-4-turbo','gpt-4'))
    elif prov == 'Groq':
        key = st.text_input("Enter Your API key", type="password")
        model =  st.selectbox('Choose LLM Model:', ('llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'))
    else:
        key = None
        model = None


    mode = st.radio(
        "Choose Input mode",
        ["PDF file", "Text"],
        captions = ["Upload a pdf.", "input your text."])


 
with tab1:
    if mode == "PDF file":
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file:
            paragraphs_text = extract_text_by_paragraph(uploaded_file) 
    else:
        paragraphs_text = st.text_input("Enter the text").split("\n\n")
        
    language = st.selectbox('Choose Target Language:', ('Persian', 'English', 'Dutch'))
    btn = st.button("Translate")
    if paragraphs_text:
        paragraph_count = len(paragraphs_text)
        if btn:
            progress_text = "Translation in progress. Please wait ..."
            my_bar = st.progress(0, text=progress_text)

            for i, text in enumerate(paragraphs_text):
                t_text = translate_text(text, language , prov , model, key)
                translated_texts.extend(t_text)
                my_bar.progress((i + 1)/paragraph_count, text=progress_text)
                if language == "Persian":
                    st.markdown(f"<div style='direction: rtl;'>{t_text}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(t_text)

            my_bar.empty()
            st.success("Translation finished!")
            st.download_button("Download Translation", "".join(translated_texts))

    
with tab2:
    for text in paragraphs_text:
        st.write(''.join(text))   
