import os
from io import BytesIO
from random import randint

from PIL import Image, ImageDraw, ImageFont

from niupi.settings import STATICFILES_DIRS


class VerifyCode:
    def __init__(self, width=100, height=40, size=4):
        '''

        :param width: 验证码图片宽度
        :param height: 验证码图片高度
        :param size: 验证码字符数
        '''
        self.width = width
        self.height = height
        self.size = size

    def output(self):
        im = Image.new("RGB", (self.width, self.height), self.rand_color(200, 255))
        self.pen = ImageDraw.Draw(im)
        self.code = self.genearte_string()
        self.__draw_string()
        self.__draw_point()
        self.__draw_line()
        # im.save('vc.png')
        buf = BytesIO()
        im.save(buf, 'png')
        res = buf.getvalue()
        buf.close()
        return res

    def rand_color(self, low, high):
        return randint(low, high), randint(low, high), randint(low, high)

    def genearte_string(self):
        return str(randint(10 ** (self.size - 1), 10 ** (self.size)))

    def __draw_string(self):
        path = os.path.join(STATICFILES_DIRS[0], 'assets/fonts/yzmfont.ttf')
        font = ImageFont.truetype(path, size=25, encoding='utf-8')
        for i in range(0, self.size):
            ch = self.code[i]
            x = 10 + (self.width - 20) // self.size * i
            y = randint(1, 6)
            self.pen.text((x, y), ch, font=font, fill=self.rand_color(10, 120))

    def __draw_point(self):
        for i in range(200):
            x = randint(1, self.width - 1)
            y = randint(1, self.height - 1)
            self.pen.point((x, y))

    def __draw_line(self):
        for i in range(5):
            x1 = randint(1, self.width - 1)
            y1 = randint(1, self.height - 1)
            x2 = randint(1, self.width - 1)
            y2 = randint(1, self.height - 1)
            self.pen.line([(x1, y1), (x2, y2)], fill=self.rand_color(50, 150))

if __name__ == '__main__':
    vc = VerifyCode()
    vc.output()
    print(vc.code)