from base64 import b64encode
import os
import requests
import sys

from dotenv import load_dotenv

from gifos.utils.load_config import gifos_settings
from gifos.utils.schemas.imagebb_image import ImgbbImage

"""This module contains a function for uploading an image to ImgBB."""

load_dotenv()
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
ENDPOINT = "https://api.imgbb.com/1/upload"


def upload_imgbb(file_name: str, expiration: int = None) -> ImgbbImage:
    """Upload an image to ImgBB.

    This function uploads an image to ImgBB using the ImgBB API. The function reads the
    image file, encodes it in base64, and sends a POST request to the ImgBB API. The
    function uses the `IMGBB_API_KEY` environment variable for authentication and the
    `ENDPOINT` constant for the API endpoint. If the `debug` configuration value is
    True, the function sets the image expiration time to 10 minutes.

    :param file_name: The name of the image file to upload.
    :type file_name: str
    :param expiration: The expiration time for the image in seconds. If the `debug`
        configuration value is True, this parameter is ignored and the expiration time
        is set to 10 minutes. The value must be between 60 and 15552000 (6 months) if
        provided.
    :type expiration: int, optional
    :return: An `ImgbbImage` object containing the uploaded image's information if the
        upload is successful, otherwise None.
    :rtype: ImgbbImage or None
    """
    if not IMGBB_API_KEY:
        print("ERROR: Please provide IMGBB_API_KEY")
        sys.exit(1)

    if gifos_settings.get("general", {}).get("debug"):
        expiration = 600
        print("INFO: Debugging is true Setting expiration to 10min")
    else:
        if expiration is None:
            pass
        elif expiration < 60 or expiration > 15552000:
            raise ValueError

    with open(file_name, "rb") as image:
        image_name = image.name
        image_base64 = b64encode(image.read())

        data = {
            "key": IMGBB_API_KEY,
            "image": image_base64,
            "name": image_name,
        }
        if expiration:
            data["expiration"] = expiration

        response = requests.post(ENDPOINT, data)
        if response.status_code == 200:
            json_obj = response.json()
            return ImgbbImage(
                id=json_obj["data"]["id"],
                url=json_obj["data"]["url"],
                delete_url=json_obj["data"]["delete_url"],
                file_name=json_obj["data"]["image"]["filename"],
                expiration=json_obj["data"]["expiration"],
                size=json_obj["data"]["size"],
                mime=json_obj["data"]["image"]["mime"],
                extension=json_obj["data"]["image"]["extension"],
            )
        else:
            print(f"ERROR: {response.status_code}")
            return None
