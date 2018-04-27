from PIL import Image
import pytesseract


def image_recognize(file):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(Image.open(file), lang='chi_sim')
    print(text)
    return text


def fixed_size(infile, outfile):
    """按照固定尺寸处理图片"""
    im = Image.open(infile)
    (x, y) = im.size
    size = (x * 2, y * 2)
    im2 = im.resize(size).convert('RGB')
    out = im2.resize(size, Image.ANTIALIAS)
    out.save(outfile)
    print("按固定尺寸放大图片,处理已完成")


if __name__ == '__main__':
    # fixed_size("F:/a.png", "F:/a_new.png")
    text = image_recognize("F:/tag.png")
    print(text)