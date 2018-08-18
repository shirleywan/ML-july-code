#####################################################
范例:
1.运行系统命令行
    import os
    os_command = 'echo haha...'
    # 运行命令行,返回运行结果(成功时返回0,失败返回1或以上的出错数字)
    result = os.system(os_command)
    if result == 0:
        print('run Successful')
    else:
        print('run FAILED')
    # 注:os.system()函数不推荐使用,它容易引发严重的错误。(可能是因为不具备可移植性)

    #os.system(os_command) # 这命令会弹出一个黑乎乎的cmd运行窗口,而且无法获得输出
    p = os.popen(os_command) # 捕获运行的屏幕输出，以文件类型接收，不再另外弹出窗口
    print(p.read()) # p 是个文件类型，可按文件的操作


2.获取系统时间
    import time,datetime
    time.sleep(2)  # 时间暂停两秒
    print(time.strftime('%Y-%m-%d %H:%M:%S')) # 打印如: 2011-04-13 18:30:10
    print(time.strftime('%Y-%m-%d %A %X', time.localtime(time.time()))) # 显示当前日期； 打印如: 2011-04-13 Wednesday 18:30:10
    print(time.strftime("%Y-%m-%d %A %X", time.localtime())) # 显示当前日期； 打印如: 2011-04-13 Wednesday 18:30:10
    print(time.time()) # 以浮点数形式返回自Linux新世纪以来经过的秒数； 打印如: 1302687844.7
    print(time.ctime(1150269086.6630149)) #time.ctime([sec]) 把秒数转换成日期格式，如果不带参数，则显示当前的时间。打印如: Wed Apr 13 21:13:11 2011

    # 得到今天的日期
    print(datetime.date.today()) # 打印如: 2011-04-13
    # 得到前一天的日期
    print(datetime.date.today() + datetime.timedelta(days=-1)) # 打印如: 2011-04-12
    print(datetime.date.today() - datetime.timedelta(days=1))  # 打印如: 2011-04-14
    # 得到10天后的时间
    print(datetime.date.today() + datetime.timedelta(days=10)) # 打印如: 2011-04-23
    # 得到10小时后的时间，上面的 days 换成 hours
    print(datetime.datetime.now() + datetime.timedelta(hours=10)) # 打印如: 2011-04-14 04:30:10.189000

    #两日期相减(也可以大于、小于来比较):
    d1 = datetime.datetime(2005, 2, 16)
    d2 = datetime.datetime(2004, 12, 31)
    print((d1 - d2).days) # 打印： 47

    #运行时间：
    starttime = datetime.datetime.now()
    time.sleep(1) # 暂停1秒
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds) # 秒, 打印： 1
    print((endtime - starttime).microseconds) # 微秒； 打印： 14000


    日期格式化符号:
    %%: %号本身
    %A: 本地星期(全称),如:Tuesday   %a: 本地星期(简称),如:Tue
    %B: 本地月份(全称),如:February  %b: 本地月份(简称),如:Feb
                                    %c: 本地相应的日期表示和时间表示,如:02/15/11 16:50:57
                                    %d: 月内中的一天(0-31),如:15
    %H: 24进制小时数(0-23)
    %I: 12进制小时数(01-12)
                                    %j: 年内的一天(001-366),如:046
    %M: 分钟(00-59),如:50           %m: 月份(01-12),如:02
                                    %p: 上下午(本地A.M.或P.M.的等价符),如:PM
    %S: 秒钟(00-59),如:57
    %X: 本地的时间,如:16:50:57      %x: 本地的日期,如:02/15/11
    %Y: 四位的年(000-9999)          %y: 两位数的年份表示(00-99)

    %U: 年里的星期数(00-53)从星期天开始,如:07
    %W: 年里的星期数(00-53)从星期一开始,如:07
    %w: 星期(0-6),星期天为星期的开始,如:2 (星期天为0)
    %Z: 当前时区的名称,如:中国标准时间
    %z: 当前时区的名称,如:中国标准时间


3.创建目录
    import os
    pathDir = r'D:\Work' # 不同系统的目录写法有所不同
    if not os.path.exists(pathDir):
        os.mkdir(pathDir) # 创建目录, os.makedirs(pathDir) 创建多个不存在的目录
    target = pathDir + os.sep + 'test.txt'
    print(target)
    # 注意os.sep变量的用法, os.sep 是目录分隔符,这样写方便移植。即在Linux、Unix下它是'/'，在Windows下它是'\\'，而在Mac OS下它是':'。


4.文件操作(读写txt文件)
    filePath = 'poem.txt'
    f = open(filePath, 'w') # 以写的模式打开文件,Python 2.x 需将 open() / io.open() 改成 file()
    for a in range( 0, 10 ):
        s = "%5d %5d\n" % (a, a*a)
        f.write( s ) # 把文本写入文件
    f.close() # 关闭io流

    f2 = open(filePath) # 没有提供模式，则默认是读取,即 'r'
    while True:
        line = f2.readline()
        if len(line) == 0: # 读取结束
            break
        print(line, end=' ') # 避免print自动换行, 此行Python2.x应该写：“print line,”
    f2.close() # close the file

    # 删除文件
    import os
    os.remove(filePath)

    说明:
    一、在pythony 3.0 已经废弃了 file 类。

    二、pythony 3.0 内置 open() 函数的构造函数是:
    open(file, mode="r", buffering=None, encoding=None, errors=None, newline=None, closefd=True)
    1.mode(模式):
      r: 读，只能读文件，如果文件不存在，会发生异常
      w: 写，只能写文件，如果文件不存在，创建该文件；如果文件已存在，先清空，再打开文件
      a: 打开供追加
      b: 二进制模式；一般是组合写法,如: rb 以二进制读方式打开；wb 以二进制写方式打开
      t: 文本模式
      +: 打开一个磁盘文件供更新,一般是组合使用,如:
         rb+: 以二进制读方式打开，可以读、写文件，如果文件不存在，会发生异常
         wb+: 以二进制写方式打开，可以读、写文件，如果文件不存在，创建该文件；如果文件已存在，先清空，再打开文件
      u: 通用换行模式
      默认的模式是 rt，即打开供读取的文本模式。
    2.buffering 关键字参数的期望值是以下三个整数中的一个以决定缓冲策略：
      0: 关闭缓冲
      1: 行缓冲
      > 1: 所填的 int 数=缓冲区大小
      默认: 完全缓冲
    3.encoding 默认的编码方式独立于平台。
    4.关闭文件描述符 closefd 可以是 True 或 False 。
      如果是 False,此文件描述符会在文件关闭后保留。若文件名无法奏效的话，那么必须设为 True 。

    三、清空文件内容
    f.truncate()
    注意：当以 "r+","rb+","w","wb","wb+"等模式时可以执行该功能，即具有可写模式时才可以。

    四、文件的指针定位与查询
    (1)文件指针：
         文件被打开后，其对象保存在 f 中， 它会记住文件的当前位置,以便于执行读、写操作，
         这个位置称为文件的指针( 一个从文件头部开始计算的字节数 long 类型 )。
    (2)文件打开时的位置:
         以"r","r+","rb+" 读方式, "w","w+","wb+"写方式 打开的文件，
         一开始，文件指针均指向文件的头部。
    (3)获取文件指针的值:
         L = f.tell()
    (4)移动文件的指针
         f.seek(偏移量, 选项) # 偏移量 是 long 或者 int 类型，计算偏移量时注意换行符是2,汉字可能是2或3
         选项 =0 时， 表示将文件指针指向从文件头部到 "偏移量"字节处。
         选项 =1 时， 表示将文件指针指向从文件的当前位置，向后移动 "偏移量"字节。
         选项 =2 时， 表示将文件指针指向从文件的尾部，，向前移动 "偏移量"字节。

    五、从文件读取指内容
    1.文本文件(以"rt"方式打开的文件)的读取
      s = f.readline()
      返回值： s 是字符串，从文件中读取的一行，含行结束符。
      说明: (1)如果 len(s) = 0 表示已到文件尾(换行符也是有长度的,长度为2)
            (2)如果是文件的最后一行，有可能没有行结束符
    2.二进制文件(以"rb"、"rb+"、"wb+" 方式打开的文件)的读取
      s = f.read(n)
      说明: (1)如果 len( s ) =0 表示已到文件尾
            (2)文件读取后，文件的指针向后移动 len(s) 字节。
            (3)如果磁道已坏，会发生异常。

    六、向文件写入一个字符串
      f.write( s )
      参数: s 要写入的字符串
      说明: (1)文件写入后，文件的指针向后移动 len(s) 字节。
            (2)如果磁道已坏，或磁盘已满会发生异常。

    七、常用文件操作参考
      [1.os]
        1.重命名：os.rename(old, new)
        2.删除：os.remove(file)
        3.列出目录下的文件：os.listdir(path)
        4.获取当前工作目录：os.getcwd()
        5.改变工作目录：os.chdir(newdir)
        6.创建多级目录：os.makedirs(r"c:\python\test")
        7.创建单个目录：os.mkdir("test")
        8.删除多个目录：os.removedirs(r"c:\python") #删除所给路径最后一个目录下所有空目录。
        9.删除单个目录：os.rmdir("test")
        10.获取文件属性：os.stat(file)
        11.修改文件权限与时间戳：os.chmod(file)
        12.执行操作系统命令：os.system("dir")
        13.启动新进程：os.exec(), os.execvp()
        14.在后台执行程序：osspawnv()
        15.终止当前进程：os.exit(), os._exit()
        16.分离文件名：os.path.split(r"c:\python\hello.py") --> ("c:\\python", "hello.py")
        17.分离扩展名：os.path.splitext(r"c:\python\hello.py") --> ("c:\\python\\hello", ".py")
        18.获取路径名：os.path.dirname(r"c:\python\hello.py") --> "c:\\python"
        19.获取文件名：os.path.basename(r"r:\python\hello.py") --> "hello.py"
        20.判断文件是否存在：os.path.exists(r"c:\python\hello.py") --> True
        21.判断是否是绝对路径：os.path.isabs(r".\python\") --> False
        22.判断是否是目录：os.path.isdir(r"c:\python") --> True
        23.判断是否是文件：os.path.isfile(r"c:\python\hello.py") --> True
        24.判断是否是链接文件：os.path.islink(r"c:\python\hello.py") --> False
        25.获取文件大小：os.path.getsize(filename)
        26.*******：os.ismount("c:\\") --> True
        27.搜索目录下的所有文件：os.path.walk()
        28.文件的访问时间 :  os.path.getatime(myfile) # 这里的时间以秒为单位，并且从1970年1月1日开始算起
        29.文件的修改时间:  os.path.getmtime(myfile)

      [2.shutil]
        1.复制单个文件：shultil.copy(oldfile, newfle)
        2.复制整个目录树：shultil.copytree(r".\setup", r".\backup")
        3.删除整个目录树：shultil.rmtree(r".\backup")

      [3.tempfile]
        1.创建一个唯一的临时文件：tempfile.mktemp() --> filename
        2.打开临时文件：tempfile.TemporaryFile()

      [4.StringIO] #cStringIO是StringIO模块的快速实现模块
        1.创建内存文件并写入初始数据：f = StringIO.StringIO("Hello world!")
        2.读入内存文件数据： print f.read() #或print f.getvalue() --> Hello world!
        3.想内存文件写入数据：f.write("Good day!")
        4.关闭内存文件：f.close()

      [5.glob]
        1.匹配文件：glob.glob(r"c:\python\*.py")


5.文件操作(遍历目录和文件名)
    import os
    import os.path
    rootdir = r"D:\Holemar\1.notes\28.Python\test"
    # os.walk 返回一个三元组，其中parent表示所在目录, dirnames是所有目录名字的列表, filenames是所有文件名字的列表
    for parent,dirnames,filenames in os.walk(rootdir):
        # 所在目录
        print("parent is:" + parent)
        # 遍历此目录下的所有目录(不包含子目录)
        for dirname in dirnames:
           print(" dirname is:" + dirname)
        # 遍历此目录下的所有文件
        for filename in filenames:
           print(" filename with full path:" + os.path.join(parent, filename))

    # 列表显示出某目录下的所有文件及目录(不包括子目录的内容)
    ls = os.listdir(rootdir)


6.文件操作(分割路径和文件名)
    import os.path
    #常用函数有三种：分隔路径，找出文件名，找出盘符(window系统)，找出文件的扩展名。
    spath = "d:/test/test.7z"

    # 下面三个分割都返回二元组
    # 分隔目录和文件名
    p,f = os.path.split(spath)  # 注意二元组的接收
    print("dir is:" + p)    # 打印: d:/test
    print(" file is:" + f)  # 打印: test.7z

    # 分隔盘符和文件名
    drv,left = os.path.splitdrive(spath)
    print(" driver is:" + drv)   # 打印: d:
    print(" left is:" + left)    # 打印: /test/test.7z

    # 分隔文件和扩展名
    f,ext = os.path.splitext(spath)
    print(" f is: " + f)    # 打印: d:/test/test
    print(" ext is:" + ext) # 打印: 7z


7.储存器
    pickle标准模块。它可以在一个文件中储存任何Python对象，之后又可以把它完整无缺地取出来。这被称为 持久地 储存对象。
    在pythony 3.0 已经移除了 cPickle 模块，可以使用 pickle 模块代替。

    import pickle as p # 这里使用 as 简称,方便更改模块时只需改一行代码
    # import cPickle as p # Python 2.x 有这个模块(比pickle快1000倍)

    # 将会把资料保存在这个文件里面
    shoplistfile = 'shoplist.data'

    # 需要保存的资料
    shoplist = ['apple', 'mango', 'carrot', 2, 5]

    # 写入文件
    f = open(shoplistfile, "wb") # 以二进制写入,Python2.x时可不用二进制,但3.x必须
    p.dump(shoplist, f) # dump the object to a file
    f.close()

    # 取出资料
    f = open(shoplistfile, "rb") # 以二进制读取
    storedlist2 = p.load(f)
    print(storedlist2)
    f.close()

    # 删除文件
    import os
    os.remove(shoplistfile)


8.url编码操作
    import urllib,sys

    s = '杭州'
    print(urllib.quote(s)) # url 转码,打印如: %E6%9D%AD%E5%B7%9E
    print(urllib.unquote('%E6%9D%AD%E5%B7%9E')) # url 解码,打印如: 杭州

    # 按所用的编码来转码
    print(urllib.quote(s.decode(sys.stdin.encoding).encode('utf8'))) # 打印如: %E6%9D%AD%E5%B7%9E
    print(urllib.quote(s.decode(sys.stdin.encoding).encode('gbk')))  # 打印如: %BA%BC%D6%DD
    print(urllib.quote(s.decode('gbk').encode('utf8'))) # 指定编码来转码
    print(urllib.quote(u'中国'.encode('utf8'))) # unicode编码的，需encode一下；否则中文会出错
    # decode就是把其他编码转换为unicode，等同于unicode函数；encode就是把unicode编码的字符串转换为特定编码。

    # 一些不希望被编码的url
    print urllib.quote("http://localhost/index.html?id=1") # 打印: http%3A//localhost/index.html%3Fid%3D1
    print urllib.quote("http://localhost/index.html?id=1',':?=/") # 打印: http://localhost/index.html?id=1

    # 查看
    print(u'中国'.__class__) # 打印: <type 'unicode'>
    print('中国'.__class__)  # 打印: <type 'str'>


9.数据库连接
    cx_Oracle : 是一个用来连接并操作 Oracle 数据库的 Python 扩展模块， 支持包括 Oracle 9.2 10.2 以及 11.1 等版本。
      安装：
        需先oracle安装客户端，并配置环境变量：
            ORACLE_HOME＝D:\Oracle\Ora81
　　        PATH=D:\Oracle\Ora81\bin;(其他path的地址)
        下载 cx_Oracle 安装包： http://www.python.net/crew/atuining/cx_Oracle/

      Oracle 示例：
        import cx_Oracle
        print(cx_Oracle.version) # 打印出版本信息
        # 建立连接, 3种不同写法
        conn = cx_Oracle.connect('username/pwssword@localhost:1521/db_name') # 参数连写
        conn = cx_Oracle.connect('username', 'pwssword', 'ip_address:1521/db_name') # 分开3个参数写
        dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'db_name')
        conn = cx_Oracle.connect('username', 'pwssword', dsn_tns) # 分开5个参数写


    MySQLdb   : MySQL 数据库的 Python 扩展模块
        import MySQLdb
                下载地址(tar安装包)： http://sourceforge.net/projects/mysql-python
                 (exe安装文件) http://www.lfd.uci.edu/~gohlke/pythonlibs/

    mongodb:
        下载数据库安装文件： http://www.mongodb.org/downloads
        import pymongo


    其他数据库：
    postgresql PostgreSQL psycopg version 1.x, http://initd.org/projects/psycopg1
    postgresql_psycopg2 PostgreSQL psycopg version 2.x, http://initd.org/projects/psycopg2
    sqlite3 SQLite No adapter needed if using Python 2.5+ Otherwise, pysqlite, http://initd.org/tracker/pysqlite
    ado_mssql Microsoft SQL Server adodbapi version 2.0.1+, http://adodbapi.sourceforge.net/

     MySQL 示例：
        # 0. 导入模块(如果导入出错，说明安装驱动不成功)
        import MySQLdb

        # 1. 数据库联结，默认host为本机, port为3306(各数据库的连接写法有所不同)
        conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="testdb")
        # conn = MySQLdb.Connection(host="localhost", port=3306, user="root", passwd="root", db="testdb") # 与上句一样

        # 2. 选择数据库(如果前面还没有选择数据库的话)
        conn.select_db('database name')

        # 3. 获得cursor
        cursor = conn.cursor()

        # 4.1 执行SQL，查询和增删改都这样写； 查询返回查询结果的行数，增删改返回影响的行数
        cursor.execute("SELECT * FROM tb_member")

        # 4.1.1. cursor位置设定及读取结果(仅查询时可这样用)
        # cursor.scroll(int, mode) # mode可为相对位置或者绝对位置，分别为relative和absolute。
        cursor.scroll(0)

        # 4.1.2. Fetch 及 获取结果(每次Fetch,结果集都会下移,下次获取的是剩下的结果集，除非再 cursor.scroll() 移动结果集)
        print(cursor.fetchone()) # 获取对应位置的资料,返回一个一维元组,打印如：(1L, 'stu1', 'm')
        print(cursor.fetchall()) # 返回结果是个二维元组(所有结果) 打印如：((1L, 'stu1', 'm'), (2L, 'stu2', 'f'))

        # 4.2 execute SQL, 返回影响的行数
        rows = cursor.execute("delete from tb_member where memid=2")
        print(rows) # 返回影响的行数(整数类型), 打印如：1

        # 5. 关闭连接
        cursor.close()
        conn.close()


10.需注意的默认参数
    # 默认参数： 如果调用的时候没指定，那它会是函数定义时的引用；
    # 因此，默认参数建议使用基本类型；如果不是基本类型，建议写 None,然后在函数里面设默认值
