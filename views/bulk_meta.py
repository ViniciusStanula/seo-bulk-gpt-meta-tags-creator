import streamlit as st
import pandas as pd
from pyexcelerate import Workbook
import functions as fc
import openai
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import streamlit_antd_components as sac
import pandas as pd
import io

buffer = io.BytesIO()

@st.cache_data(show_spinner=False)
def carregar_modulos_nltk():
    # Baixa os módulos 'stopwords' e 'punkt' do NLTK
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    # Retorna True para indicar que os módulos foram baixados e armazenados em cache
    return True

# Função para pré-processamento de texto
def preprocess_text(text):
    # Crie um objeto lematizador para o português
    lemmatizer = WordNetLemmatizer()
    
    if st.session_state.language == 'English':
        # Obtenha as palavras de parada em português
        palavras_de_parada = set(stopwords.words('english'))    
    elif st.session_state.language == 'Portuguese (Brazil)':
        # Obtenha as palavras de parada em português
        palavras_de_parada = set(stopwords.words('portuguese'))

    # Divida o texto em palavras
    palavras = text.split()

    # Aplique lematização e remova as palavras de parada e os espaços em branco
    palavras_filtradas = [lemmatizer.lemmatize(palavra) for palavra in palavras if palavra.lower() not in palavras_de_parada and palavra.strip() != '']

    # Reconstrua o texto a partir das palavras filtradas
    texto_processado = ' '.join(palavras_filtradas)
    
    return texto_processado


def createPage():
    carregar_modulos_nltk()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
        
    if 'api' not in st.session_state:
        st.session_state.api = 'api-key'
        
    if 'button_proceed' not in st.session_state:
        st.session_state.button_proceed = False
    
    if 'df_resultado' not in st.session_state:
        st.session_state.df_resultado = None
        
    if 'meta' not in st.session_state:
        st.session_state.meta = None
        
           
    # Criando duas colunas para layout
    colunhead, colundhead2 = st.columns([0.06, 0.99])
    
    # Inserindo animação na primeira coluna
    with colunhead:
        st.image(fc.open_image("./assets/robozin2.png"))

    # Inserindo informações de contatos na segunda coluna
    with colundhead2:
        st.header("Bulk Meta Tags Creator")
        st.markdown('<p class="minha-classe">By <a href="https://viniciusstanula.com/en/">Vinicius Stanula</a>, made in Streamlit 🎈</p>', unsafe_allow_html=True)
        
    with st.expander('ℹ️ - About the App'):
        st.markdown("""
                 This web application is designed for creating SEO-friendly titles and descriptions either individually or in bulk using .xlsx files.
                    \n **Benefits of this app**:
                    \n- You can achieve around a 30% reduction in token usage with the API, and that means saving money.
                    \n - You can bulk create meta tags with a simple upload of an .xlsx file. With that, each row in your file will generate a unique prompt based on the provided information. This results in personalized prompts for each URL.""")
                      
   
    tab1, tab2 = st.tabs(['Single Creator', 'Bulk Creator'])
    
    with tab1:
        container_single = st.container()
        container_config = st.container()
        container_upload = st.container()
        container_result = st.container()       
        c1, c2, c3 = st.columns(3)
        
        with container_config:
            with c1:
                c1col1, c1col2 = st.columns(2)
                
                index = 0
                
                with c1col1:      
                    st.session_state.language = st.selectbox('Choose your Language:', ('English', 'Portuguese (Brazil)'))
                with c1col2:
                    st.session_state.api = st.text_input('Open API Key:', value=st.session_state.api)
                    
                if st.session_state.language == 'English':
                    persona = st.text_input('Your Persona Here', 'Passionate about technology', help='This persona is going to be inserted into the prompt. You can check the full AI persona below')
                    with st.expander("📏 - Change Meta's size"):
                        title_caract = st.slider('Maximum characters for Title:', 0, 70, 60)
                        desc_caract = st.slider('Maximum characters for Description:', 0, 170, 155)
                    with st.expander('🤖 - GPT Bot:', expanded=True):
                        st.markdown(f'🤖 - I am an SEO specialist writer, **{persona}**, and I love to write in a natural and engaging manner in {st.session_state.language}. My approach is to create meta titles and descriptions that truly captivate readers and help products stand out on search engines.')
                    button_proceed = st.button('Proceed to Page Details ➡️')
                elif st.session_state.language == 'Portuguese (Brazil)':
                    persona = st.text_input('Sua Persona aqui', 'Apaixonado por tecnologia')
                    with st.expander("📏 - Tamanho das Meta Tags"):
                        title_caract = st.slider('Maximum characters for Title:', 0, 70, 60)
                        desc_caract = st.slider('Maximum characters for Description:', 0, 170, 155)
                    with st.expander('🤖 - Bot GPT:', expanded=True):
                        st.write(f"🤖 - Eu sou um redator especializado em SEO, **{persona}**, e adoro escrever de maneira natural e envolvente em língua portuguesa brasileira. Minha abordagem é criar meta titles e descriptions que realmente cativam os leitores e ajudam a destacar os produtos nos motores de busca.")               
                    button_proceed = st.button('Ir para os Detalhes da Página: ➡️')
                    
                if button_proceed:
                    st.session_state.button_proceed = True
                    index = 1
                                         
        
        with st.container():
            button = False
            with c2:
                if not st.session_state.button_proceed and st.session_state.language == 'English':
                    st.write('⬅️ You should be writing your inputs')
                elif not st.session_state.button_proceed and st.session_state.language == 'Portuguese (Brazil)':
                    st.write('⬅️ Você deveria estar escrevendo on seus inputs')
                
                if st.session_state.button_proceed and persona and st.session_state.language == 'English':    
                    text = st.text_area('Insert any details about your page:', help="Insert any description you have, including price, tags, or any other information that could assist AI in generating content",height=200)
                    button = st.button('Craft Meta Tags ✨')   
                elif st.session_state.button_proceed and persona and st.session_state.language == 'Portuguese (Brazil)':    
                    text = st.text_area('Insira todos os detalhes sobre sua página:', help="Insira qualquer descrição que você tenha, incluindo preço, tags ou qualquer outra informação que possa ajudar a IA a gerar conteúdo",height=200)
                    button = st.button('Criar Meta Tags ✨') 
        
        with st.container():
            with c3:
                if button:
                    openai.api_key = st.session_state.api
                    
                    texto_preprocessado = preprocess_text(text)
                    
                    if st.session_state.language == 'English':
                        # Crie um prompt para a API do chatGPT
                        prompt = f"SEO: Title (maximum {title_caract} chars), Meta Description (maximum {desc_caract} chars) for prominence.\n"
                        prompt += f"{texto_preprocessado}\n"

                        response = openai.ChatCompletion.create(
                            model="gpt-4",  # Use a engine GPT-4.0
                            messages=[
                                {"role": "system", "content": f'🤖 - I am an SEO specialist writer, **{persona}**, and I love to write in a natural and engaging manner in {st.session_state.language}. My approach is to create meta titles and descriptions that truly captivate readers and help products stand out on search engines.'},
                                {"role": "user", "content": prompt},
                            ]
                        )

                    elif st.session_state.language == 'Portuguese (Brazil)':
                        # Crie um prompt para a API do chatGPT
                        prompt = f"SEO: Título (máximo {title_caract} carac), Meta Description (máximo {desc_caract} carac) p/ destaque no buscador\n"
                        prompt += f"{texto_preprocessado}\n"

                        response = openai.ChatCompletion.create(
                            model="gpt-4",  # Use a engine GPT-4.0
                            messages=[
                                {"role": "system", "content": f"🤖 - Eu sou um redator especializado em SEO, **{persona}**, e adoro escrever de maneira natural e envolvente em língua portuguesa brasileira. Minha abordagem é criar meta titles e descriptions que realmente cativam os leitores e ajudam a destacar os produtos nos motores de busca."},
                                {"role": "user", "content": prompt},
                            ]
                        )
                        
                    # Obtenha a resposta gerada pelo chatGPT
                    generated_text = response['choices'][0]['message']['content']
                    
                    st.session_state.meta = generated_text
                   
                if hasattr(st.session_state, 'meta') and st.session_state.meta is not None:
                    index = 2
                    if st.session_state.language == 'English':         
                        st.write('Here is your result:')
                        st.write(st.session_state.meta)
                    elif st.session_state.language == 'Portuguese (Brazil)':
                        st.write('Aqui está o resultado:')
                        st.write(st.session_state.meta)                  
                  
        with container_single:
            if st.session_state.language == 'English':
                steps_bar = sac.steps(
                items=[
                    sac.StepsItem(title='API Config'),
                    dict(title='Page Details'),
                    dict(title='Result'),
                ], index=index, format_func='title', placement='horizontal', size='default', direction='horizontal', type='default', dot=False, return_index=True)
            elif st.session_state.language == 'Portuguese (Brazil)':
                steps_bar = sac.steps(
                items=[
                    sac.StepsItem(title='Configuração da API'),
                    dict(title='Detalhes da Página'),
                    dict(title='Resultado'),
                ], index=index, format_func='title', placement='horizontal', size='default', direction='horizontal', type='default', dot=False, return_index=True)

        if index == 1:       
            style = st.markdown(
            """
            <style>
            .css-1r6slb0.e1f1d6gn1:nth-of-type(1) {
                opacity: 0.5;
            }
            </style>
            """,
            unsafe_allow_html=True
        )   
                     
        if index == 2:
            style = st.markdown(
            """
            <style>
            .css-1r6slb0.e1f1d6gn1:nth-of-type(1),
            .css-1r6slb0.e1f1d6gn1:nth-of-type(2) {
                opacity: 0.5;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
    with tab2:
        
        c1, c2, c3 = st.columns(3)
        
        container_bulk_config = st.container()
        container_bulk_upload = st.container()
        container_bulk_result = st.container()
        
        with container_bulk_config:
            with c1:
                c1col1, c1col2 = st.columns(2)
                               
                with c1col1:      
                    st.session_state.language = st.selectbox('Choose your Language:', ('English', 'Portuguese (Brazil)'), key="bulk_language")
                with c1col2:
                    st.session_state.api = st.text_input('OpenAI API Key:', value=st.session_state.api, key="bulk_api")
            
                if st.session_state.language == 'English':
                    persona = st.text_input('Your Persona Here', 'Passionate about technology', help='This persona is going to be inserted into the prompt. You can check the full AI persona below', key="bulk_persona")
                    with st.expander("📏 - Change Meta's size"):
                        title_caract = st.slider('Maximum characters for Title:', 0, 70, 60, key="bulk_title")
                        desc_caract = st.slider('Maximum characters for Description:', 0, 170, 155, key="bulk_desc")
                    with st.expander('🤖 - GPT Bot:', expanded=True):
                        st.markdown(f'🤖 - I am an SEO specialist writer, **{persona}**, and I love to write in a natural and engaging manner in English. My approach is to create meta titles and descriptions that truly captivate readers and help products stand out on search engines.')
                    button_proceed = st.button('Proceed to File Upload ➡️', key="bulk_proceed")
                elif st.session_state.language == 'Portuguese (Brazil)':
                    persona = st.text_input('Sua Persona aqui', 'Apaixonado por tecnologia', key="bulk_persona")
                    with st.expander("📏 - Tamanho das Meta Tags"):
                        title_caract = st.slider('Maximum characters for Title:', 0, 70, 60, key="bulk_title")
                        desc_caract = st.slider('Maximum characters for Description:', 0, 170, 155, key="bulk_desc")
                    with st.expander('🤖 - Bot GPT:', expanded=True):
                        st.write(f"🤖 - Eu sou um redator especializado em SEO, **{persona}**, e adoro escrever de maneira natural e envolvente em língua portuguesa brasileira. Minha abordagem é criar meta titles e descriptions que realmente cativam os leitores e ajudam a destacar os produtos nos motores de busca.")               
                    button_proceed = st.button('Ir para o Upload do Arquivo ➡️', key="bulk_proceed")
                   
            if button_proceed and st.session_state.api:
                st.session_state.button_proceed = True
                
            if st.session_state.button_proceed == True:       
                style = st.markdown(
                """
                <style>
                .css-1r6slb0.e1f1d6gn1:nth-of-type(1) {
                    opacity: 0.5;
                }
                </style>
                """,
                unsafe_allow_html=True
            )   

        with container_bulk_upload:
            with c2:
                if st.session_state.button_proceed and st.session_state.language == 'English':
                    file = st.file_uploader('Upload your .xlsx file')
                    
                    if file:
                        df = pd.read_excel(file)
                    
                    options = st.multiselect(
                    'Choose the Columns your .xlsx have',
                    ['URL', 'Name', 'Description'],
                    ['URL', 'Name', 'Description'])
                    button = st.button('Craft Meta Tags ✨', key='bulk_button')
                    
                if st.session_state.button_proceed and st.session_state.language == 'Portuguese (Brazil)':
                    file = st.file_uploader('Upload do seu arquivo .xlsx')
                    
                    if file:
                        df = pd.read_excel(file)
                    
                    options = st.multiselect(
                    'Escolha as colunas que o seu arquivo .xlsx possui',
                    ['URL', 'Nome', 'Descrição'],
                    ['URL', 'Nome', 'Descrição'])
                    button = st.button('Criar Meta Tags ✨', key='bulk_button')           
                       
        with container_bulk_result:
            with c3:
                if button:
                    openai.api_key = st.session_state.api
                    
                    df_temp_list = []
                    
                    # Itera sobre as linhas do DataFrame e atualiza a coluna "description" com o conteúdo revisado
                    for index, row in df.iterrows():
                        if st.session_state.language == 'English':
                            # Pré-processa o texto
                            texto_preprocessado = preprocess_text(row['Description'])
                            name_preprocessado = preprocess_text(row['Name'])
                            
                            # Atualiza a coluna "description" com o conteúdo revisado
                            df.at[index, 'Description'] = texto_preprocessado
                            # Atualiza a coluna "description" com o conteúdo revisado
                            df.at[index, 'Name'] = name_preprocessado
                        elif st.session_state.language == 'Portuguese (Brazil)':
                            # Pré-processa o texto
                            texto_preprocessado = preprocess_text(row['Descrição'])
                            name_preprocessado = preprocess_text(row['Nome'])
                            
                            # Atualiza a coluna "description" com o conteúdo revisado
                            df.at[index, 'Descrição'] = texto_preprocessado
                            # Atualiza a coluna "description" com o conteúdo revisado
                            df.at[index, 'Nome'] = name_preprocessado       
    
                    for index, row in df.iterrows():
                        if st.session_state.language == 'English':
                        # Obtenha os valores das colunas                        
                            if 'URL' in options:
                                url=row['URL']
                            if 'Name' in options:
                                name = row['Name']
                            if 'Description' in options:
                                description = row['Description']

                            # Crie um prompt para a API do chatGPT
                            prompt = "SEO: Title (maximum {title_caract} characters), Meta Description (maximum {desc_caract} characters) for prominence.\n"
                            if 'name' in options:
                                prompt += f"{name}\n"
                            if 'Description' in options:
                                prompt += f"{description}\n"

                            response = openai.ChatCompletion.create(
                                model="gpt-4",  # Use a engine GPT-4.0
                                messages=[
                                    {"role": "system", "content": f'I am an SEO specialist writer, **{persona}**, and I love to write in a natural and engaging manner in English. My approach is to create meta titles and descriptions that truly captivate readers and help products stand out on search engines.'},
                                    {"role": "user", "content": prompt},
                                ]
                            )
                            
                            # Obtenha a resposta gerada pelo chatGPT
                            generated_text = response['choices'][0]['message']['content']

                            # Crie um DataFrame temporário para cada linha
                            df_temp = pd.DataFrame({'URL': [url], 'Name': [name], 'Answer GPT-4': [generated_text]})
                            df_temp_list.append(df_temp)
                            
                        if st.session_state.language == 'Portuguese (Brazil)':
                        # Obtenha os valores das colunas                        
                            if 'URL' in options:
                                url=row['URL']
                            if 'Nome' in options:
                                nome = row['Nome']
                            if 'Descrição' in options:
                                descricao = row['Descrição']

                            # Crie um prompt para a API do chatGPT
                            prompt = "SEO: Título (máximo {title_caract} carac), Meta Description (máximo {desc_caract} carac) p/ destaque no buscador\n"
                            if 'nome' in options:
                                prompt += f"{nome}\n"
                            if 'Descrição' in options:
                                prompt += f"{descricao}\n"

                            response = openai.ChatCompletion.create(
                                model="gpt-4",  # Use a engine GPT-4.0
                                messages=[
                                    {"role": "system", "content": f"🤖 - Eu sou um redator especializado em SEO, **{persona}**, e adoro escrever de maneira natural e envolvente em língua portuguesa brasileira. Minha abordagem é criar meta titles e descriptions que realmente cativam os leitores e ajudam a destacar os produtos nos motores de busca."},
                                    {"role": "user", "content": prompt},
                                ]
                            )

                            # Obtenha a resposta gerada pelo chatGPT
                            generated_text = response['choices'][0]['message']['content']

                            # Crie um DataFrame temporário para cada linha
                            df_temp = pd.DataFrame({'URL': [url], 'Nome': [nome], 'Resposta GPT-4': [generated_text]})
                            df_temp_list.append(df_temp)

                    # Concatene os DataFrames temporários para criar o DataFrame final
                    df_final = pd.concat(df_temp_list, ignore_index=True)

                    # Armazene o DataFrame final na st.session_state
                    st.session_state.df_resultado = df_final
                                               
                if hasattr(st.session_state, 'df_resultado') and st.session_state.df_resultado is not None:
                    style = st.markdown(
                    """
                    <style>
                    .css-1r6slb0.e1f1d6gn1:nth-of-type(1),
                    .css-1r6slb0.e1f1d6gn1:nth-of-type(2) {
                        opacity: 0.5;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )        
                    
                    if st.session_state.language == 'English':
                        st.write('Here is your result:')
                    elif st.session_state.language == 'Portuguese (Brazil)':
                        st.write('Aqui está o seu resultado:')
                        
                    st.dataframe(st.session_state.df_resultado)
                    
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        # Write each dataframe to a different worksheet.
                        st.session_state.df_resultado.to_excel(writer, sheet_name='file.name')
                        writer.close()
                        
                        st.download_button(
                        label="📥 Download Excel",
                        data=buffer,
                        file_name="bulk-"+file.name,
                        mime="application/vnd.ms-excel"
                    )  
                
    return True