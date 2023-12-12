import os
import requests
from base64 import b64encode
from dotenv import load_dotenv
from .schemas.imgbbImage import imgbbImage

load_dotenv()
imgbbToken = os.getenv("IMGBB_API_KEY")


def uploadImgBB(fileName: str, expiration: int = None):
    if expiration is None:
        pass
    elif expiration < 60 or expiration > 15552000:
        raise ValueError

    with open(fileName, "rb") as image:
        imageName = image.name
        imageBase64 = b64encode(image.read())

        url = "https://api.imgbb.com/1/upload"
        data = {
            "key": imgbbToken,
            "image": imageBase64,
            "name": imageName,
        }
        if expiration:
            data["expiration"] = expiration

        response = requests.post(url, data)
        if response.status_code == 200:
            jsonObj = response.json()
            return imgbbImage(
                id=jsonObj["data"]["id"],
                url=jsonObj["data"]["url"],
                deleteUrl=jsonObj["data"]["delete_url"],
                fileName=jsonObj["data"]["image"]["filename"],
                expiration=jsonObj["data"]["expiration"],
                size=jsonObj["data"]["size"],
                mime=jsonObj["data"]["image"]["mime"],
                extension=jsonObj["data"]["image"]["extension"],
            )
        else:
            print(f"ERROR: {response.status_code}")
            return
