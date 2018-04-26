from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string(Image.open('E:/python3.6/Lib/site-packages/pytesseract/test.png'), lang='chi_sim')
print(text)
