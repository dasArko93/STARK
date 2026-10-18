import os
import sys
import time
import shutil
import subprocess
import urllib.request
import urllib.parse
from typing import Tuple

def is_ollama_online(base_url: str = "http://localhost:11434") -> bool:
    """
    Check if the Ollama server is responding to HTTP requests.
    Strips '/v1' path if present to test root or health endpoint.
    """
    try:
        parsed = urllib.parse.urlparse(base_url)
        root_url = f"{parsed.scheme}://{parsed.netloc}"
        with urllib.request.urlopen(root_url, timeout=1.5) as response:
            return response.status == 200
    except Exception:
        return False

def find_ollama_binary() -> str:
    """
    Attempt to locate the ollama binary on PATH or standard OS installation locations.
    """
    # 1. Check if 'ollama' is directly on system PATH
    bin_path = shutil.which("ollama")
    if bin_path:
        return bin_path

    # 2. Check standard Windows default install location
    if sys.platform == "win32":
        default_win_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
        if os.path.exists(default_win_path):
            return default_win_path

    return None

def ensure_ollama_running(base_url: str = "http://localhost:11434", timeout_seconds: int = 15) -> Tuple[bool, str]:
    """
    Verifies that Ollama is active. If offline and targeting localhost,
    automatically starts 'ollama serve' in the background with terminal status messages.

    Returns:
        (success: bool, message: str)
    """
    parsed = urllib.parse.urlparse(base_url)
    is_local = parsed.hostname in ("localhost", "127.0.0.1", "0.0.0.0")

    # If already running, return immediately
    if is_ollama_online(base_url):
        print(f"[Ollama Check] Connected successfully to Ollama at {parsed.netloc}.")
        return True, "Ollama is running."

    # If remote endpoint (not localhost), we can't start it locally
    if not is_local:
        msg = f"[Ollama Check] Remote Ollama server at {base_url} is unreachable."
        print(msg)
        return False, msg

    # Server is offline on localhost -> attempt automatic launch
    print(f"[Ollama Check] Ollama server is not running on {parsed.netloc}.")
    ollama_path = find_ollama_binary()

    if not ollama_path:
        msg = "[Ollama Check] Could not locate 'ollama.exe'. Please start Ollama manually."
        print(msg)
        return False, msg

    print(f"[Ollama Check] Launching Ollama in the background from: {ollama_path} ...")

    try:
        # Launch detached background process without opening an annoying console window
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        subprocess.Popen(
            [ollama_path, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags
        )
    except Exception as e:
        msg = f"[Ollama Check] Failed to launch Ollama process: {e}"
        print(msg)
        return False, msg

    # Wait for the service to bind and respond
    print("[Ollama Check] Waiting for Ollama server to become ready...", end="", flush=True)
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        time.sleep(1)
        print(".", end="", flush=True)
        if is_ollama_online(base_url):
            print(" Ready!")
            print(f"[Ollama Check] Ollama server started successfully and is responding at {parsed.netloc}.\n")
            return True, "Ollama started successfully."

    print(" Timeout!")
    msg = f"[Ollama Check] Ollama started but did not respond within {timeout_seconds} seconds."
    print(msg)
    return False, msg
