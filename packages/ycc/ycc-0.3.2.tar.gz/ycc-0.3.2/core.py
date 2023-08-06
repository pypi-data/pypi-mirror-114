from __init__ import * #排好顺序start变量覆盖
from p.__init__ import *
from p.y import *
from p.yh import *
from p.yz import *
def main():
    A()
    print('\033[1;1m 由于更换颜色太费时费力,所以只加入了部分颜色,请谅解')
    print('\033[7;36m开始使用时间:\033[0m','\033[7;32m',start,'\nWelcome Users!','\033[0m')
    while True:
        print('\033[1;1m')
        print('=====切换/选择模式，请选择=====\n模式1.计算关于圆的计算(输入1执行)\n模式2.计算关于圆柱的计算(输入2执行)\n模式3.计算关于圆环的计算(输入3执行)\n输入其他数字退出')
        yyy=input('请选择模式(输入数字):')
        try:
            yyy=eval(yyy)
        except (IOError,ValueError,TypeError,SyntaxError,EOFError,NameError):
            print('请输入正确数字')
        except ZeroDivisionError:
            print('除数不能为0，emmm，2年级小孩都知道')
        if yyy==1:
            part_y() 
        elif yyy==2:
            part_yz()
        elif yyy==3:
            part_yh()
        else:
            end=sj.now()-start
            print('即将\033[10;31m退出\033[0m,','本次使用时间:',end,'\n程序将在5秒后关闭,谢谢使用')
            dd(5)
            tc('谢谢使用')
#main()
#if __name__=='__main__':
#    main()