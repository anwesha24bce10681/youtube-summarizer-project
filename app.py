import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="YouTube Video Summarizer", layout="wide")

st.title("AI YouTube Video Summarizer")
st.write("Paste a YouTube URL and get transcript summary with timestamps!")

url = st.text_input("Paste YouTube URL")


def extract_video_id(url):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i["text"] for i in transcript])
        return text
    except Exception:
        return "Transcript unavailable for this video."





def generate_timestamps(transcript):
    timestamps = []

    for item in transcript[:8]:
        minute = int(item['start'] // 60)
        second = int(item['start'] % 60)

        timestamps.append(
            f"{minute:02d}:{second:02d} - {item['text']}"
        )

    return "\n".join(timestamps)


if st.button("Generate Summary"):

    if not url:
        st.error("Please paste a YouTube URL.")
        st.stop()

    video_id = extract_video_id(url)

    if not video_id:
        st.error("Invalid YouTube URL.")
        st.stop()

    with st.spinner("Fetching transcript..."):
        transcript = get_transcript(video_id)

    full_text = transcript

    timestamps = generate_timestamps(transcript)

    st.subheader("Summary")

    summary = full_text[:1500]

    st.write(summary)

    st.subheader("Important Timestamps")

    st.text(timestamps)

    st.subheader("Important Timestamps")
    st.text(timestamps)
 