import cv2
import tensorflow as tf

def load_video(path: str) -> tf.Tensor:
    cap = cv2.VideoCapture(path)
    frames = []
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frame = tf.image.rgb_to_grayscale(frame)
        frame = frame[190:236, 80:220, :]
        frames.append(frame)
    cap.release()
    if not frames:
        raise ValueError("No frames extracted from video.")
    frames_tensor = tf.stack(frames)
    mean = tf.reduce_mean(frames_tensor)
    std = tf.math.reduce_std(tf.cast(frames_tensor, tf.float32))
    normalized = tf.cast((frames_tensor - mean), tf.float32) / std
    return normalized
