---
name: screenshot-helper
description: Take a screenshot of the local Windows screen and send it to Discord. Use when the user says "截图", "截屏", "screenshot", or similar commands.
---

# Screenshot Helper

## When to Use

Triggered when user asks for a screenshot of their Windows screen. Supports keywords in Chinese or English:
- 截图、截屏、截个图
- screenshot、take a screenshot

## How It Works

1. Takes a full-screen screenshot using PowerShell + System.Drawing
2. Saves the image to the system temp folder with a timestamp filename
3. Sends the image to the current Discord channel using the `message` tool

## Steps

```python
# Create screenshot using Python + Pillow
import os
from datetime import datetime
from PIL import ImageGrab

path = os.path.join(
    os.environ['TEMP'],
    'screenshot_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
)
ImageGrab.grab().save(path)
print(path)  # Output path for next step
```

After saving, send the file to Discord using `message` tool with:
- `action: send`
- `target: <current_channel_id>` (auto-detected from context)
- `filePath: $path`

## Notes

- Requires Python with Pillow installed (`pip install pillow`)
- Works on Windows with GUI
- Screenshot is temporary; consider deleting after sending if disk space is a concern
