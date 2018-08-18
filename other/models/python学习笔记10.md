    threading.Thread类的使用：
    1，在自己的线程类的__init__里调用threading.Thread.__init__(self, name = threadname) # threadname 为线程的名字
    2， run()，通常需要重写，编写代码实现做需要的功能。
    3，getName()，获得线程对象名称
    4，setName()，设置线程对象名称
    5，start()，启动线程
    6，jion(timeout=None)，等待另一线程结束后再运行。如果给出timeout，则最多阻塞timeout秒
    7，setDaemon(bool)，设置子线程是否随主线程一起结束，必须在start()之前调用。默认为False。
    8，isDaemon()，判断线程是否随主线程一起结束。
    9，isAlive()，检查线程是否在运行中。
       此外threading模块本身也提供了很多方法和其他的类，可以帮助我们更好的使用和管理线程。可以参看http://www.python.org/doc/2.5.2/lib/module-threading.html。

http://www.cnblogs.com/tqsummer/archive/2011/01/25/1944771.html
http://blog.sina.com.cn/s/blog_4b5039210100esc1.html
http://sm4llb0y.blog.163.com/blog/static/18912397200981594357140/


16. 多进程 (从 2.6 起增加了子进程级别的并行开发支持 —— multiprocessing)
    #!/usr/bin/env python
    # -*- coding:utf-8 -*-

    import os, time
    from multiprocessing import *

    def test(x):
        print current_process().pid, x
        #time.sleep(1)

    if __name__ == "__main__":
        print "main:", os.getpid()
        p = Pool(5)
        p.map(test, range(13)) # 启动13个子进程
        time.sleep(1)

  1. Process
    我们先从最根本的 Process 入手，看看是如何启动子进程完成并行计算的。上面的 Pool 不过是创建多个 Process，然后将数据(args)提交给多个子进程完成而已。

    import os, time
    from multiprocessing import *

    def test(x):
        print current_process().pid, x
        time.sleep(1)

    if __name__ == "__main__":
        print "main:", os.getpid()
        p = Process(target = test, args = [100])
        p.start()
        p.join()


17. 进程监视(windows)
    # 定期监视某进程是否存在，不存在则执行
    import os,time

    def __Is_Process_Running(imagename):
        '''
           功能：检查进程是否存在
           返回：返回有多少个这进程名的程序在运行，返回0则程序不在运行
        '''
        p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename) # 利用 windows 批处理的 tasklist 命令
        return p.read().count(imagename) # p 是个文件类型，可按文件的操作

    def test():
        '''
           功能：定期地监视测进程是否还在运行，不再运行时执行指定代码
        '''
        while True:
            time.sleep(10)
            pid = __Is_Process_Running('barfoo.exe')
            if pid <= 0:
                # code .....
                break

    if __name__ == "__main__":
        test()


18. 程序退出时执行
    # 注册 atexit 函数来解决
    # 如果中途关闭运行窗口，无法调用结束事件
    import threading
    import time
    import atexit

    def clean():
        print "clean temp data..."

    def test():
        for i in range(10):
            name = threading.currentThread().name
            print name, i
            # time.sleep(1)

    if __name__ == "__main__":
        atexit.register(clean) # 注册程序结束时执行的函数
        threading.Thread(target = test).start()
        time.sleep(1)

        exit(4) # quit() 和 exit() 会等待所有前台线程退出，同时会调用退出函数。
        import sys; sys.exit(4) # 和 exit / quit 作用基本相同。等待前台线程退出，调用退出函数。
        import os; os._exit(4) # os._exit() 通过系统调用来终止进程的，所有线程和退出函数统统滚蛋。

        time.sleep(1)
        print "Ho ..."

    import subprocess


18. 程序退出时执行
    # 通过 subprocess.Popen 函数来解决；但会发生问题，不知道内部是什么原因
    import subprocess
    proc = subprocess.Popen("python test.py")
    proc.wait()

    # 前面的程序结束后，才继续执行下面的代码
    test_file = open('test.txt', 'wb')
    test_file.write('hello') # 这里的写入偶尔会出问题，不知道原因
    test_file.close()


18. 程序退出时执行
    import os

    # 运行另外一个进程
    proxy_server = os.popen('cmd.exe /c start "" barfoo_proxy.exe')
    # 等待这个进程结束(其实是读取程序的输出，但程序如果一直不停止的话，就一直阻塞)，再往下执行
    proxy_server.read()

    # 前面的程序结束后，才继续执行下面的代码
    test_file = open('test.txt', 'wb')
    test_file.write('hello')
    test_file.close()


19. 杀掉进程(windows)
    def kill(pid):
        """ kill process by pid for windows """
        kill_command = "taskkill /F /T /pid %s" % pid
        os.system(kill_command)


20. 反射(自省)
    dir([obj]):                 调用这个方法将返回包含obj大多数属性名的列表（会有一些特殊的属性不包含在内）。obj的默认值是当前的模块对象。
    hasattr(obj, attr):         这个方法用于检查obj是否有一个名为attr的值的属性，返回一个布尔值。
    getattr(obj, attr):         调用这个方法将返回obj中名为attr的属性对象，或者名为attr的函数, 例如如果attr为'bar'，则返回obj.bar。
    setattr(obj, attr, val):    调用这个方法将给obj的名为attr的值的属性赋值为val。例如如果attr为'bar'，则相当于obj.bar = val。
    callable(obj):              如果传入的参数是可以调用的对象或函数，则返回 True, 否则返回 False 。

    例：
        # 测试类
        class Cat(object):
            def __init__(self, name='kitty'):
                self.name = name
            def sayHi(self): #  实例方法，sayHi指向这个方法对象，使用类或实例.sayHi访问
                print(self.name + 'says Hi!') # 访问名为name的字段，使用实例.name访问


        cat = Cat('kitty2')
        print(dir(cat)) # 获取实例的属性名，以列表形式返回
        if hasattr(cat, 'name'): # 检查实例是否有这个属性
            setattr(cat, 'name', 'tiger') # 相当于: cat.name = 'tiger'
        print(getattr(cat, 'name')) # 相当于: print(cat.name)

        getattr(cat, 'sayHi')() # 相当于: cat.sayHi()


        # 下面这段代码列出对象的所有函数或可调用的对象：
        methodList = [method for method in dir(cat) if callable(getattr(cat, method))]

        # globals() 返回一个map，这个map的key是全局范围内对象的名字，value是该对象的实例。
        globals().get('Cat')()  # 相当于执行: Cat();   注意，这用法需要导入相应的类，如果不导入，则会抛出异常。

        # 解决不能直接导入的问题，使用动态导入
        module = __import__('test_lib') # 导入模组, 多重的导入照样使用点运算符, 如: module = __import__('test_lib.test')
        parser = getattr(module, 'test_fun')  # 获取模组里面的对象,可以是函数或者属性或者类
        test_attr = getattr(module, 'test_attr')
        parser()  # 获取模组里面的对象如果是函数或者类，可直接调用
        print(test_attr) # 调用模组里面的属性
        print(dir(module)) # 列表模组里面的所有内容


    http://www.cnblogs.com/huxi/archive/2011/01/02/1924317.html
    http://blog.csdn.net/lokibalder/article/details/3459722


21. @符号修饰函数(有的语言称为:注释)
    python 2.4以后，增加了 @符号修饰函数 对函数进行修饰, python3.0/2.6又增加了对类的修饰。
    修饰符必须出现在函数定义前一行，不允许和函数定义在同一行。也就是说 @A def f(): 是非法的。

        class Person:
            def sayHi(self):  # self参数必须写，正常函数的写法
                print('Hello, how are you?')

            @staticmethod # 申明此方法是一个静态方法，外部可以直接调用
            def tt(a): # 静态方法，第一个参数不需要用 self
                print(a)

            def ff(self):
                self.sayHi() # 正常方法的调用
                self.tt('dd') # 静态方法的调用

        p = Person()
        p.ff() # 正常方法的调用: self参数不需赋值, 必须先 new 出一个类才可以用
        Person.tt('a', 'b') # 可以直接调用


    # 下面的效果类似于: dec1(dec2(test(arg)))
    @dec1
    @dec2
    def test1(arg):
        print(arg)

    #修饰函数还可以带参数, 效果类似于: dec1(arg1,arg2)(test(arg))
    @dec1(arg1,arg2)
    def test2(arg):
        pass


    范例：
    def accepts(*types):
        def check_accepts(f):
            assert len(types) == f.func_code.co_argcount
            def new_f(*args, **kwds):
                for (a, t) in zip(args, types):
                    assert isinstance(a, t), "arg %r does not match %s" % (a,t)
                return f(*args, **kwds)
            new_f.func_name = f.func_name
            return new_f
        return check_accepts

    def returns(rtype):
        def check_returns(f):
            def new_f(*args, **kwds):
                result = f(*args, **kwds)
                assert isinstance(result, rtype), "return value %r does not match %s" % (result,rtype)
                return result
            new_f.func_name = f.func_name
            return new_f
        return check_returns

    @accepts(int, (int,float))
    @returns((int,float))
    def func(arg1, arg2):
        return arg1 * arg2


http://www.python.org/dev/peps/pep-0318/
http://blog.csdn.net/pythoner/article/details/2823260


22. 垃圾回收
    import gc
    gc.collect() # 显示调用垃圾回收

    gc.disable() # 关闭垃圾回收,当程序需要大量内存时可调用这语句,避免频繁的垃圾回收而影响效率
    gc.enable()  # 开启垃圾回收


23. 利用 Python 搭建一个简单的 Web 服务器,快速实现局域网内文件共享。
    1. cd 到准备做服务器根目录的路径下(这目录下的文件将会被共享)
    2. 运行命令：
       python -m Web服务器模块[端口号，默认8000]
       这里的“Web服务器模块”有如下三种：
            BaseHTTPServer: 提供基本的Web服务和处理器类，分别是HTTPServer和BaseHTTPRequestHandler。
            SimpleHTTPServer: 包含执行GET和HEAD请求的SimpleHTTPRequestHandler类。
            CGIHTTPServer: 包含处理POST请求和执行CGIHTTPRequestHandler类。

       运行如: python -m SimpleHTTPServer 8080

    3. 可以在浏览器中访问:
       http://$hostname/:端口号/路径

 

 

 


#############################################################
################## 内置变量 #################################

__all__
    这是一个字符串列表,定义在一个模块出口时使用 from <module> import * 将可以引用到什么变量,但对 import <module> 没有影响。
    没有定义此语句，则 import * 默认的行为是导入所有的符号不以下划线开始的对象。

    例如：
    a1.py 的内容如下:
    __all__=['b','c']
    a='aaa'
    b='bbb'
    c='ccc'

    b1.py 的内容如下:
    import a1
    from a1 import *
    print a1.a # 正常打印
    print b # 正常打印
    print a # 报错了,变量未定义


__call__
    类的调用
    只要定义类的时候，实现 __call__ 函数，这个类型就成为可调用的。
    换句话说，我们可以把这个类型的对象当作函数来使用，相当于 重载了括号运算符。


__del__
    del 类名 # 调用对象的 __del__ 方法


__doc__
    docstring

    例：
    print(Person.__doc__) # 打印类的docstring
    print(Person.func_name.__doc__) # 打印类的方法的docstring


__file__
    当前代码所在的Python模块的文件名。

    例：
    import os, sys
    print( os.path.dirname(os.path.realpath(__file__)) ) # 获取当前目录
    print( os.path.dirname(os.path.dirname(os.path.realpath(__file__))) ) # 获取上一层目录
    print( os.path.dirname(os.path.abspath(sys.argv[0])) ) # 获取当前目录, sys.argv[0] 与 __file__ 一样显示当前文件名
    print( os.getcwd() ) # 获取当前目录
    print( os.path.abspath(os.curdir) ) # 获取当前目录
    print( os.path.abspath( '. ') ) # 获取当前目录, 打印会加上点号，如： /home/holemar/project/ppf_web/.


__init__
    类的构造方法

    例：
    class Human(object):
        def __init__(self, name):
            print(name)

    class Person(Human): # Person 类继承 Human 类
        def __init__(self, name):
            self.name = name # 对象的变量,每个对象独立的
            super(Person, self).__init__(name)  # 调用父类的 __init__ 方法,但这样的调用要求父类必须继承 object 类,或者继承其它的类
            Human.__init__(self, "province") # 这样调用父类的 __init__ 方法也可以


__name__
    每个Python模块都有它的__name__，如果它是'__main__'，这说明这个模块被用户单独运行，我们可以进行相应的恰当操作。

    例:
    if __name__ == '__main__':
        print('This program is being run by itself')
    else:
        print('I am being imported from another module')


__version__
    版本信息

    例如:
    __version__ = '2.6.26'
    print( tuple(int(i) for i in __version__.split('.')) ) # 打印: (2, 6, 26)
    print( float(__version__) ) # 报错


运算符,如大于、小于、等于、加减乘除, 等等
    class Field(object):
        def __init__(self, value):
            self.value = value

        # 小于:  x < y, y > x
        def __lt__(self, value):
            print('__lt__ 被调用啦...')
            return self.value < value
        # 小于等于:  x <= y, y >= x
        def __le__(self, value):
            return self.value <= value
        # x > y, y < x
        def __gt__(self, value):
            return self.value > value
        # x >= y, y <= x
        def __ge__(self, value):
            return self.value >= value

        # 等于: x == y
        def __eq__(self, value):
            return self.value == value
        # 不等于:  x != y, x <> y
        def __ne__(self, value):
            return self.value != value

        # 加:  x + y
        def __add__(self, value):
            return str(self.value) + ' + ' + str(value)
        # y + x
        def __radd__(self, value):
            return str(value) + ' + ' + str(self.value)

        # 减: x - y
        def __sub__(self, value):
            return str(self.value) + ' - ' + str(value)
        # y - x
        def __rsub__(self, value):
            return str(value) + ' - ' + str(self.value)

        # 乘: x * y
        def __mul__(self, value):
            return str(self.value) + ' × ' + str(value)
        # y * x
        def __rmul__(self, value):
            return str(value) + ' × ' + str(self.value)

        # 除: x / y
        def __div__(self, value):
            return str(self.value) + ' ÷ ' + str(value)
        # y / x
        def __rdiv__(self, value):
            return str(value) + ' ÷ ' + str(self.value)
        # 整除: x // y
        def __floordiv__(self, value):
            return str(self.value) + ' // ' + str(value)
        # y // x
        def __rfloordiv__(self, value):
            return str(value) + ' // ' + str(self.value)
        # python2里面不知道怎么调用这个函数,但python3没有了 __div__,除的时候直接调用此函数
        def __truediv__(self, value):
            return str(self.value) + ' / ' + str(value)
        def __rtruediv__(self, value):
            return str(value) + ' / ' + str(self.value)

        # 单元运算符
        # ~x
        def __invert__(self):
            return '~' + str(self.value)
        # -x
        def __neg__(self):
            return '-' + str(self.value)
        # +x
        def __pos__(self):
            return '+' + str(self.value)

        # x[y]
        def __getitem__(self, value):
            return 'this[' + str(value) + ']'
        # x[y] = z
        def __setitem__(self, key, value)
            self[key] = value
        # del x[y]
        def __delitem__(self, value):
            del self[value]
        # x[y:z]
        def __index__(self, y, z):
            return self[y:z]
        # 遍历
        def __iter__(self):
            pass
        # y in x
        def __contains__(self, value): # in 判断,只能返回 True / False
            return False

        # x.name
        #def __getattribute__(self, value): # 覆盖此方法后,调用 self.value 会引起死循环
        #    return 'this.' + str(value)


        # 被特定函数调用时
        # len(x) ,返回值必须大于或等于0
        def __len__(self):
            return 1
        # str(x) ,返回值必须是字符串
        def __str__(self):
            return str(self.value)
        # unicode(x)
        def __unicode__(self):
            return unicode(self.value)

        # abs(x)
        def __abs__(self):
            return abs(self.value)
        # hash(x)
        def __hash__(self):
            return hash(self.value)
        # hex(x)
        def __hex__(self):
            return hex(self.value)

        # int(x)
        def __int__(self):
            return int(self.value)
        # long(x)
        def __long__(self):
            return long(self.value)
        # float(x)
        def __float__(self):
            return float(self.value)

        # oct(x)
        def __oct__(self):
            return oct(self.value)
        # cmp(x, y)
        def __cmp__(self, value):
            return cmp(self.value, value)
        # coerce(x, y)
        def __coerce__(self, value):
            return coerce(self.value, value)
        # divmod(x, y)
        def __divmod__(self, value):
            return divmod(self.value, value)
        # divmod(y, x)
        def __rdivmod__(self, value):
            return divmod(self.value, value)

        # pow(x, y[, z])
        def __pow__(self, value):
            return pow(self.value, value[, z])
        # pow(y, x[, z])
        def __rpow__(self, value):
            return pow(self.value, value[, z])
        # repr(x])
        def __repr__(self, value):
            return repr(self.value)
        # size of S in memory, in bytes
        def __sizeof__(self, value):
            return 1


    a = Field(32)
    print(a < 12)  # 调用 a 的 __lt__
    print(12 > a)  # 调用 a 的 __lt__
    print(a >= 17)
    print(a != 15)
    print(a == 32)
    print(a + 8)   # 调用 a 的 __add__
    print(8 + a)   # 调用 a 的 __radd__
    print(a * 8)   # 调用 a 的 __mul__
    print(8 * a)   # 调用 a 的 __rmul__
    print(a / 8)   # python2时, 调用 a 的 __div__； python3时调用 __truediv__

    print(~a)
    print(-a)
    print(+a)
    #print(a.name2)
    print(a['name3'])
    print('name' in a)

    print(len(a))  # 调用 a 的 __len__
    print(str(a))  # 调用 a 的 __str__
