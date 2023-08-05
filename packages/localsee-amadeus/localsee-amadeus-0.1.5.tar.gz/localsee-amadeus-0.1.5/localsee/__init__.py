import elogger
import os
import sys
import uuid
import glob
import cv2

# rootpath = r'E:\Code\Python\MyPackage\LocalShower\localsee'
# syspath = sys.path
# sys.path = []
# sys.path.append(rootpath)  # 将工程根目录加入到python搜索路径中
# sys.path.extend([os.path.join(rootpath, i) for i in os.listdir(rootpath) if i[0] != "."])
# sys.path.extend(syspath)
from .option import args


# 需求
# 单图像、多图像
# 处理数据选取以及如何处理
# 针对多图像，需要配置文件或用户手写或命令行输入
# 日志，汇报所有的图片的处理情况，汇总处理了多少图片，时间等。。。

def localshower(path: str, select_area: tuple = (200, 200, 60, 60), show_area: tuple = (0, 0),
                scale: int = 3,
                border_size: int = 2, border_color: tuple = (255, 0, 0)) -> object:
    """

    :rtype: object
    """
    # 参数
    # 路径：判断是单图像还是多图像
    # 选框的位置：（）,()默认右上角
    # 选框的边框粗细：默认是2
    # 展示的位置：（）默认左下角
    # 放大的倍数：默认3倍
    # 选框的颜色：默认红色
    # 显示框的颜色：默认红色
    # 创建文件夹
    if os.path.isdir(path):
        folder = os.path.join(path, str(uuid.uuid4()))
        os.mkdir(folder)
        img_list = glob.glob(os.path.join(path, '*.*g'))
        for i, img in enumerate(img_list):
            # 处理图片
            img_name = os.path.basename(img)
            print(img_name)
            single_shower(path=img, folder=folder, select_area=select_area, show_area=show_area, scale=scale,
                          border_size=border_size,
                          border_color=border_color)
    else:
        folder = os.path.join(os.path.dirname(path), str(uuid.uuid4()))
        os.mkdir(folder)
        single_shower(path=path, folder=folder, select_area=select_area, show_area=show_area, scale=scale,
                      border_size=border_size,
                      border_color=border_color)


def single_shower(folder: str, path: str, select_area: tuple = (200, 200, 60, 60), show_area: tuple = (0, 0),
                  scale: int = 3,
                  border_size: int = 2, border_color: tuple = (255, 0, 0)):
    ori_img = cv2.imread(path)
    img_name = os.path.basename(path)
    h, w, c = ori_img.shape
    # 选择框的坐标
    select_x1, select_y1 = select_area[0:2]
    select_x2, select_y2 = (select_area[0] + select_area[2], select_area[1] + select_area[3])
    # 选择框的宽高
    select_width = select_x2 - select_x1
    select_height = select_y2 - select_y1
    # 带框框的图片
    rec = cv2.rectangle(ori_img, (select_x1 - (border_size // 2), select_y1 - (border_size // 2)),
                        (select_x2 + (border_size // 2), select_y2 + (border_size // 2)),
                        border_color, border_size)
    # 框选中的图片
    rec_img = ori_img[select_y1:select_y2, select_x1:select_x2, :]
    # 显示的区域
    resized = cv2.resize(rec_img, (select_width * scale, select_height * scale), interpolation=cv2.INTER_LINEAR)
    # 显示区域
    sx1, sy1 = show_area
    sx1 += border_size
    sy1 += border_size
    rec[sy1:sy1 + select_height * scale, sx1:sx1 + select_width * scale, :] = resized[:, :, :]
    rec2 = cv2.rectangle(rec, (sx1 - (border_size // 2), sy1 - (border_size // 2)),
                         (sx1 + select_width * scale + (border_size // 2),
                          sy1 + select_height * scale + (border_size // 2)),
                         border_color,
                         border_size)
    cv2.imwrite(os.path.join(folder, img_name), rec2)
    # 返回框选后的结果图,放大展示的区域,框选的区域
    return rec2, resized, rec_img


class LocalShower(object):
    def __init__(self):
        self.path = ''
        self.single = True
        self.log = True
        self.config_type = ''
        self.config = ''

    def show(self):
        # 判断路径是多图还是单图
        if self.single:
            self.single_show()
        else:
            self.multi_show()
        return 0

    def single_show(self):
        return 0

    def multi_show(self):
        return 0


if __name__ == '__main__':
    path = args.path
    select_area = tuple(args.select_area)
    show_area = tuple(args.show_area)
    scale = args.scale
    border_size = args.border_size
    border_color = tuple(args.border_color)
    localshower(path=path, select_area=select_area, show_area=show_area, scale=scale, border_size=border_size,
                border_color=border_color)
    print('done')
