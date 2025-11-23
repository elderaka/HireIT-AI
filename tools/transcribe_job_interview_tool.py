import os
import re
import json
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

STT_URL = os.getenv("https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/c6178b34-fc62-4527-91cf-4f498faff0e4","https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/c6178b34-fc62-4527-91cf-4f498faff0e4/v1/recognize")
STT_API_KEY = os.getenv("***REMOVED***", "***REMOVED***")
STT_DEFAULT_LANGUAGE = "en-US"  # atau "id-ID"


def _download_audio_from_source(audio) -> bytes:
    """Normalisasi berbagai bentuk input audio menjadi audio_bytes."""
    # Kasus 1: dict (downloadable_file dari Orchestrate)
    if isinstance(audio, dict):
        if "path" not in audio:
            raise ValueError("Invalid audio object: dict without 'path' field.")
        resp = requests.get(audio["path"], stream=True, timeout=120)
        resp.raise_for_status()
        return resp.content

    # Kasus 2: bytes / bytearray
    if isinstance(audio, (bytes, bytearray)):
        return bytes(audio)

    # Kasus 3: string (bisa URL atau JSON downloadable_file)
    if isinstance(audio, str):
        audio_str = audio.strip()

        # 3a. Kalau string-nya JSON downloadable_file
        if audio_str.startswith("{") and audio_str.endswith("}"):
            try:
                obj = json.loads(audio_str)
            except json.JSONDecodeError:
                raise ValueError("Audio string looks like JSON but failed to parse.")

            if not isinstance(obj, dict) or "path" not in obj:
                raise ValueError("JSON string for audio does not contain 'path'.")
            resp = requests.get(obj["path"], stream=True, timeout=120)
            resp.raise_for_status()
            return resp.content

        # 3b. Kalau string-nya URL langsung
        if audio_str.startswith("http://") or audio_str.startswith("https://"):
            resp = requests.get(audio_str, stream=True, timeout=120)
            resp.raise_for_status()
            return resp.content

        raise ValueError(
            f"Unsupported audio string format. Expected URL or JSON downloadable_file, got: {audio_str[:50]}..."
        )

    # Tipe lain benar-benar tidak didukung
    raise ValueError(f"Unsupported audio type: {type(audio)}. Expected dict, bytes, or str.")


def _extract_raw_transcript(stt_result: dict) -> str:
    """Ambil teks mentah dari hasil STT (gabung alternatif pertama tiap result)."""
    segments = []
    for res in stt_result.get("results", []):
        alts = res.get("alternatives", [])
        if not alts:
            continue
        segments.append(alts[0].get("transcript", "").strip())

    raw_text = " ".join(seg for seg in segments if seg).strip()
    return raw_text


def _clean_transcript(text: str) -> str:
    """Bersihkan transkrip tanpa mengubah makna (light normalization)."""
    if not text:
        return text

    # 1) Normalkan spasi berlebih
    t = " ".join(text.split())

    # 2) Rapikan spasi sebelum tanda baca (.,!?)
    t = re.sub(r"\s+([,.!?])", r"\1", t)

    # 3) Tambahkan spasi setelah tanda baca kalau belum ada
    t = re.sub(r"([,.!?])([^\s])", r"\1 \2", t)

    # 4) Perbaiki " i " -> " I " (bahasa Inggris)
    t = re.sub(r"\bi\b", "I", t)

    # 5) Kapitalisasi awal kalimat sederhana
    #    Pisah berdasarkan . ! ? lalu gabungkan lagi
    parts = re.split(r"([.!?])", t)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        s = parts[i].strip()
        punct = parts[i + 1]
        if not s:
            continue
        s = s[0].upper() + s[1:] if len(s) > 1 else s.upper()
        sentences.append(s + punct)

    # Kalau ada sisa tanpa tanda baca di akhir
    if len(parts) % 2 == 1:
        last = parts[-1].strip()
        if last:
            last = last[0].upper() + last[1:] if len(last) > 1 else last.upper()
            sentences.append(last)

    cleaned = " ".join(sentences)
    return cleaned.strip()


@tool(permission=ToolPermission.READ_ONLY)
def transcribe_job_interview(audio, language: str = STT_DEFAULT_LANGUAGE) -> dict:
    """
    Transcribe a job interview audio file.

    Args:
        audio: Bisa berupa:
            - dict downloadable_file dengan field 'path'
            - string URL (http/https)
            - string JSON berisi downloadable_file
            - raw audio bytes
        language (str): kode bahasa STT, contoh "en-US" atau "id-ID".

    Returns:
        dict: {
            "raw_transcript": "<transkrip mentah dari STT>",
            "clean_transcript": "<transkrip yang sudah dirapikan>"
        }
    """
    # 1) Normalisasi audio -> bytes
    audio_bytes = _download_audio_from_source(audio)
    if not audio_bytes:
        raise ValueError("Audio data is empty after download/normalization.")

    # 2) Panggil Watson STT
    headers = {
        "Content-Type": "audio/mpeg",  # sesuaikan kalau format audio lain
    }
    params = {
        "model": f"{language}_BroadbandModel"
    }

    try:
        stt_resp = requests.post(
            STT_URL,
            headers=headers,
            params=params,
            data=audio_bytes,
            auth=("apikey", STT_API_KEY),
            timeout=120,
        )
        stt_resp.raise_for_status()
    except Exception as e:
        raise ValueError(f"Failed to call STT API: {e}") from e

    stt_result = stt_resp.json()

    # 3) Ambil transkrip mentah
    raw_text = _extract_raw_transcript(stt_result)
    if not raw_text:
        raise ValueError("STT API returned no transcripts.")

    # 4) Bersihkan transkrip
    clean_text = _clean_transcript(raw_text)

    return {
        "raw_transcript": raw_text,
        "clean_transcript": clean_text,
    }