from dotenv import load_dotenv, find_dotenv
import os

# Find .env file with os variables
load_dotenv(find_dotenv())

# Конфигурация
VA_ALIAS = ("inmoov",)
VA_TBR = ("скажи", "покажи", "ответь", "произнеси", "расскажи", "сколько", "слушай")
SPEAKER = "aidar"  # aidar, baya, kseniya, xenia, random

# Microphone ID
# -1 defauilt device
MICROPHONE_INDEX = 0

# TTS keys
PICOVOICE_TOKEN = os.getenv("PICOVOICE_TOKEN")
EDEN_API_KEY = os.getenv("EDEN_API_KEY")

# OpenAI Key
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# Auth password
PASSWORD = os.getenv("SERVER_PASSWORD")
