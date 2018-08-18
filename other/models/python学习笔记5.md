类的变量和对象的变量
    类的变量: 由一个类的所有对象(实例)共享使用。当某个对象对类的变量做了改动的时候，这个改动会反映到所有其他的实例上。
    对象的变量: 由类的每个对象/实例拥有。它们不是共享的，在同一个类的不同实例中，虽然对象的变量有相同的名称，但是是互不相关的。
    使用的数据成员名称以“双下划线前缀”且不是双下划线后缀,比如__privatevar，Python的名称管理体系会有效地把它作为私有变量。
    惯例: 如果某个变量只想在类或对象中使用，就应该以单下划线前缀。而其他的名称都将作为公共的，可以被其他类/对象使用。

    例:
    class Person:
        '''Represents a person.'''
        population = 0 # 类的变量

        def __init__(self, name):
            '''Initializes the person's data.'''
            # 每创建一个对象都增加1
            Person.population += 1 # 调用类的变量,必须用 类名.变量名,如果写 self.变量名 则是对象的变量了
            self.name = name # 对象的变量,每个对象独立的
            print('(Initializing %s) We have %d persons here.' % (self.name, Person.population))

        def __del__(self):
            '''I am dying.'''
            print('%s says bye.' % self.name)
            Person.population -= 1

        def sayHi(self):
            self.__sayHi2() # 调用私有方法,外部不能调用的

        # 以双下划线开头(但没有双下划线结尾),则变成私有,仅供内部调用
        def __sayHi2(self): # 使用 self.population 也可以读取类的变量,只是改变的时候却只改变对象的变量
            print('Hi, my name is %s. We have %d persons here.' % (self.name, self.population))

    swaroop = Person('Swaroop')
    swaroop.sayHi() # 打印: Swaroop, 1

    kalam = Person('Abdul Kalam')
    kalam.sayHi() # 打印: Abdul Kalam, 2

    swaroop.sayHi() # 打印: Swaroop, 2
    print(Person.population) # 打印: 2
    del swaroop # 调用对象的 __del__ 方法
    print(Person.population) # 打印: 1

    print(Person.__doc__) # 打印类的docstring
    print(Person.__init__.__doc__) # 打印类的方法的docstring


继承
    多态现象:一个子类型在任何需要父类型的场合可以被替换成父类型，即对象可以被视作是父类的实例。
    被继承的类被称为“基本类”或“超类”、“父类”。继承的类被称为“导出类”或“子类”。

    例:
    # 父类
    class Member:
        def __init__(self, name, age):
            self.name = name
            self.age = age
            print('(Initialized Member: %s)' % self.name)

        def tell(self):
            print('Member Name:"%s" Age:"%s"' % (self.name, self.age))

        def tell2(self):
            print('Member haha...')

    # 子类
    class Student(Member): # 继承的父类写括号里面;多继承则写多个,这括号的称为继承元组
        def __init__(self, name, age, marks):
            Member.__init__(self, name, age) # 父类的初始化,需手动写；Python不会自动调用父类的constructor
            self.marks = marks
            print('(Initialized Student: %s)' % self.name)

        def tell(self):
            Member.tell(self) # 调用父类的方法,注意:方法调用之前要加上父类名称前缀，然后把self变量及其他参数传递给它。
            print('Marks: "%d"' % self.marks)

    s = Student('Swaroop', 22, 75)
    s.tell() # 会调用子类的方法
    s.tell2() # 子类没有的，则使用父类的；如果多继承,且父类都有这个方法,则使用继承元组中排前面的


特殊的方法
__init__ 方法
    __init__ 方法在类的一个对象被建立时，马上运行。用来对你的对象做初始化。
    注意，这个名称的开始和结尾都是双下划线。( __init__ 方法类似于C++、C#和Java中的 constructor )

    例:
    class Person:
        def __init__(self, name):
            self.test_name = name
        def sayHi(self):
            print('Hello, my name is ' + self.test_name)
            self.test = 'sss'  # 属性可以随处定义,不需事先定义
            print('the test is ' + self.test)

    p = Person('Swaroop')
    p.sayHi() # 打印: Swaroop , sss
    print('the Person test is ' + p.test) # 打印: sss
    p.test2 = 'haha...'
    print('the Person test2 is ' + p.test2) # 打印: haha...

    名称   说明
    __init__(self,...) 这个方法在新建对象恰好要被返回使用之前被调用。
    __del__(self) 在对象要被删除之前调用。如使用 del 删除时。
    __str__(self) 在我们对对象使用 print 语句或是使用 str() 的时候调用。
    __lt__(self,other) 当使用 小于 运算符 (<) 的时候调用。
    __gt__(self,other) 当使用 大于 运算符 (>) 的时候调用。
    __eq__(self,other) 当使用 等于 运算符 (==) 的时候调用。
    __ne__(self,other) 当使用 不等于 运算符 (!=) 的时候调用。
    __le__(self,other) 当使用 小于等于 运算符 (<=) 的时候调用。
    __ge__(self,other) 当使用 大于等于 运算符 (>=) 的时候调用。
    __add__(self,other)当使用 加 运算符 (+) 的时候调用。
    __getitem__(self,key) 使用x[key]索引操作符的时候调用。
    __len__(self) 对序列对象使用内建的 len() 函数的时候调用。


try ... except (处理异常)
    使用 try ... except 语句来处理异常。
    except 从句可以专门处理单一的错误或异常，或者一组包括在圆括号内的错误/异常。没有给出错误或异常的名称，则处理所有的错误和异常。
    如果某个错误或异常没有被处理，默认的Python处理器就会被调用。它会终止程序的运行，并且打印一个消息。
    还可以关联上一个 else 从句,当没有异常发生的时候执行。

    常见异常(可避免的):
        使用不存在的字典关键字 将引发 KeyError 异常。
        搜索列表中不存在的值 将引发 ValueError 异常。
        调用不存在的方法 将引发 AttributeError 异常。
        引用不存在的变量 将引发 NameError 异常。
        未强制转换就混用数据类型 将引发 TypeError 异常。
        导入一个并不存在的模块将引发一个 ImportError 异常。

try ... finally
    假如希望在无论异常发生与否的情况下都执行一段代码,可以使用 finally 块来完成。
    注意，在一个 try 块下，你可以同时使用 except 从句和 finally 块。
    如果在 finally 前面的 try 或者 except, else 等里面有 return 语句,会先跳去执行 finally 再执行 return

raise 语句
    可以使用 raise 语句引发异常(抛出异常)。你还得指明错误/异常的名称和伴随异常触发的异常对象。
    可以引发 Error 或 Exception 类的直接或间接导出类。

    在Python 3里，抛出自定义异常的语法有细微的变化。
        Python 2                                        Python 3
    ① raise MyException                                MyException
    ② raise MyException, 'error message'               raise MyException('error message')
    ③ raise MyException, 'error message', a_traceback  raise MyException('error message').with_traceback(a_traceback)
    ④ raise 'error message'                            unsupported(不支持)
    说明:
    ① 抛出不带自定义错误信息的异常，这种最简单的形式下，语法没有改变。
    ② 抛出带自定义错误信息的异常时:Python 2用一个逗号来分隔异常类和错误信息；Python 3把错误信息作为参数传递给异常类。
    ③ 抛出一个带用户自定义回溯(stack trace,堆栈追踪)的异常。在Python 2和3里这语法完全不同。
    ④ 在Python 2里，可以仅仅抛出一个异常信息。在Python 3里，这种形式不再被支持。2to3将会警告你它不能自动修复这种语法。

    例：
    raise RuntimeError("有异常发生")


生成器的 throw 方法
    在Python 2里，生成器有一个 throw()方法。
    调用 a_generator.throw()会在生成器被暂停的时候抛出一个异常，然后返回由生成器函数获取的下一个值。

       Python 2                                         Python 3
    ① a_generator.throw(MyException)                   a_generator.throw(MyException) # 没有变化
    ② a_generator.throw(MyException, 'error message')  a_generator.throw(MyException('error message'))
    ③ a_generator.throw('error message')               unsupported(不支持)
    说明:
    ① 最简单的形式下，生成器抛出不带用户自定义错误信息的异常。这种情况下，从Python 2到Python 3语法上没有变化 。
    ② 如果生成器抛出一个带用户自定义错误信息的异常，你需要将这个错误信息字符串(error string)传递给异常类来以实例化它。
    ③ Python 2还支持抛出只有异常信息的异常。Python 3不支持这种语法，并且2to3会显示一个警告信息，告诉你需要手动地来修复这处代码。

    例(3.x)语法:
    # 定义一个异常类,继承 Exception
    class ShortInputException(Exception):
        '''A user-defined exception class.'''
        def __init__(self, length, atleast):
            Exception.__init__(self)
            self.length = length
            self.atleast = atleast

    try:
        s = input('Enter something --> ') # Python 2 的输入是 raw_input()
        if len(s) < 3:
            raise ShortInputException(len(s), 3) # 引发异常;Python 2可以写：raise ShortInputException,(len(s), 3)
    # 捕获 EOFError 异常
    except EOFError:
        print('\nWhy did you do an EOF on me?')
    # 捕获一组错误/异常,Python 2 时应该写: “except (RuntimeError, ImportError), e:”
    except (RuntimeError, ImportError) as e:
        pass
    # Python 2 时应该写: “except ShortInputException, x:”
    except ShortInputException as x:
        print('ShortInputException: The input was of length %d,\
              was expecting at least %d' % (x.length, x.atleast))
    # 捕获所有异常
    except:
        print('\nWhy did you do an Exception on me?')
    # 没有任何异常时执行
    else:
        print('No exception was raised.')
    # 不管是否有异常,都会执行
    finally:
        print('finally .....')

 

lambda 形式
    lambda 语句被用来创建新的函数对象，并且在运行时返回它们。
    注意, lambda 形式中，只能使用表达式。

    例:
    def make_repeater(n):
        return lambda s: s*n    # 注意: lambda 返回的是函数,而不是表达式的值

    # 注意, twice 接收的是函数, 而不是表达式的值, 所以 twice 是一个函数,而不是值
    twice = make_repeater(2)
    print(twice('word '))       # 因为 twice 是一个函数,这里是调用这个函数,打印结果: word word

    print(make_repeater(3)(5))  # 这里的“make_repeater(3)”可以认为是匿名函数,打印结果: 15


    # 上面例子貌似太过复杂,下面是简单点的写法
    # 记住, twice2 是一个函数
    twice2 = lambda s: s*2

    print(twice2('word '))  # 打印: word word
    print(twice2(5))        # 打印: 10

    # 上面的 twice2 相当于正常的函数这样写(lambda 后面的是参数，而结果是返回冒号后面的表达式)：
    def twice3(s):
        return s*2

    print(twice3('word '))  # 打印: word word
    print(twice3(5))        # 打印: 10


    # 可认为 lambda 是一个匿名函数
    print((lambda s: s*2)('word '))  # 打印: word word

    # 而 def 是不能申明匿名函数的
    print((def (s): return s*2)(10)) # 这写法将会报错
    print((def twice3(s): return s*2)(10)) # 这写法也同样会报错


    # lambda 可以有多个参数
    twice4 = lambda x,y: x*y
    print(twice4('word ', 3))  # 打印: word word word
    print(twice4(5, 3))        # 打印: 15


exec 和 eval
    exec 用来执行储存在字符串或文件中的Python语句。
    eval 用来计算存储在字符串中的有效Python表达式。
    exec 跟 eval 是相似的，但是 exec 更加强大并更具有技巧性。
    eval 只能执行单独一条表达式；但是 exec 能够执行多条语句，导入(import)，函数声明
    实际上 exec 能执行整个Python程序的字符串。

    Python 2 与 Python 3 的比较
            Python 2                                              Python 3
        ① exec codeString                                       exec(codeString)
        ② exec codeString in global_namespace                   exec(codeString, global_namespace)
        ③ exec codeString in global_namespace, local_namespace  exec(codeString, global_namespace, local_namespace)
    说明:
        ① 就像 print 语句在Python 3里变成了一个函数一样, exec 语句在Python 3里也变成一个函数。
        ② exec 可以指定名字空间，代码将在这个由全局对象组成的私有空间里执行。
        ③ exec 还可以指定一个本地名字空间(比如一个函数里声明的变量)。

    例：
    exec('print("Hello World")')  # 执行打印语句
    print(eval('2*3'))  # 打印：6


execfile 语句
    Python 2里的 execfile 语句也可以像执行Python代码那样使用字符串。不同的是 exec 使用字符串，而 execfile 则使用文件。
    在Python 3里,execfile 语句已经被去掉了。如果你真的想要执行一个文件里的Python代码(但是你不想导入它)，你可以通过打开这个文件，读取它的内容，然后调用 compile()全局函数强制Python解释器编译代码，然后调用 exec() 函数。

    Python 2 写的： execfile('a_filename')
    Python 3 写的： exec(compile(open('a_filename', 'rb').read(), 'a_filename', 'exec'))


assert 语句
    assert 语句用来声明某个条件是真的。
    当 assert 语句失败的时候，会引发一个 AssertionError 错误。
    比较常用于检验错误。

    例:
    assert 2 >= 1  # 正常运行
    assert 0 >= 1  # 出现错误


repr 函数
    repr 函数用来取得对象的规范字符串表示。反引号(也称转换符)可以完成相同的功能。
    注意，在大多数时候有 eval(repr(object)) == object。
    基本上, repr 函数和反引号用来获取对象的可打印的表示形式。
    你可以通过定义类的 __repr__ 方法来控制你的对象在被repr函数调用的时候返回的内容。

    例：
    i = ["item"]
    print(repr(i)) # 打印：['item']


yield 用法
    1) 包含 yield 的函数是一个 Generator, 与平常的函数不同

    例：
        def gen():
            print 'enter'
            yield 1
            print 'next'
            yield 2
            print 'next end'

        print('begin...')
        gen() # 直接调用,发现打印没有执行(与平常的函数不同)
        # 从容器里拿到 iterator 的时候它还什么也不是，处在容器入口处，对于数组来说就是下标为-1的地方，对于函数来说就是函数入口嘛事没干，但是万事俱备就欠 next 。
        print('end...')

        print
        for i in gen():
            print('...%d...' % i)

        # 开始 for in , next 让 itreator 爬行到 yield 语句存在的地方并返回值,
        # 再次 next 就再爬到下一个 yield 语句存在的地方并返回值,依次这样直到函数返回(容器尽头)。

    上面代码的输出是：
        begin...
        end...

        enter
        ...1...
        next
        ...2...
        next end


    2) Generator 里面的 send(msg) 与 next()
        调用 for in 时，相当于是使用 next() 语句或是 send(None)
        如果没有接收值则使用 send 发送的值必须是 None ，否则会出错的，因为 yield 语句没有接收这个值，但 send 又必须传参数的。

    例，用上例的 gen() 函数
        c = gen()
        print(c.next()) # 调用第一个 yield
        print(c.send(None)) # 调用第二个 yield, 这里 next() 与 send(None) 是同样效果的
        print(c.next()) # 第三次调用则出错了，因为数组下标越界, 抛出 StopIteration 的异常； 但会把最后的“next end”打印出来，前两个是没法把它打印出来的


        # send(msg) 貌似没法把 msg 传到参数中
        def gen2(m):
            for i in range(10):
                print(m)
                yield i + 101

        d = gen2('***')
        print(c.next())
        print(c.send(5555)) # 打印的依然是 ***, 而不是 5555


    3) throw() 与 close() 中断 Generator
        中断 Generator 是一个非常灵活的技巧，可以通过 throw 抛出一个 GeneratorExit 异常来终止 Generator 。 Close() 方法作用是一样的，其实内部它是调用了 throw(GeneratorExit) 的。我们看：

        def close(self):
            try:
                self.throw(GeneratorExit)
            except (GeneratorExit, StopIteration):
                pass
            else:
                raise RuntimeError("generator ignored GeneratorExit")  # Other exceptions are not caught

    因此，当我们调用了 close() 方法后，再调用 next() 或是 send(msg) 的话会抛出一个异常
    例，继续用前面例的 gen() 函数
        c = gen()
        print(c.next()) # 调用第一个 yield
        c.close()
        print(c.next()) # 调用第二个 yield 出错了，抛出 StopIteration 的异常, 因为前面的 close 已经关闭它了
