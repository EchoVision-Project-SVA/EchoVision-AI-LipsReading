import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from model.lipreading_model import LipreadingModel
from utils.video_processing import load_video
from utils.text_to_speech import convert_text_to_speech
from config import VIDEO_DIR

router = APIRouter()
lipreading_model = LipreadingModel()

request_count = 0

def cleanup_files():
    """Delete video and audio files older than one week.
    Files must be named as <basename>_YYYYMMDD.ext.
    """
    now = datetime.now()
    one_week = timedelta(days=7)
    directories = [VIDEO_DIR, "output_audio"]

    for directory in directories:
        if os.path.exists(directory):
            for file_name in os.listdir(directory):
                parts = file_name.rsplit('_', 1)
                if len(parts) != 2:
                    continue
                date_part = parts[1].split('.')[0]
                try:
                    file_date = datetime.strptime(date_part, "%Y%m%d")
                except Exception:
                    continue
                if now - file_date > one_week:
                    try:
                        os.remove(os.path.join(directory, file_name))
                        print(f"Deleted {os.path.join(directory, file_name)}")
                    except Exception as e:
                        print(f"Failed to delete {file_name}: {e}")

@router.post("/predict")
async def predict_video(request: Request, file: UploadFile = File(...)):
    global request_count
    request_count += 1

    date_str = datetime.now().strftime("%Y%m%d")
    base, ext = os.path.splitext(file.filename)
    video_filename = f"{base}_{date_str}{ext}"
    os.makedirs(VIDEO_DIR, exist_ok=True)
    video_path = os.path.join(VIDEO_DIR, video_filename)

    try:
        with open(video_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    try:
        frames = load_video(video_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

    try:
        prediction_text = lipreading_model.predict(frames)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    audio_dir = "output_audio"
    os.makedirs(audio_dir, exist_ok=True)
    audio_filename = f"{base}_{date_str}.mp3"
    audio_output_path = os.path.join(audio_dir, audio_filename)
    try:
        convert_text_to_speech(prediction_text, audio_output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech error: {str(e)}")

    audio_url = f"{request.base_url}static/{audio_filename}"

    if request_count % 100 == 0:
        cleanup_files()

    return {"prediction_text": prediction_text, "audio_file": audio_url}