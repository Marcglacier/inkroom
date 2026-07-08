from io import BytesIO

from mutagen import File


def extract_audio_cover(file):
    """
    Returns the embedded album cover as bytes,
    or None if the audio has no artwork.
    """

    try:
        file.stream.seek(0)

        audio = File(BytesIO(file.stream.read()))

        file.stream.seek(0)

        if audio is None or not audio.tags:
            return None

        for tag in audio.tags.values():

            # MP3 (ID3 APIC frame)
            if tag.__class__.__name__ == "APIC":
                return {
                    "data": tag.data,
                    "mime_type": tag.mime,
                }

        return None

    except Exception as e:
        print("Album cover extraction failed:", e)

        file.stream.seek(0)

        return None