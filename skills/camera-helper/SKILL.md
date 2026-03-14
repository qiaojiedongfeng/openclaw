---
name: camera-helper
description: Capture a photo from the local webcam and send it to Discord. Use when user asks for webcam photo, camera capture, or similar.
---

# Camera Helper

## When to Use

Triggered when user asks for webcam photo or camera capture. Supports keywords:
- 拍照、拍一张、摄像头
- camera、webcam、take a photo

## How It Works

1. Uses OpenCV to capture one frame from the default webcam
2. Saves the image to temp folder with timestamp
3. Sends the image to Discord using `message` tool

## Steps

```python
import cv2
import os
import time
from datetime import datetime

# Capture from default webcam with optimized settings
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
time.sleep(2)  # Warm up camera for 2 seconds

ret, frame = cap.read()
cap.release()

if ret:
    path = os.path.join(
        os.environ['TEMP'],
        'camera_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
    )
    cv2.imwrite(path, frame)
    print(path)  # Output for message tool
```

After capture, send to Discord:
- `action: send`
- `target: <current_channel_id>`
- `filePath: $path`

## Notes

- Requires: `pip install opencv-python`
- Assumes default webcam (index 0)
- If no webcam found, capture will fail silently
