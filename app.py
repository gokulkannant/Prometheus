import streamlit as st
import yt_dlp
import os

def download_video(url):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloaded_video.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

st.title("YouTube Video Downloader")

url = st.text_input("Enter Video URL:")

if st.button("Download"):
    if url:
        st.info("Downloading... Please wait!")
        try:
            file_path = download_video(url)
            
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4"
                )
            
            st.success("Download completed!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL!")
