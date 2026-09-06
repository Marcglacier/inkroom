import os
import tempfile
import subprocess


def extract_video_thumbnail(file):
    """
    Extract a JPEG thumbnail from a video.

    Returns:
        bytes | None
    """

    suffix = os.path.splitext(file.filename)[1]

    input_path = None
    output_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp:

            file.stream.seek(0)
            temp.write(file.stream.read())
            input_path = temp.name

        with tempfile.NamedTemporaryFile(
            delete=False,  suffix=".jpg",) as thumb:
            output_path = thumb.name

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                "00:00:01",
                "-i",
                input_path,
                "-frames:v",
                "1",
                output_path,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if not os.path.exists(output_path):
            return None

        with open(output_path, "rb") as image:
            return image.read()

    finally:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)

        file.stream.seek(0)