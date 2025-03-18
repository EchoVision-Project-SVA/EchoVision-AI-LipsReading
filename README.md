# LipsReading

## Overview

This project implements a lipreading model that takes a video file name, predicts the spoken words, converts the text to speech, and returns both the text prediction and an audio file.

## Folder Structure

LipReading/
├── app/
│ ├── **init**.py
│ ├── api.py
│ └── main.py
├── model/
│ ├── **init**.py
│ └── lipreading_model.py
├── utils/
│ ├── **init**.py
│ ├── video_processing.py
│ └── text_to_speech.py
├── config.py
├── requirements.txt
└── README.md

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the API Server

uvicorn app.main:app --reload
