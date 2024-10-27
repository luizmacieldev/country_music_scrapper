import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from config.settings import load_data_from_mongo


mongo_uri = "mongodb://localhost:27017/"
db_name = "country_db"
collection_name = "artists"


data = load_data_from_mongo(mongo_uri, db_name, collection_name)


st.title("Country Artists from Last FM")


st.sidebar.header("Select Artist")
artist_names = ([artist.get('name', '') for artist in data if 'name' in artist])

selected_artist_name = st.sidebar.selectbox("Choose an artist:", artist_names)


selected_artist = next((artist for artist in data if artist['name'] == selected_artist_name), None)
artist_names = sorted([artist.get('name') for artist in data if 'name' in artist])


if selected_artist:
    st.subheader(f"Artist: {selected_artist['name']}")
    

    cols = st.columns(5)
    for i, photo in enumerate(selected_artist.get('photos', [])):
        if i < 5:
            with cols[i]:
                st.image(photo, caption=f'Photo {i + 1} of {selected_artist["name"]}', width=120)

    if selected_artist.get('principal_tags'):
        st.write("### 🏷️ Main Tags")
        st.write(" | ".join([f" {tag}" for tag in selected_artist['principal_tags']]))
    else:
        st.write("No tags found")

    st.write("\n\n")


    st.write(f"#### 🤠 Most played songs by {selected_artist['name']}")
    for idx, song in enumerate(selected_artist['ten_most_played_songs'], start=1):
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            col1.write(f"**{idx}. 🎵**")
            listeners = song.get('listeners', 'N/A')
            formatted_listeners = f"{listeners:,}" if isinstance(listeners, int) else listeners

            col2.markdown(
                f"**[{song['song']}]({song['url']})**  \n"
                f"*Plays:* {formatted_listeners.replace(',', '.')}"
            )


    if 'ten_most_played_songs' in selected_artist:
        song_names = [song['song'] for song in selected_artist['ten_most_played_songs']]
        song_listeners = [int(song['listeners']) for song in selected_artist['ten_most_played_songs']] 

        plt.figure(figsize=(10, 5))
        plt.bar(song_names, song_listeners, color='lightcoral')
        plt.title(f'Most Played Songs by {selected_artist["name"]}')
        plt.xlabel('Songs')
        plt.ylabel('Number of Listeners')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No song data available.")
                
    if 'most_popular_albums' in selected_artist:

        st.write("### 🎶 Most Popular Albums")
        album_cols = st.columns(5)

        for i, album in enumerate(selected_artist['most_popular_albums']):
            if i < 4:
                with album_cols[i]:
                    album_image_url = album.get('photo')
                    album_name = album.get('name', 'Unknown Album')

                    st.image(album_image_url, caption=album_name, width=120)


        album_names = [album['name'] for album in selected_artist['most_popular_albums']]
        album_listeners = [int(album['listeners']) for album in selected_artist['most_popular_albums']]

        plt.figure(figsize=(10, 5))
        plt.bar(album_names, album_listeners, color='skyblue')
        plt.title(f'Listeners of {selected_artist["name"]}\'s Albums')
        plt.xlabel('Album')
        plt.ylabel('Number of Listeners')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No album data available.")


    if selected_artist.get('social_media_links'):
        st.write("### 🌐 Social Media")
        for link in selected_artist['social_media_links']:
            st.write(f"- [{link}]({link})")
    else:
        st.write("No social media avaliable.")

    if selected_artist.get('biography'):
        st.write("**📜 Biography:**")
        st.write(selected_artist['biography'])
    else:
        st.write("No Biography avaliable.")

else:
    st.write("No artists found in the database.")
