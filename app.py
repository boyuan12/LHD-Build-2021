import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "", 
  api_key = "", 
  api_secret = "" 
)

path = input("Path to the file: ")

d = cloudinary.uploader.upload(path,
  overwrite = "true",
)

print(d)

response = requests.get(f'https://api.imagga.com/v2/tags?image_url={d["secure_url"]}', auth=('acc_c646ba294f90d6d', '31b9d9aa741fe405bfaab8138d3635cf'))

print(f"According to imagga API, there are {response.json()['result']['tags'][0]['confidence']}% that it is {response.json()['result']['tags'][0]['tag']['en']}")

