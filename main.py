import http.client
import typing
import urllib.request
import cv2
import numpy as np

'''import IPython.display'''
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Image,
    Part,
)


multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

video_capture = cv2.VideoCapture(0)

frame_count = 0
frame_interval = 2
next_frame_time = 0

while True:
    ret, frame = video_capture.read()
    current_time = cv2.getTickCount() / cv2.getTickFrequency()
    
    if current_time>=next_frame_time:
        next_frame_time = current_time + frame_interval
        pil_image = PIL_Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    image = Image.load_from_pil_image(pil_image)
    prompt = "Describe the closest object in this image"
    contents = [image, prompt]

    generation_config = GenerationConfig(
        temperature=0.2,          # higher = more creative (default 0.0)
        top_p=0.3,                # higher = more random responses, response drawn from more possible next tokens (default 0.95)
        top_k=20,                 # higher = more random responses, sample from more possible next tokens (default 40)
        candidate_count=1,
        max_output_tokens=1024,   # default = 2048
    )

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    responses = multimodal_model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True
    )

    print(responses[0].text)

video_capture.release()
cv2.destroyAllWindows()




