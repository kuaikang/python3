import base64



def convert_image():
    # Picture ==> base64 encode
    with open('d:\\FileTest\\Hope_Despair.jpg', 'rb') as fin:
        image_data = fin.read()
        base64_data = base64.b64encode(image_data)

        fout = open('d:\\FileTest\\base64_content.txt', 'w')
        fout.write(base64_data.decode())
        fout.close()


if __name__ == '__main__':
    # base64 encode ==> Picture
    with open('a.txt', 'r') as fin:
        base64_data = fin.read()
        ori_image_data = base64.b64decode(base64_data)

        fout = open('2.png', 'wb')
        fout.write(ori_image_data)
        fout.close()
