import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name='dljndgwcl',
    api_key='829619775481739',
    api_secret='yLunbkW41qpLT_BTLbxQfViAtEY'
)

# Upload an image file directly
response = cloudinary.uploader.upload("car.jpeg")
print(response)