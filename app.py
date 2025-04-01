import streamlit as st
import yt_dlp
import os

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d['_percent_str'].strip('%')
        st.session_state.progress_bar.progress(float(p) / 100)

def download_video(url, format_option, quality):
    options = {
        'format': quality if format_option == 'Video' else 'bestaudio',
        'outtmpl': 'downloaded_video.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

st.title("YouTube Video Downloader")

url = st.text_input("Enter Video URL:")
format_option = st.radio("Select Format:", ["Video", "Audio"])
quality_options = {"1080p": "bestvideo+bestaudio/best", "720p": "bv[height=720]+ba/best", "480p": "bv[height=480]+ba/best", "Audio Only": "bestaudio"}
quality = st.selectbox("Select Quality:", list(quality_options.keys()))

if 'progress_bar' not in st.session_state:
    st.session_state.progress_bar = st.empty()

if st.button("Download"):
    if url:
        st.info("Downloading... Please wait!")
        try:
            st.session_state.progress_bar = st.progress(0)
            file_path = download_video(url, format_option, quality_options[quality])
            
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download File",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4" if format_option == "Video" else "audio/mpeg"
                )
            
            st.success("Download completed!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL!")
