from google.cloud import aiplatform
import os
import database as db
import base64
import cv2
import numpy as np
import tempfile
    
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"

PROJECT_ID = 733362641083  # @param {type:"string"} ENV VARIABLE
LOCATION = "us-central1"  # @param {type:"string"}

# Initialize Vertex AI
import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Image,
    Part,
)

multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

import http.client
import typing
import urllib.request

import IPython.display
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps


def display_images(
    images: typing.Iterable[Image],
    max_width: int = 600,
    max_height: int = 350,
) -> None:
    for image in images:
        pil_image = typing.cast(PIL_Image.Image, image._pil_image)
        if pil_image.mode != "RGB":
            # RGB is supported by all Jupyter environments (e.g. RGBA is not yet)
            pil_image = pil_image.convert("RGB")
        image_width, image_height = pil_image.size
        if max_width < image_width or max_height < image_height:
            # Resize to display a smaller notebook image
            pil_image = PIL_ImageOps.contain(pil_image, (max_width, max_height))
        IPython.display.display(pil_image)


def get_image_bytes_from_url(image_url: str) -> bytes:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        image_bytes = response.read()
    return image_bytes


def load_image_from_url(image_url: str) -> Image:
    image_bytes = get_image_bytes_from_url(image_url)
    return Image.from_bytes(image_bytes)


def get_url_from_gcs(gcs_uri: str) -> str:
    # converts gcs uri to url for image display.
    url = "https://storage.googleapis.com/" + gcs_uri.replace("gs://", "").replace(
        " ", "%20"
    )
    return url


def print_multimodal_prompt(contents: list):
    """
    Given contents that would be sent to Gemini,
    output the full multimodal prompt for ease of readability.
    """
    for content in contents:
        if isinstance(content, Image):
            display_images([content])
        elif isinstance(content, Part):
            url = get_url_from_gcs(content.file_data.file_uri)
            IPython.display.display(load_image_from_url(url))
        else:
            print(content)

 #Load from local file



# Assuming `video_uri` contains the path to the local video file
video_path = "23504.mov"

# Read the contents of the local file into memory
with open(video_path, "rb") as file:
    video_contents = file.read()

# Create a Part object from the file contents
#video = Part.from_data(video_contents, mime_type="video/mov")

# Use a more deterministic configuration with a low temperature
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini
generation_config = GenerationConfig(
    temperature=0.9,          # higher = more creative (default 0.0)
    top_p=0.8,                # higher = more random responses, response drawn from more possible next tokens (default 0.95)
    top_k=40,                 # higher = more random responses, sample from more possible next tokens (default 40)
    candidate_count=1,
    max_output_tokens=1024,   # default = 2048
)

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
}

#BLOCK_ONLY_HIGH - block when high probability of unsafe content is detected
#BLOCK_MEDIUM_AND_ABOVE - block when medium or high probablity of content is detected
#BLOCK_LOW_AND_ABOVE - block when low, medium, or high probability of unsafe content is detected
#BLOCK_NONE - always show, regardless of probability of unsafe content

def generate_response(prompt):
    responses = multimodal_model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False
    )
    return responses.text


while True:
    datamap = db.GET("ASAP", "Outgoing")
    data_map_string= datamap.get("documents")[0].get("data")
    #print(data_map_string)
    decoded_image = base64.b64decode(data_map_string)
        # Convert image data to numpy array
    nparr = np.frombuffer(decoded_image, np.uint8)
        # Decode numpy array to image
    image_file=tempfile.mktemp(suffix='.jpg')
    with open(image_file, "wb") as temp_image_file:
        temp_image_file.write(decoded_image)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow("haha", image)
    cv2.waitKey(1)

    image2 = Image.load_from_file(image_file)
    print(generate_response([image2, "Describe this video"]))


