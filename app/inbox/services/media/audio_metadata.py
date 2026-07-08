from mutagen import File
from io import BytesIO


DEBUG_AUDIO = False


def log(*args):
    if DEBUG_AUDIO:
        print(*args)


def extract_audio_metadata(file):
    try:
        log("\n🎧 [AUDIO METADATA] START EXTRACTION")
        log("📁 Filename:", file.filename)
        log("📦 Content-Type:", file.content_type)

        file.stream.seek(0)
        data = file.stream.read()

        if not data:
            return {}

        audio = File(BytesIO(data))

        if audio is None:
            return {}

        metadata = {
            "title": None,
            "artist": None,
            "album": None,
            "duration": None,
            "cover": None,
        }

        if audio.info:
            metadata["duration"] = int(audio.info.length)

        tags = audio.tags

        if tags:
            title = tags.get("TIT2")
            artist = tags.get("TPE1")
            album = tags.get("TALB")

            metadata["title"] = str(title) if title else None
            metadata["artist"] = str(artist) if artist else None
            metadata["album"] = str(album) if album else None

            # Extract embedded album art
            for key, tag in tags.items():
                log("TAG:", key)

                if key.startswith("APIC"):
                    metadata["cover"] = tag.data
                    log("🖼 Album cover found:", len(tag.data), "bytes")
                    break

        file.stream.seek(0)
        return metadata

    except Exception as e:
        log("❌ AUDIO METADATA ERROR:", e)
        file.stream.seek(0)
        return {}