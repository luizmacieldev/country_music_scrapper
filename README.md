# 🎧 Last.fm Country Artists Scraper

Este projeto foi desenvolvido utilizando o framework **Scrapy**, com o objetivo de coletar informações detalhadas sobre artistas de música country diretamente do site Last.fm.<br/> Ele faz a coleta de dados de perfis de artistas, estrutura e armazena as informações em um banco de dados **MongoDB** e utiliza **Streamlit** para a visualização dos dados, facilitando a exploração e análise das informações extraídas.


![image](https://github.com/user-attachments/assets/58911373-b0a3-4a4d-a0ad-ea15bc10a0c3)





## 📋 Funcionalidades
As principais informações extraídas sobre cada artista incluem:

- **Nome do Artista**: Nome completo do artista ou banda.
- **Ouvintes**: Quantidade de ouvintes no Last.fm.
- **Foto do Artista**: URL da imagem de perfil.
- **Mini Biografia**: Breve descrição sobre o artista.
- **URL do Artista**: Link para o perfil completo no Last.fm.
- **Principais Gêneros**: Tags mais frequentes associadas ao artista.
- **Músicas Mais Ouvidas**: As 10 faixas mais reproduzidas, com nome e link para cada uma.
- **Álbuns Mais Populares**: Lista de álbuns mais ouvidos, com detalhes como foto do album, número de faixas, ano de lançamento e quantidade de ouvintes.
- **Fotos do Artista**: Links com as principais fotos do artista.
- **Redes Sociais**: URLs das principais redes sociais do artista.
- **Biografia**: Texto completo da biografia completa do artista.

## 📦 Armazenamento no MongoDB
Os dados coletados são organizados e armazenados no MongoDB, permitindo fácil acesso e consulta. Cada documento no banco de dados inclui todas as informações mencionadas acima para cada artista de country disponível no Last.fm.

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- **Python 3.8+**
- **Scrapy**
- **MongoDB**
- **Streamlit**

### Instruções

1. Clone este repositório:
   **git clone https://github.com/luizmacieldev/country_music_scrapper**

2. Instalar as dependências:
  **pip install -r requirements.txt**

3. Utilizar o comando abaixo para iniciar o processo, esse processo irá iniciar a coleta e estruturação dos dados e salvar em um database chamado "country_db" e na collection "artists"<br>
  **scrapy crawl artists**

4. Utilize os comandos abaixo para gerar esses dados em formato json ou csv.<br/>
  **scrapy crawl artists -O artists.json**<br/>
  **scrapy crawl artists -O artists.csv**

5. Para visualização com o **StreamLit** : <br/>
Entrar na pasta country/streamlit
Utilizar o comando **streamlit run app.py**
