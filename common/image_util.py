from PIL import Image
import pytesseract

text = pytesseract.image_to_string(Image.open('E:/python3.6/Lib/site-packages/pytesseract/test.png'), lang='chi_sim')
print(text)
