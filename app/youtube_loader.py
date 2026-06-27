import re

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document


def extract_video_id(url: str):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def load_youtube(url: str):
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    text = "\n".join(
        item.text
        for item in transcript
    )

    return [
        Document(
            page_content=text,
            metadata={
                "source": url,
                "video_id": video_id,
                "file_type": "youtube",
                "page": 0
            }
        )
    ]