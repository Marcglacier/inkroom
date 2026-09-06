# app/inbox/services/media/video/video_metadata.py
import json
import os
import subprocess
import tempfile


def extract_video_metadata(file):
    """
    Extract video metadata using FFprobe.

    Returns:
        {
            "duration": int | None,
            "width": int | None,
            "height": int | None,
        }
    """

    suffix = os.path.splitext(file.filename)[1]

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp:

            file.stream.seek(0)
            temp.write(file.stream.read())

            temp_path = temp.name

        command = [
            "ffprobe",
            "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            temp_path,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        video_stream = next(
            (
                stream
                for stream in data.get("streams", [])
                if stream.get("codec_type") == "video"
            ),
            None,
        )

        duration = data.get("format", {}).get("duration")

        return {
            "duration": (
                round(float(duration))
                if duration
                else None
            ),
            "width": (
                video_stream.get("width")
                if video_stream
                else None
            ),
            "height": (
                video_stream.get("height")
                if video_stream
                else None
            ),
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        file.stream.seek(0)