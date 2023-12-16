from base64 import b64encode
import os
import requests
import sys

from dotenv import load_dotenv

from gifos.utils.schemas.imagebb_image import ImgbbImage

load_dotenv()
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
ENDPOINT = "https://api.imgbb.com/1/upload"


def upload_imgbb(file_name: str, expiration: int = None) -> ImgbbImage:
    if not IMGBB_API_KEY:
        print("ERROR: Please provide IMGBB_API_KEY")
        sys.exit(1)

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
                file_name=json_obj["data"]["image"]["file_name"],
                expiration=json_obj["data"]["expiration"],
                size=json_obj["data"]["size"],
                mime=json_obj["data"]["image"]["mime"],
                extension=json_obj["data"]["image"]["extension"],
            )
        else:
            print(f"ERROR: {response.status_code}")
            return None
