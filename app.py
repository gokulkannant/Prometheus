import streamlit as st
import yt_dlp
import os
import re

def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d['_percent_str']
        percent_clean = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).strip('%')  # Remove ANSI codes
        try:
            progress = float(percent_clean) / 100
            st.session_state.progress_bar.progress(progress)
        except ValueError:
            pass  # Ignore if conversion fails

def download_video(url, format_option, quality):
    options = {
        'format': quality if format_option == 'Video' else 'bestaudio',
        'progress_hooks': [progress_hook],
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = f"{info['title']}.{'mp4' if format_option == 'Video' else 'mp3'}"
        os.rename(ydl.prepare_filename(info), file_name)
        return file_name

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
                    file_name=file_path,
                    mime="video/mp4" if format_option == "Video" else "audio/mpeg"
                )
            
            st.success("Download completed!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL!")
