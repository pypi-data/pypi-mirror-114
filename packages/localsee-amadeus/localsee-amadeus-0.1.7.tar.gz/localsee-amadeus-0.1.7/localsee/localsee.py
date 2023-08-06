import os
import elogger


# 需求
# 单图像、多图像
# 处理数据选取以及如何处理
# 针对多图像，需要配置文件或用户手写或命令行输入
# 日志，汇报所有的图片的处理情况，汇总处理了多少图片，时间等。。。

# 获取日志对象
def localshower(use_logger=False):
    """
    生成日志对象
    记录消息：日志对象.info('xxx')即可
    例子：
    import elogger
    logger = elogger.get_logger()
    logger.info('hello world!')
    Args:
        directory: 日志存放的目录
        filename: 日志文件的存放路径
        encoding: 日志记录编码格式
        mode: 日志写入格式
        fmt: 日志格式，写法与logging的fmt参数相同
        datefmt: 时间格式，写法与logging的datefmt参数相同
        use_stream: 是否在终端打印日志，True表示是，False表示否

    Returns:
        e_logger: 日志对象 Logger
    """
    if use_logger == True:
        elog = elogger.get_logger()
        elog.info('start elogger')


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
    print('local shower')
