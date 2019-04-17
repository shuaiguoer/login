import base64


# 图片转换
def tra(name, path, style='a+'):
    with open(path, 'rb') as f:
        b64str = base64.b64encode(f.read())
    write_data = name + " = " + "%s" % b64str
    with open('icon.py', style) as f:
        f.write("\n" + write_data)


tra(name='img1', path=r'E:\Python\Code\packing\login.ico', style='w+')
tra(name='img2', path=r'E:\Python\Code\packing\welcome.png')
