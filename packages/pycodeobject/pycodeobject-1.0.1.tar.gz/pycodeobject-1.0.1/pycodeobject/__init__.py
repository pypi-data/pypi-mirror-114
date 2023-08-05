"""一个Python对象浏览器模块。
A python object browser with tkinter and command-lines.

"""
import sys,os
try:
    from pycodeobject.code_ import *
except ImportError:
    # 直接双击运行__init__.py
    sys.path.append(os.path.split(os.getcwd())[0])
    from pycodeobject.code_ import *

__email__="3416445406@qq.com"
__author__="七分诚意 qq:3076711200 邮箱:%s"%__email__
__version__="1.0.01"

if __name__=="__main__":
    import doctest
    doctest.testmod(__import__('pycodeobject.code_').code_)
    interactive()
