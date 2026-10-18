import os
import sys
from typing import Generator, List, Dict, Any, Union
from dotenv import load_dotenv
from openai import OpenAI

# Load configuration values from .env file into environment variables
load_dotenv()

# Read settings from environment with fallbacks for local Ollama OpenAI-compatible endpoint
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("API_KEY", "ollama")
MODEL = os.getenv("MODEL", "qwen2.5:7b")

# Initialize OpenAI client pointed at Ollama's endpoint
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

SYSTEM_PROMPT = (
    "You are S.T.A.R.K. (Stock Testing, Analytics & Ratio Kernel), an advanced quantitative "
    "financial research engine. Your objective is rigorous fundamental stock analysis, "
    "accurate mathematical computations (ratios, valuations, growth rates), and objective data synthesis. "
    "Always be concise, precise, and explicit with formulas and calculations."
)

STARK_BANNER = r"""
  ___ _____ _   ___ _  __
 / __|_   _/_\ | _ \ |/ /
 \__ \ | |/ _ \|   / ' < 
 |___/ |_/_/ \_\_|_\_|\_\
 Stock Testing, Analytics & Ratio Kernel [v1.0]
 Engine: {model} via {base_url} | Mode: Deterministic Math & Intel
 (Type prompt or paste data. Press Enter twice to compute. 'exit' to quit)
"""

def run_stark_kernel(
    prompt: str,
    conversation_history: List[Dict[str, str]] = None,
    stream: bool = True
) -> Union[Generator[str, None, None], str]:
    """
    Core STARK kernel function.
    Processes user financial prompts via OpenAI-compatible endpoint (.env configured).
    Supports streaming generators for both CLI and Streamlit interfaces.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        messages.extend(conversation_history)
    else:
        messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1,  # Low temperature for deterministic calculations
        stream=stream,
    )

    if stream:
        def stream_generator():
            for chunk in response:
                delta_content = chunk.choices[0].delta.content
                if delta_content:
                    yield delta_content
        return stream_generator()
    else:
        return response.choices[0].message.content or ""

# Backward compatibility alias
run_financial_analyst = run_stark_kernel

def get_multiline_input(prompt_text: str) -> str:
    """Helper to capture multiline text in CLI until an empty line is submitted."""
    print(prompt_text)
    lines = []
    while True:
        try:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines).strip()

def cli_stark_kernel():
    """Terminal interactive console for running the STARK kernel."""
    print(STARK_BANNER.format(model=MODEL, base_url=BASE_URL))
    print("=" * 65)

    while True:
        try:
            user_prompt = get_multiline_input("\n[STARK-INPUT] >")

            if not user_prompt:
                continue

            if user_prompt.lower() in ("exit", "quit"):
                print("\n[STARK] Shutting down kernel.")
                break

            print("\n[STARK-KERNEL] Processing financial telemetry...\n" + "-" * 55)

            for chunk in run_stark_kernel(user_prompt, stream=True):
                print(chunk, end="", flush=True)

            print("\n" + "-" * 55)

        except KeyboardInterrupt:
            print("\n[STARK] Operation aborted. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[STARK-ERROR]: {e}")

if __name__ == "__main__":
    cli_stark_kernel()
