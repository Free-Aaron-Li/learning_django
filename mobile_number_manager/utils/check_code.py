import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


def check_code(width=120, height=30, char_length=5, font_size=28, font_file='fonts/Monaco.ttf'):
    code = []
    # 1.创建图片
    img = Image.new('RGB', (width, height), (255, 255, 255))
    # 2.创建画笔
    draw = ImageDraw.Draw(img, mode='RGB')

    # 3.随机字符颜色生成
    def get_random_char():
        return chr(random.randint(65, 90))

    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 4.随机生成字符
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = get_random_char()
        code.append(char)
        h = random.randint(0, 4)
        # 初始x,y值，字符，颜色，字体
        draw.text((i * width / char_length, h), char, get_random_color(), font=font)

    # 5.干扰点
    for i in range(40):
        # 坐标，颜色
        draw.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())

    # 6.干扰圆
    for i in range(40):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        # 起始结束坐标，开始角度，结束角度，颜色
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 7.干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        # 起始结束坐标，颜色
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    # 8.保存图片
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
