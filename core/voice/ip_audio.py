"""IP camera audio helper for Jarvis.

Default audio URL: http://192.168.1.5:8080/audio.wav
Works best if ffmpeg is installed. Falls back to saving the HTTP audio stream.
"""

import json
import os
import shutil
import subprocess
import tempfile
import time

try:
    from core.utils.interrupt import is_interrupted
except Exception:
    def is_interrupted():
        return False


def load_media_config():
    cfg = {
        "audio_source": "ip",
        "ip_audio_url": "http://192.168.1.5:8080/audio.wav",
        "audio_duration_seconds": 4,
        "fallback_to_local_microphone": False,
    }
    try:
        if os.path.exists("config/camera_config.json"):
            with open("config/camera_config.json", "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
    except Exception as e:
        print(f"[IPAudio] config read failed: {e}")

    if os.environ.get("JARVIS_AUDIO_SOURCE"):
        cfg["audio_source"] = os.environ["JARVIS_AUDIO_SOURCE"].strip().lower()
    if os.environ.get("JARVIS_IP_AUDIO_URL"):
        cfg["ip_audio_url"] = os.environ["JARVIS_IP_AUDIO_URL"].strip()
    if os.environ.get("JARVIS_AUDIO_DURATION"):
        try:
            cfg["audio_duration_seconds"] = float(os.environ["JARVIS_AUDIO_DURATION"])
        except ValueError:
            pass
    return cfg


def should_use_ip_audio():
    cfg = load_media_config()
    return str(cfg.get("audio_source", "local")).lower() in ("ip", "ip_camera", "http") and bool(cfg.get("ip_audio_url"))


def _record_with_ffmpeg(url, duration, out_wav):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False, "ffmpeg not found"

    cmd = [
        ffmpeg,
        "-y",
        "-loglevel", "error",
        "-t", str(duration),
        "-i", url,
        "-ar", "16000",
        "-ac", "1",
        out_wav,
    ]
    proc = None
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deadline = time.time() + float(duration) + 8
        while proc.poll() is None:
            if is_interrupted():
                proc.terminate()
                try:
                    proc.wait(timeout=1)
                except Exception:
                    proc.kill()
                return False, "cancelled"
            if time.time() > deadline:
                proc.kill()
                return False, "ffmpeg timeout"
            time.sleep(0.1)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0 and os.path.exists(out_wav) and os.path.getsize(out_wav) > 1000:
            return True, "ok"
        err = stderr.decode("utf-8", errors="ignore") if stderr else ""
        return False, err.strip() or "ffmpeg failed"
    except Exception as e:
        try:
            if proc and proc.poll() is None:
                proc.kill()
        except Exception:
            pass
        return False, str(e)


def _record_with_requests(url, duration, out_wav):
    try:
        import requests
        start = time.time()
        bytes_written = 0
        with requests.get(url, stream=True, timeout=(3, float(duration) + 5)) as resp:
            resp.raise_for_status()
            with open(out_wav, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if is_interrupted():
                        return False, "cancelled"
                    if chunk:
                        f.write(chunk)
                        bytes_written += len(chunk)
                    if time.time() - start >= float(duration):
                        break
        if bytes_written > 1000:
            return True, "ok"
        return False, f"too few bytes: {bytes_written}"
    except Exception as e:
        return False, str(e)


def record_ip_audio_to_wav(duration=None):
    cfg = load_media_config()
    url = cfg.get("ip_audio_url") or "http://192.168.1.5:8080/audio.wav"
    duration = float(duration or cfg.get("audio_duration_seconds", 4))

    tmp_dir = tempfile.gettempdir()
    out_wav = os.path.join(tmp_dir, "jarvis_ip_audio.wav")
    try:
        if os.path.exists(out_wav):
            os.remove(out_wav)
    except Exception:
        pass

    print(f"[IPAudio] recording {duration}s from {url}")

    ok, msg = _record_with_ffmpeg(url, duration, out_wav)
    if ok:
        print("[IPAudio] recorded by ffmpeg")
        return out_wav

    print(f"[IPAudio] ffmpeg failed/fallback: {msg}")
    ok, msg = _record_with_requests(url, duration, out_wav)
    if ok:
        print("[IPAudio] recorded by requests")
        return out_wav

    raise RuntimeError(f"Cannot record IP audio from {url}: {msg}")


def recognize_from_ip_audio(language="en-IN", duration=None):
    import speech_recognition as sr

    wav_path = record_ip_audio_to_wav(duration=duration)
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    print("[IPAudio] recognizing...")
    return recognizer.recognize_google(audio, language=language)
