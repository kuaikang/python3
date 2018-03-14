from PIL import Image
import pytesseract

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
text = pytesseract.image_to_string(Image.open('image/bcd.png'), config=tessdata_dir_config)
print(text)


# img = Image.open('image/c.png')
# region = (0, 15, 15, 15)
# print(img.size)

# # 裁切图片
# cropImg = img.crop(region)
#
# # 保存裁切后的图片
# cropImg.save('image/4_new.png')
