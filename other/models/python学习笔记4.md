包(Packages)
    包通常是使用用“圆点模块名”的结构化模块命名空间。例如， A.B 表示名为"A" 的包中含有名为"B"的子模块。
    使用圆点模块名保存不同类库的包可以避免模块之间的命名冲突。(如同用模块来保存不同的模块架构可以避免变量之间的命名冲突)
    包目录必须要有一个 __init__.py 文件的存在；这是为了防止命名冲突而无意中在随后的模块搜索路径中覆盖了正确的模块。
    最简单的情况下， __init__.py 可以只是一个空文件，不过它也可能包含了包的初始化代码，或者设置了 __all__ 变量。


dir()函数
    使用内建的dir函数来列出模块定义的标识符。标识符有函数、类和变量。
    当你为 dir()提供一个模块名的时候，它返回模块定义的名称列表。如果不提供参数，它返回当前模块中定义的名称列表。

    $ python
    >>> import sys
    >>> dir(sys) # get list of attributes for sys module
    ['__displayhook__', '__doc__', '__excepthook__', '__name__', '__stderr__',
    '__stdin__', '__stdout__', '_getframe', 'api_version', 'argv',
    'builtin_module_names', 'byteorder', 'call_tracing', 'callstats',
    'copyright', 'displayhook', 'exc_clear', 'exc_info', 'exc_type',
    'excepthook', 'exec_prefix', 'executable', 'exit', 'getcheckinterval',
    'getdefaultencoding', 'getdlopenflags', 'getfilesystemencoding',
    'getrecursionlimit', 'getrefcount', 'hexversion', 'maxint', 'maxunicode',
    'meta_path','modules', 'path', 'path_hooks', 'path_importer_cache',
    'platform', 'prefix', 'ps1', 'ps2', 'setcheckinterval', 'setdlopenflags',
    'setprofile', 'setrecursionlimit', 'settrace', 'stderr', 'stdin', 'stdout',
    'version', 'version_info', 'warnoptions']
    >>> dir() # get list of attributes for current module
    ['__builtins__', '__doc__', '__name__', 'sys']
    >>>
    >>> a = 5 # create a new variable 'a'
    >>> dir()
    ['__builtins__', '__doc__', '__name__', 'a', 'sys']
    >>>
    >>> del a # delete/remove a name; 这个得留意
    >>>
    >>> dir()
    ['__builtins__', '__doc__', '__name__', 'sys']
    >>>


数据结构
    可以处理一些 数据 的 结构 。或者说，它们是用来存储一组相关数据的。
    在Python中有三种内建的数据结构——列表、元组和字典。

列表(list, 有的语言称为:数组)
    是处理一组有序项目的数据结构，即你可以在一个列表中存储一个 序列 的项目。
    列表中的项目应该包括在方括号中，每个项目之间用逗号分割。
    可以添加、删除或是搜索列表中的项目。列表是 可变的 数据类型。
    列表对象定义的所有方法可以通过 help(list) 获得完整的知识。我比较习惯称它为“数组”。

    例:
    shoplist = ['apple', 'mango', 'carrot', 'banana']
    #查看长度
    print('I have', len(shoplist),'items to purchase.')
    #遍历
    print('These items are:', end=' ') # 注意这行的结尾,打印时可以不换行,python 2.x应该用逗号结尾
    for item in shoplist:
        print(item, end=' ') # python 2.x 此行应该写：“print item,”

    #添加
    print('\nI also have to buy rice.')
    shoplist.append('rice')
    print('My shopping list is now:', shoplist)

    #排序
    print('I will sort my list now')
    shoplist.sort()
    print('Sorted shopping list is:', shoplist)

    #删除,以及使用下标
    print('The first item I will buy is:', shoplist[0])
    olditem = shoplist[0]
    del shoplist[0]
    print('I bought the', olditem)
    print('My shopping list is now:', shoplist)

    #多维列表时,保存的对象只是引用
    newlist = ['waa','dd']
    shoplist.append(newlist)
    print('My shopping list is now:', shoplist)
    del newlist[0]
    print('My shopping list is now', shoplist)

    # 删除重复, 用 set (对元组也可以这样写)
    L = [1,1,1,2,2]
    print(list(set(L))) # 打印：[1, 2]
    l = [(1, 2), (1, 2), 3, 5, 4, 3, 4, (1, 2), 0, 5]
    l = list(set(l))
    print(l) # 打印: [(1, 2), 0, 3, 4, 5]

    # 复制列表(浅拷贝)
    c = shoplist[:]
    # 复制(深拷贝)
    import copy
    c = copy.deepcopy(shoplist)


元组(tuple)
    元组和列表十分类似，只不过元组和字符串一样是 不可变的 即你不能修改元组。
    元组通过圆括号中用逗号分割的项目定义。
    元组通常用在使语句或用户定义的函数能够安全地采用一组值的时候，即被使用的元组的值不会改变。
    如果你想要知道元组对象定义的所有方法，可以通过 help(tuple) 获得完整的知识。

    例:
    #一维元组
    zoo = ('wolf', 'elephant', 'penguin')
    print('Number of animals in the zoo is %s' % len(zoo))  # 打印: 3

    newlist = ['waa','dd']
    #多维元组
    new_zoo = ('monkey', 'dolphin', zoo, newlist)
    print('Number of animals in the new zoo is %s' % len(new_zoo))  # 打印: 3
    print('All animals in new zoo are %s' % str(new_zoo))  # 打印: ('monkey','dolphin',('wolf','elephant','penguin'),['waa','dd'])
    print('Animals brought from old zoo are %s' % str(new_zoo[2]))  # 打印: ('wolf', 'elephant', 'penguin')
    print('Last animal brought from old zoo is %s' % new_zoo[2][2]) # 打印: penguin

    #多维元组时,保存的对象只是引用
    del newlist[0]
    print('new_zoo is now:' + str(new_zoo) )  # 打印: ('monkey','dolphin',('wolf','elephant','penguin'),['dd'])

    注意:含有0个或1个项目的元组
    一个空的元组(含有0个项目)由一对空的圆括号组成，如myempty = ()。
    含有单个元素的元组必须在第一个(唯一一个)项目后跟一个逗号。如: singleton = (2 , )。
    如果小括号里面只有唯一一个项目,而这个项目后面又没有跟一个逗号的话,Python会认为它是一个表达式。


字典(dict, 有的语言称为:json)
    字典把键(名字)和值(详细情况)联系在一起。
    注意，键必须是唯一的，且只能使用不可变的对象(比如字符串)来作为字典的键，但字典的值没有此限制。应该说只能使用简单的对象作为键。
    键值对在字典中以这样的方式标记：d = {key1 : value1, key2 : value2 }。
    键值对用冒号分割，而各个对用逗号分割，所有这些都包括在花括号中。
    记住字典中的键/值对是没有顺序的。如果要一个特定的顺序，那么应该在使用前自己对它们排序。
    字典是dict类的实例/对象，可以用 help(dict) 来查看其属性和函数。

    例:
    ab = { 'Swaroop': 'swar',
           'Larry'  : 'larry',
           'Spammer': 'spammer'
         }
    print(ab) # 打印: {'Swaroop':'swar', 'Larry':'larry', 'Spammer':'spammer'}
    print("Swaroop's address is %s" % ab['Swaroop'])  # 打印: swar

    # 添加值,或者设值
    ab['Guido'] = 'guido'

    # 删除值
    del ab['Spammer']
    # ab.pop('Spammer') # 也可以用 pop 来删除，但建议后面的这种写法，避免没有这个键时会报错： ab.pop('Spammer', None)

    print('\nThere are %d contacts in the address-book\n' % len(ab)) # 打印: 3
    # 遍历(这写法得留意)
    for name, address in ab.items():
        print('Contact %s at %s' % (name, address))

    # 包含key
    if 'Guido' in ab: # 或者写： if ab.has_key('Guido'):
        print("\nGuido's address is %s" % ab['Guido'])

    # 原字典上创建新字典
    print(ab) # 打印: {'Swaroop':'swar', 'Larry':'larry', 'Guido':'guido'}
    dd = dict(ab, slug_field='slug', test=5) # 创建新字典,字典作为参数的只能放第一个，其余不能再是字典；字典参数可省略
    print(dd) # 打印: {'Swaroop':'swar', 'test':5, 'slug_field':'slug', 'Larry':'larry', 'Guido':'guido'}

    # 建议的取值方法
    print( ab['test'] )  # 这样取值，当字典里面没有对应的key时会报错:“KeyError”
    print( ab.get('test', 'default_value') )  # get取值，当字典里面没有对应的key时可取后面的预设值,预设值是可选的(默认是 None)

    # 所有的键和值
    print(ab.keys())   # 所有的键
    print(ab.values()) # 所有的值

    # 复制(浅拷贝)
    print(ab.copy())
    # 复制(深拷贝)
    import copy
    c = copy.deepcopy(ab)


序列
    列表、元组和字符串都是序列，序列的两个主要特点是“索引”操作符和“切片”操作符。
    索引操作符让我们可以从序列中抓取一个特定项目。(即使用下标)
    切片操作符让我们能够获取序列的一个切片，即一部分序列。(即在下标的中括号里面使用冒号)

    例:
    shoplist = ['apple', 'mango', 'carrot', 'banana']

    # Indexing or 'Subscription' operation
    print('Item 0 is %s' % shoplist[0])
    print('Item 3 is %s' % shoplist[3])
    print('Item -1 is %s' % shoplist[-1])   # 打印:banana   即倒数第一个
    print('Item -2 is %s' % shoplist[-2])   # 打印:carrot   即倒数第二个

    # Slicing on a list
    print('Item 1 to 3 is %s' % shoplist[1:3])      # 打印:['mango', 'carrot']   即下标[1]到[3],包括开始但不包括结束
    print('Item 2 to end is %s' % shoplist[2:])     # 打印:['carrot', 'banana']  即下标[2]到结束,包括最后一个
    print('Item 1 to -1 is %s' % shoplist[1:-1])    # 打印:['mango', 'carrot']   即下标[1]到[-1],包括开始但不包括结束
    print('Item start to end is %s' % shoplist[:])  # 打印整个列表,跟直接写“shoplist”效果一样

    # Slicing on a string (string与列表有同样的操作,)
    name = 'swaroop'
    print('characters 1 to 3 is %s' % name[1:3])     # 打印:wa
    print('characters 2 to end is %s' % name[2:])    # 打印:aroop
    print('characters 1 to -1 is %s' % name[1:-1])   # 打印:waroo
    print('characters start to end is %s' % name[:]) # 打印:swaroop  跟直接写这个字符串一样


参考(引用)
    当你创建一个对象并给它赋一个变量的时候，这个变量仅仅 参考 那个对象，而不是表示这个对象本身！
    也就是说，变量名指向你计算机中存储那个对象的内存。
    这被称作名称到对象的绑定。

    例:
    shoplist = ['apple', 'mango', 'carrot', 'banana']
    mylist = shoplist # mylist 只是对象的另一个名称,他们指向相同的内存空间

    del shoplist[0]

    # 他们此时打印相同的内容,都少了'apple'
    print('shoplist is', shoplist)
    print('mylist is', mylist)

    # 深拷贝,复制成另一个对象(得记住用切片操作符来取得拷贝)
    mylist = shoplist[:] # make a copy by doing a full slice
    del mylist[0] # remove first item

    # 注意，现在他们打印出不同的内容
    print('shoplist is', shoplist)
    print('mylist is', mylist)


列表综合
    通过列表综合，可以从一个已有的列表导出一个新的列表。
    [返回值 for 元素 in 列表 if 条件] 比如 [num for num in xrange(100) if num%2==0] 返回0～99之间的偶数列表

    # 例如，你有一个数的列表，而你想要得到一个对应的列表，使其中所有大于2的数都是原来的2倍。对于这种应用，列表综合是最理想的方法。
    listone = [2, 3, 4]
    listtwo = [2*i for i in listone if i > 2] # 为满足条件(if i > 2)的数指定了一个操作(2*i)，从而导出一个新的列表。
    print(listtwo) # 打印: [6, 8]

    ls=[1,3,5,7] # reduce 在python3去掉了
    print(reduce(lambda x,y:x+y,ls)) # 计算过程就是 1+3=4 然后4+5得到结果9，再加7，以此类推，最后返回最终计算的结果(总和)；打印：16

    # 将字典的key，value倒过来的写法：
    a_dict = {'a': 1, 'b': 2, 'c': 3}
    # python3 的写法:
    b_dict = {value:key for key, value in a_dict.items()}
    # python2 时的写法：
    b_dict = {}
    for key, value in a_dict.iteritems():
        b_dict[value] = key
    print(b_dict) # key与value翻转，打印: {1:'a', 2:'b', 3:'c'}

    说明:
    注意原来的列表并没有发生变化。
    在很多时候，我们都是使用循环来处理列表中的每一个元素，而使用列表综合可以用一种更加精确、简洁、清楚的方法完成相同的工作。

    小心 list 的 += 操作(python2时可以用，python3不可以再这样用)


集合
    Python3 开始有这写法,跟之前的差不多,只是用大括号括起来,如： a = {1, 'aa', 3, 5, 6}
    集合同样可以使用综合计算，如： a = {x for x in range(10) if x % 2 == 0}

 

成员测试 in, not in
    检查是否包含有此内容,返回 True 或者 False, 例如：

    # 1.对字符串
    if 'a' in 'Swaroop':
        print('Yes, it contains the string "a"')

    # 2.对集合(列表、元组和字典)
    if 'genre' in ('genre', 'jazz'):
        print('Yes, it contains the genre')
    print('genre' in ('genre', 'jazz')) # 元组,打印： True
    print('genre' in ['genre', 'jazz']) # 列表,打印： True
    print('genre' in {'genre':'sss', 'jazz':'dddd'}) # 字典,检查key，打印： True
    print('sss' in {'genre':'sss', 'jazz':'dddd'}) # 字典,打印： False


排序
    1.sort方法
      Python语言内置了sort方法，可以很方便地对某个List进行排序
      例如：
        L = [6, 5, 1, 3, 4, 2]
        L.sort()
        print(L) # 打印：[1, 2, 3, 4, 5, 6]
        li=[(2,'a'),(4,'b'),(1,'d')]
        li.sort() # 元组列表排序
        print(li) # 打印： [(1, 'd'), (2, 'a'), (4, 'b')]

    2.自定义排序(例如，按关键词的权重排序，按人的年龄排序，等等)
      若List中每个元素都是2-tuple，tuple中第一个元素为String类型的keyword，第二个元素为该字符串对应的权重(int类型)，希望按照权重排序(从高到低)，则可以这样：

        L = [('b', 1), ('a', 0), ('c', 2), ('d', 3)]
        # L.sort(lambda E1, E2: -cmp(E1[1], E2[1])) # cmp函数里面是需比较的两个值，负号表示倒序。(python2 的写法)
        L.sort(key=lambda d:-d[1]) # Python3的写法，由于去掉了cmp()函数,得传入key参数； python2也可以这样用；负号表示倒序
        print(L) # 打印：[('d', 3), ('c', 2), ('b', 1), ('a', 0)]

    3.dict排序
      对字典的排序，因为每一个项包括一个键值对，所以要选择可比较的键或值进行排序
        sorted(iterable[, cmp[, key[, reverse]]])
        # cmp 和 key 一般使用 lambda
        如：

        d={"ok":1,"no":2}
        # 对字典按键排序，用元组列表的形式返回
        print(sorted(d.items(), key=lambda a:a[0])) # 打印： [('no', 2), ('ok', 1)]
        print(sorted(d)) # 打印：['no', 'ok']
        print(d) # 原字典并未改变，打印：{'ok':1, 'no':2}
        # 对字典按值排序，用元组列表的形式返回
        print(sorted(d.items(), key=lambda d:d[1])) # 打印：[('ok', 1), ('no', 2)]

        # 排序后再转成字典，就无法再保证排序了
        b = sorted(d.items(), key=lambda v:v[0])
        print(b) # 打印： [('no', 2), ('ok', 1)]
        print(dict(b)) # (排序又乱了)打印： {'ok': 1, 'no': 2}


    4.类的排序
        class test:
            def __init__(self,a,b):
                self.a = a
                self.b = b

        test1 = test(5,25)
        test2 = test(50,35)
        test3 = test(10,15)
        tests = [test1, test2, test3]

        # 以 cmp 来指定排序方式, python3不可以这样写(没有cmp参数及cmp函数)
        result = sorted(tests,cmp = lambda x,y: cmp(x.a, y.a))
        # 遍历排序结果，结果是已排序的： a:5  a:10  a:50
        for item in result:
            print("a:%s" % item.a)

        # 以 key 来排序，结果也是可以的
        result2 = sorted(tests,key = lambda d:d.a)
        for item in result2:
            print("a:%s" % item.a)

        # 遍历原资料，原资料的顺序没有改变
        for item in tests:
            print("a:%s" % item.a)

    5.注意：
      python3 由于去掉了 cmp() 函数，可以用“(a > b) - (a < b)”代替“ cmp(a, b) ”

    6.冒泡算法，如下：
        num = [23,2,3,6,18,9,33,13,24,19]
        for i in range(len(num)-1):
            for j in range(len(num)-i-1):
                if (num[j] > num[j+1]):
                    num[j], num[j+1] = num[j+1], num[j] # 置换，这样写比较简便，不需再用临时变量
        print(num)


综合实例：
    在Python中对列表，元组，字典等内置的数据结构的处理是很方便的事情，python借鉴了Lisp中的很多函数式计算的方法来处理列表，可以极大的简化我们的代码。
    1. set():  将元组，列表 转化成没有重复项的集合
    2. list(): 将集合，元组转化成列表
    3. tuple(): 将集合，列表转化成元组

    4. map(func,list):将list的每一个元素传递给func的函数，这个函数有一个参数，且返回一个值，map将每一次调用函数返回的值组成一个新列表返回
    5. filter(func,list):将list的每一个元素传递给func的函数，这个函数有一个参数，返回bool类型的值，filter将返回True的元素组成新列表返回
    6. reduce(func,list):将list的元素，挨个取出来和下一个元素通过func计算后将结果和再下一个元素继续计算


    一、列表去重
        ls = [1,3,2,5,2,1,3,4,6]
        ls = list(set(ls)) # 最简单的列表去除重复

        L = [1, 8, 3, 4, 6, 2, 3, 4, 5]
        kk = [x for x in L if x not in locals()['_[1]']] # 保留原顺序的去除重复,只有 2.6 上可以, 2.7 以上版本不能这样写
        # '_[1]' 是个内部临时变量，可查看:  [x for x, y in locals().items()]


    二、假如有列表：
        books = [
            {"name":"C#从入门到精通",  "price":23.7,  "store":"卓越"},
            {"name":"ASP.NET高级编程", "price":44.5,  "store":"卓越"},
            {"name":"C#从入门到精通",  "price":24.7,  "store":"当当"},
            {"name":"ASP.NET高级编程", "price":45.7,  "store":"当当"},
            {"name":"C#从入门到精通",  "price":26.7,  "store":"新华书店"},
            {"name":"ASP.NET高级编程", "price":55.7,  "store":"新华书店"},
        ]

        2.1 求《ASP.NET高级编程》价格最便宜的店：
        storename=min([b for b in books if b['name']=="ASP.NET高级编程"],key=lambda b:b['price'])["store"]
        过程：先用列表解析取出《ASP.NET高级编程》的列表，通过min函数，比较字典的price键获取price最小的项


        2.2 求在新华书店购买两本书一样一本要花的钱：
        price=sum([b['price'] for b in books if b['store']=="新华书店"])


        2.3 求列表中有那几本书：
        booknames=list(set([b['name'] for b in books]))


        2.4 列表里的书都打5折：
        books=map(lambda b:dict(name=b['name'],price=b['price']*0.5,store=b['store']),books)


        2.5 《C#从入门到精通》的平均价格：
        avg=(lambda ls:sum(ls)/len(ls))([b['price'] for b in books if b['name']=="C#从入门到精通"])


        2.6 求每本书的平均价格：
        book_avg=map(lambda bookname:dict(name=bookname,avg=(lambda ls:sum(ls)/len(ls))([b['price'] for b in books if b['name']==bookname])),list(set([b['name'] for b in books])))

        这段代码放在一行比较难看懂，但是格式化一下就很好懂了，构建的过程如下：

            step1: 要求每本书的平均价格，首先要得到共有几本书，方法见2.3，得到去重的书名列表
            list(set([b['name'] for b in books])) #去重后的书名列表

            step2: 要求每一本书的均价，需要将计算均价的函数映射到每一本书上，于是
            map(
                #计算均价的函数，
                list(set([b['name'] for b in books])) #去重后的书名列表
            )

            step3: 加入计算单本书均价的函数，参考2.5的方法，由于只用一行，所以用lambda来搞定：
            func=lambda bookname:(lambda ls:sum(ls)/len(ls))([b.price for b in books if b['name']==bookname])

            step4: 将计算单本均价的lambda函数加入map中，得到最终结果：
            经过格式化后的结果，前面的单行代码可以格式化为下面容易阅读的形式
            book_avg=map(
                lambda bookname:
                    dict(
                        name = bookname,
                        # 计算单本书均价的函数
                        avg  = (lambda ls:sum(ls)/len(ls)) ([b['price'] for b in books if b['name']==bookname])
                    ),
                #去重后的书名列表
                list(
                     set(
                         [b['name'] for b in books]
                     )
                )
            )


在函数中接收元组和列表(函数的参数数量可以变动,即可变长参数)
    当要使函数接收元组或字典形式的参数的时候，有一种特殊的方法，它分别使用*和**前缀。
    这种方法在函数需要获取可变数量的参数的时候特别有用。
    而且，使用*和**前缀的参数还可以传递给其它函数。

    例:
    # 由于在args变量前有*前缀，所有多余的函数参数都会作为一个元组存储在args中
    def sum(message, *args):
        '''Return the sum of each argument.'''
        total = 0
        # 除了用循环,也可以用下标来读取参数,如: args[0]
        for i in args:
            total += i
        print (str(type(args)) + '  ' + message + ":" + str(total))
        sum2(args) # 这样传过去的 args 是一个元组；打印如： ((3, 5.5),)
        sum2(*args) # 这样传过去的 *args 表示多个参数；打印如：(3, 5.5)

    def sum2(*args):
        print(args)

    sum('hight', 3, 5.5) # 打印: <type 'tuple'>  hight:8.5
    sum('weight', 10)    # 打印: <type 'tuple'>  weight:10


    # 函数参数接收字典用法。使用的是**前缀，多余的参数则会被认为是一个字典的键/值对。
    def printDict(message, **args):
        print(str(type(args)) + '  ' + message + ':' + str(args))
        printDict2(args = args) # 可这样，把 args 当做一个值(里面是字典)，传过去；打印如: {'args': {'a': 3, 'b': 'dd'}}
        printDict2(**args) # 也可这样，把 **args 看做传过来的多个键/值对，传过去；打印如：{'a': 3, 'b': 'dd'}

    def printDict2(**args):
        print(args)

    # 注意:参数为字典时,参数里面必须使用等号,否则运行出错
    printDict('hight', a=3, b='dd') # 打印: <type 'dict'>  hight:{'a': 3, 'b': 'dd'}


    # 可以混合使用*和**前缀的参数, 但是必须 *args 在前, **args 在后,否则编译不通过
    def printMul(message, *args1, **args2):
        print(message + '  args1:' + str(args1) + '  args2:' + str(args2))

    printMul('hello', 5, 4, a=2, b=3) # 打印： hello  args1:(5, 4)  args2:{'a': 2, 'b': 3}


面向对象的编程
    面向过程的编程:根据操作数据的函数或语句块来设计程序的。
    面向对象的编程:把数据和功能结合起来，用称为对象的东西包裹起来组织程序的方法。
    类和对象是面向对象编程的两个主要方面。“类”创建一个新类型，而“对象”是这个类的实例。
    域:属于一个对象或类的变量。
    方法:属于类的函数，被称为类的方法。
    域和方法可以合称为类的属性。
    域有两种类型——属于每个实例/类的对象或属于类本身。它们分别被称为实例变量和类变量。
    类使用class关键字创建。类的域和方法被列在一个缩进块中。

self 参数
    类的方法与普通的函数只有一个特别的区别——它们“必须”有一个额外的第一个参数名称，但是在调用这个方法的时候你不为这个参数赋值，Python会提供这个值。这个特别的变量指对象本身，按照惯例它的名称是self。
    虽然你可以给这个参数任何名称，但是“强烈建议”使用self这个名称——其他名称都是不赞成使用的。
    使用一个标准的名称有很多优点——1.方便别人阅读；2.有些IDE(集成开发环境)也可以帮助你。
    Python中的self等价于C++中的self指针和Java、C#中的this参考。

    例:
    class Person:
        def sayHi(self):  # self参数必须写
            print('Hello, how are you?')

    p = Person()
    p.sayHi() # self参数不需赋值
    print(p)  # 打印: <__main__.Person instance at 0xf6fcb18c>   (已经在__main__模块中有了一个Person类的实例)
