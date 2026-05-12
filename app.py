import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="AI YouTube Video Summarizer")

st.title("AI YouTube Video Summarizer")
st.write("Paste a YouTube URL and get transcript summary with timestamps!")

# Extract video ID
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None

# Get transcript + timestamps
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        full_text = " ".join([item["text"] for item in transcript])

        timestamps = []

        for item in transcript[:10]:
            minute = int(item["start"] // 60)
            second = int(item["start"] % 60)

            timestamps.append(
                f"{minute}:{second:02d} - {item['text']}"
            )

        return full_text, "\n".join(timestamps)

    except Exception:
        return (
            "Transcript unavailable for this video.",
            "No timestamps available."
        )

# UI
url = st.text_input("Paste YouTube URL")

if st.button("Generate Summary"):

    video_id = extract_video_id(url)

    if video_id:

        full_text, timestamps = get_transcript(video_id)

        st.subheader("Summary")
        st.write(full_text[:1500])

        st.subheader("Important Timestamps")
        st.text(timestamps)

    else:
        st.error("Invalid YouTube URL")