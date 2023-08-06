import os
import sys
import time
import prettytable as pt
from .file_utils import FileUtils

file_type = {}
dir_total = 0
size_total = 0
total = 0
def scan(root):
    for rt, dirs, files in os.walk(root):
        for d in dirs:
            global dir_total
            dir_total += 1
        for f in files:
            global size_total, total
            if f.find('.') == -1:
                if not file_type.__contains__('unknown'):
                    file_type['unknown'] = [0, 0]
                file_type['unknown'][0] += 1
                size = os.path.getsize(os.path.join(rt, f))
                size_total += size
                total += 1
                file_type['unknown'][1] += size
            else:
                extend_name = f.split(".")[1]
                if not file_type.__contains__(extend_name):
                    file_type[extend_name] = [0, 0]
                file_type[extend_name][0] += 1
                size = os.path.getsize(os.path.join(rt, f))
                size_total += size
                total += 1
                file_type[extend_name][1] += size

def main():
    global file_type, dir_total, size_total, total
    scan(sys.argv[1])
    file_type = sorted(file_type.items(), key = lambda x:x[1][0], reverse = True)
    tb = pt.PrettyTable()
    tb.title = "分析结果"
    tb.field_names = ['文件类型', '文件大小', '文件数量', '大小占比', '数量占比']
    for key,value in file_type:
        amount_pf = ""
        amount = value[0] / total
        if amount * 100 < 0.01:
            amount_pf = "微不足道"
        else:
            amount_pf = "{:.2%}".format(value[0] / total )
        size_pf = ""
        size = value[1] / size_total
        if size * 100 < 0.01:
            size_pf = "微不足道"
        else:
            size_pf = "{:.2%}".format(value[1] / size_total )
        tb.add_row([key, FileUtils.formatFileSize(value[1]), value[0], size_pf, amount_pf])
    print(tb)
    print("文件夹共 {} 个".format(dir_total))

if __name__ == "__main__":
    main()
