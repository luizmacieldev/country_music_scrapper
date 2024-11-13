# 🎧 Last.fm Country Artists Scraper

This project was developed using the **Scrapy** framework to collect detailed information about country music artists directly from the Last.fm website.<br/> It gathers artist profile data, structures and stores the information in a **MongoDB** database, and uses **Streamlit** for data visualization, making it easier to explore and analyze the extracted information.


![image](https://github.com/user-attachments/assets/58911373-b0a3-4a4d-a0ad-ea15bc10a0c3)

![Capturar](https://github.com/user-attachments/assets/fe1b6926-6100-41d7-90e5-244330a3cc5e)




## 📋 Features
The main information extracted for each artist includes:

- **Artist Name**: Full name of the artist or band.
- **Listeners**: Number of listeners on Last.fm.
- **Artist Photo**: URL of the profile picture.
- **Mini Biography**: Short description about the artist.
- **Artist URL**: Link to the full profile on Last.fm.
- **Top Genres**: Most frequent tags associated with the artist.
- **Top Tracks**: The 10 most played tracks, with name and link for each.
- **Popular Albums**: List of top albums, including details like album cover, track count, release year, and listener count.
- **Artist Photos**: Links to the main photos of the artist.
- **Social Media**: URLs to the artist’s main social media profiles.
- **Full Biography**: Full text of the artist’s biography.

## 📦 MongoDB Storage
The collected data is organized and stored in MongoDB, enabling easy access and querying. Each document in the database includes all the information mentioned above for each country artist available on Last.fm.

## 🚀 How to Run the Project

### Prerequisites
- **Python 3.8+**
- **Scrapy**
- **MongoDB**
- **Streamlit**

### Instructions

1. Clone this repository:
   **git clone https://github.com/luizmacieldev/country_music_scrapper**

2. Install the dependencies:
  **pip install -r requirements.txt**

3. Use the command below to start the process. This will begin data collection and structuring, saving it in a database named "country_db" in the "artists" collection:<br>
  **scrapy crawl artists**

4. To generate data in JSON or CSV format, use the following commands:<br/>
  **scrapy crawl artists -O artists.json**<br/>
  **scrapy crawl artists -O artists.csv**

5. To view data with **StreamLit** : <br/>
Navigate to the country/streamlit folder and run:
 **streamlit run app.py**
