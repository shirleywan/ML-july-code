注:本笔记基于python2.6而编辑,尽量的偏向3.x的语法


Python的特色
  1.简单
  2.易学
  3.免费、开源
  4.高层语言: 封装内存管理等
  5.可移植性: 程序如果避免使用依赖于系统的特性，那么无需修改就可以在任何平台上运行
  6.解释性: 直接从源代码运行程序,不再需要担心如何编译程序,使得程序更加易于移植。
  7.面向对象: 支持面向过程的编程也支持面向对象的编程。
  8.可扩展性: 需要保密或者高效的代码，可以用C或C++编写，然后在Python程序中使用它们。
  9.可嵌入性: 可以把Python嵌入C/C++程序，从而向你的程序用户提供脚本功能。
  10.丰富的库: 包括正则表达式、文档生成、单元测试、线程、数据库、网页浏览器、CGI、FTP、
     电子邮件、XML、XML-RPC、HTML、WAV文件、密码系统、GUI(图形用户界面)、Tk和其他与系统有关的操作。
     除了标准库以外，还有许多其他高质量的库，如wxPython、Twisted和Python图像库等等。
  11.概括: Python确实是一种十分精彩又强大的语言。它合理地结合了高性能与使得编写程序简单有趣的特色。
  12.规范的代码: Python采用强制缩进的方式使得代码具有极佳的可读性。


Python 下载地址
    http://www.python.org/download/

Python 安装：
    windows时，运行安装文件之后，还需要配置环境变量，在环境变量的“Path”后面加上英文的分号及python安装目录
    如：“;C:\promg\python2.6”
    不配置环境变量的话，没法在命令行直接使用python

有两种使用Python运行你的程序的方式
   1.使用交互式的带提示符的解释器
     直接双击运行“python.exe”，在里面输入内容，如： print 'haha...'
   2.使用源文件
     在Python的安装目录下，建一个批处理(test.bat)，写入：
     @echo off
     python.exe test.py
     pause

     而“test.py”里面的内容是需要执行的程序


Python命令行选项
    选项      作用
    -c cmd   在命令行直接执行python代码。如python -c 'print "hello world"'。
    -d       脚本编译后从解释器产生调试信息。同PYTHONDEBUG=1。
    -E       忽略环境变量。
    -h       显示python命令行选项帮助信息。
    -i       脚本执行后马上进入交互命令行模式。同PYTHONINSPECT=1。
    -O       在执行前对解释器产生的字节码进行优化。同 PYTHONOPTIMIZE=1。
    -OO      在执行前对解释器产生的字节码进行优化，并删除优化代码中的嵌入式文档字符串。
    -Q arg   除法规则选项，-Qold(default)，-Qwarn，-Qwarnall，-Qnew。
    -S       解释器不自动导入site.py模块。
    -t       当脚本的tab缩排格式不一致时产生警告。
    -u       不缓冲stdin、stdout和stderr，默认是缓冲的。同PYTHONUNBUFFERED=1。
    -v       产生每个模块的信息。如果两个-v选项，则产生更详细的信息。同PYTHONVERBOSE=x。
    -V       显示Python的版本信息。
    -W arg   出错信息控制。(arg is action:message:category:module:lineno)
    -x       忽略源文件的首行。要在多平台上执行脚本时有用。
    file     执行file里的代码。
    -        从stdin里读取执行代码。


easy_install
    这是个很常用的python安装工具
    可以直接安装ez_setup.py脚本(下载网址： http://peak.telecommunity.com/dist/ez_setup.py):
        python ez_setup.py

    windows 下的使用：
      安装：
        下载: http://peak.telecommunity.com/dist/ez_setup.py
        执行: python ez_setup.py
      使用：
        easy_install.exe -U %modal%  # %modal% 是模块名

    linux 下：
      安装：
        sudo apt-get install python-setuptools
      或者：
        wget -q http://peak.telecommunity.com/dist/ez_setup.py
        sudo python ez_setup.py
      使用：
        sudo easy_install 模块名

        安装完后，最好确保easy_install所在目录已经被加到PATH环境变量里:
        Windows: C:\Python25\Scripts
        Linux: /usr/local/bin

    不能使用easy_install的特殊情况：
        a、安装默认版本的MySQL-python会报错，需要指定版本如下：easy_install "MySQL-python==1.2.2"
        b、有些包直接easy_install会失败，需要自行下载安装：
           wxpython，pil要下载exe安装程序
           robotide因为在pypi上找不到，要下载后再easy_install

    通过easy_install安装软件，相关安装信息会保存到easy-install.pth文件里，路径类似如下形式：
    Windows：C:\Python25\Lib\site-packages\easy-install.pth
    Linux：/usr/local/lib/python25/site-packages/easy-install.pth

    如果想删除通过easy_install安装的软件包，比如说：MySQL-python，可以执行命令：
        easy_install -m MySQL-python

    此操作会从easy-install.pth文件里把MySQL-python的相关信息抹去，剩下的egg文件，你可以手动删除。


版本问题
   python3.0版本较之前的有很大变动，而且不向下兼容。
   Python 2.6作为一个过渡版本，基本使用了Python 2.x的语法和库，同时考虑了向Python 3.0的迁移。即2.6版本兼容2.x和3.0的语法
       Python 2.6保持了对之前版本的全兼容，而且还包含了Python 3.0的新玩意(一些新特性需要通过“from __future__ import”来启用)。
       如，在Python2.6要使用3.0的打印,得写上“ from __future__ import print_function”
   基于早期Python版本而能正常运行于Python 2.6并无警告的程序可以通过一个2 to 3的转换工具无缝迁移到Python 3.0。

   部分函数和语句的改变
      最引人注意的改变是print语句没有了，取而代之的是print函数
      同样的还有exec语句，已经改为exec()函数。去除了<>，全部改用!=。
        在python2.x版本中
          #!/usr/bin/env python
          # 或者上句写: #!/usr/bin/python
          print "Hello, world!"
          或者：
          import sys
          sys.stdout.write("Hello, world\n")

        在python3.x中
          print('Hello world!')
   用迭代器来替代列表
      一些知名的API将不再返回列表。
      而字典的dict.iterkeys()、dict.itervalues()和dict.iteritems()方法将会移除，而你可以使用.keys()、.values()和.items()，它们会返回更轻量级的、类似于集合的容器对象，而不是返回一个列表来复制键值。
      这样做的优点是，可以直接在键和条目上进行集合操作，而不需要再复制一次。
   整型数
      移除了含糊的除法符号('/')，而只返回浮点数。
      在以前的版本中，如果参数是int或者是long的话，就会返回相除后结果的向下取整(floor)，而如果参数是float或者是complex的话，那么就会返回相除后结果的一个恰当的近似。
      在2.6版本中可以通过from __future__ import division来启用这项特性。


python2 to python3 问题
    1.print 语句
           2.x                        3.x                           说明
       ① print                      print()                      # 输出一个空白行
       ② print 1                    print(1)                     # 输出一个单独的值
       ③ print 1, 2                 print(1, 2)                  # 输出多个值，以空格分割
       ④ print 1, 2,                print(1, 2, end=' ')         # 输出时取消在末尾输出回车符。
       ⑤ print >>sys.stderr, 1, 2   print(1, 2, file=sys.stderr) # 把输出重定向到一个管道

    2.被重命名或者重新组织的模块
      1)http
        在Python 3里，几个相关的HTTP模块被组合成一个单独的包，即http。
             2.x                     3.x
        ①  import httplib          import http.client     # http.client 模块实现了一个底层的库，可以用来请求HTTP资源，解析HTTP响应。
        ②  import Cookie           import http.cookies    # http.cookies 模块提供一个蟒样的(Pythonic)接口来获取通过HTTP头部(HTTP header)Set-Cookie发送的cookies
        ③  import cookielib        import http.cookiejar  # 常用的流行的浏览器会把cookies以文件形式存放在磁盘上，http.cookiejar 模块可以操作这些文件。
        ④  import BaseHTTPServer   import http.server     # http.server 模块实现了一个基本的HTTP服务器
            import SimpleHTTPServer
            import CGIHttpServer

      2)urllib
        Python 2有一些用来分析，编码和获取URL的模块，但是这些模块就像老鼠窝一样相互重叠。在Python 3里，这些模块被重构、组合成了一个单独的包，即urllib。
             2.x                                 3.x
        ①  import urllib                       import urllib.request, urllib.parse, urllib.error
        ②  import urllib2                      import urllib.request, urllib.error
        ③  import urlparse                     import urllib.parse
        ④  import robotparser                  import urllib.robotparser
        ⑤  from urllib import FancyURLopener   from urllib.request import FancyURLopener
            from urllib import urlencode        from urllib.parse import urlencode
        ⑥  from urllib2 import Request         from urllib.request import Request
            from urllib2 import HTTPError       from urllib.error import HTTPError

        以前，Python 2里的 urllib 模块有各种各样的函数，包括用来获取数据的 urlopen()，还有用来将URL分割成其组成部分的 splittype(), splithost()和 splituser()函数。
        在python3的 urllib 包里，这些函数被组织得更有逻辑性。2to3将会修改这些函数的调用以适应新的命名方案。
        在Python 3里，以前的 urllib2 模块被并入了 urllib 包。同时，以 urllib2 里各种你最喜爱的东西将会一个不缺地出现在Python 3的 urllib 模块里，比如 build_opener()方法, Request 对象， HTTPBasicAuthHandler 和 friends 。
        Python 3里的 urllib.parse 模块包含了原来Python 2里 urlparse 模块所有的解析函数。
        urllib.robotparse 模块解析 robots.txt 文件。
        处理HTTP重定向和其他状态码的 FancyURLopener 类在Python 3里的 urllib.request 模块里依然有效。 urlencode()函数已经被转移到了 urllib.parse 里。
        Request 对象在 urllib.request 里依然有效，但是像HTTPError这样的常量已经被转移到了 urllib.error 里。

      3)dbm
        所有的DBM克隆(DBM clone)现在在单独的一个包里，即dbm。如果你需要其中某个特定的变体，比如GNU DBM，你可以导入dbm包中合适的模块。
              2.x                3.x
         ①  import dbm         import dbm.ndbm
         ②  import gdbm        import dbm.gnu
         ③  import dbhash      import dbm.bsd
         ④  import dumbdbm     import dbm.dumb
         ⑤  import anydbm      import dbm
             import whichdb

      4)xmlrpc
        XML-RPC是一个通过HTTP协议执行远程RPC调用的轻重级方法。一些XML-RPC客户端和XML-RPC服务端的实现库现在被组合到了独立的包，即xmlrpc。
              2.x                        3.x
         ①  import xmlrpclib           import xmlrpc.client
         ②  import DocXMLRPCServer     import xmlrpc.server
             import SimpleXMLRPCServer

      5)其他模块
             2.x                               3.x
        ①  try:                              import io
                import cStringIO as StringIO  # 在Python 2里，你通常会这样做，首先尝试把cStringIO导入作为StringIO的替代，如果失败了，再导入StringIO。
            except ImportError:               # 不要在Python 3里这样做；io模块会帮你处理好这件事情。它会找出可用的最快实现方法，然后自动使用它。
                import StringIO
        ②  try:                              import pickle
                import cPickle as pickle      # 在Python 2里，导入最快的pickle实现也与上边 io 相似。在Python 3里，pickle模块会自动为你处理，所以不要再这样做。
            except ImportError:
                import pickle
        ③  import __builtin__                import builtins
        ④  import copy_reg                   import copyreg # copyreg模块为用C语言定义的用户自定义类型添加了pickle模块的支持。
        ⑤  import Queue                      import queue   # queue模块实现一个生产者消费者队列(multi-producer, multi-consumer queue)。
        ⑥  import SocketServer               import socketserver # socketserver模块为实现各种socket server提供了通用基础类。
        ⑦  import ConfigParser               import configparser # configparser模块用来解析INI-style配置文件。
        ⑧  import repr                       import reprlib # reprlib 模块重新实现了内置函数 repr()，并添加了对字符串表示被截断前长度的控制。
        ⑨  import commands                   import subprocess # subprocess 模块允许你创建子进程，连接到他们的管道，然后获取他们的返回值。

        builtins模块包含了在整个Python语言里都会使用的全局函数，类和常量。重新定义builtins模块里的某个函数意味着在每处都重定义了这个全局函数。这听起来很强大，但是同时也是很可怕的。


注释
  “#”后面的内容
