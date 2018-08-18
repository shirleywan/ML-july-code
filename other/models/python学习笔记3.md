控制流:

if 语句
    写法: if ... elif ... else ...  # if后面不用圆括号
    注:在Python中没有switch语句。你可以使用 if..elif..else 语句来完成同样的工作(在某些场合，使用字典会更加快捷。)
    在C/C++里面可以使用 else if ,但这里不行，得写成: else :\n\t if,故此增加关键字 elif

    例:
    number = 23
    # int是一个类，不过这里它只是把一个字符串转换为一个整数(假设这个字符串含有一个有效的整数文本信息)。
    guess = int(raw_input('Enter an integer : '))

    if guess == number:
        print('Congratulations, you guessed it.')
    elif guess < number:
        print('No, it is a little higher than that') # Another block
    else:
        print('No, it is a little lower than that')


while 语句
    只要条件为真，while语句允许你重复执行一块语句。
    注:while语句有一个可选的else从句。else块事实上是多余的，因为可以把其中的语句跟在while语句里面。

    例:
    number = 23
    running = True

    while running:
        guess = int(raw_input('Enter an integer : '))

        if guess == number:
            print('Congratulations, you guessed it.')
            running = False # this causes the while loop to stop
        elif guess < number:
            print('No, it is a little higher than that')
        else:
            print('No, it is a little lower than that')
    else:
        # Do anything else you want to do here
        print('The while loop is over.')


for 循环
    for..in 是另外一个循环语句，它在一序列的对象上 递归 即逐一使用队列中的每个项目。
    else 部分是可选的。如果包含 else,它总是在 for 循环结束后执行一次，除非遇到 break 语句。

    例:
    for i in range(1, 5):
        print(i)
    else:
        print('The for loop is over')

    # 打印结果: 1 至 4 以及 else 的内容
    # range(1,5)给出序列[1, 2, 3, 4]。range默认步长为1,第三个参数是步长。如，range(1,5,2)给出[1,3]。
    # 记住，range包含第一个数,但不包含第二个数。

    注:
    Python的 for 循环从根本上不同于C/C++的 for 循环。类似 foreach 循环。
    在C/C++中，如果你想要写 for (int i = 0; i < 5; i++)，那么用Python，你写成 for i in range(0,5)。

    # 范例：九九乘法表
    # 由于Python2 与Python3的 print 语法不相同，改用string来打印，保证两个版本的输出结果相同。
    str = ''
    for i in range(1,10):
        for j in range(1, i+1):
            str += ('%d * %d = %d \t' % (j, i, i*j))
        str += '\n'
    print(str)


break 语句
    break 语句是用来 终止 循环语句的，即哪怕循环条件没有称为 False 或序列还没有被完全递归，也停止执行循环语句。
    一个重要的注释是，如果你从 for 或 while 循环中 终止 ，任何对应的循环 else 块将不执行。

continue 语句
    continue 语句被用来告诉Python跳过当前循环块中的剩余语句，然后 继续 进行下一轮循环。
    break 语句 和 continue 语句 对于 while 循环 和 for 循环 都有效。

    例(2.x写法):
    while True:
        s = raw_input('Enter something : ')
        if s == 'quit':
            break
        if len(s) < 3:
            print 'Input is not of sufficient length'
            continue
        # Do other kinds of processing here...
        print 'Length of the string is', len(s)

    例(3.x写法):
    while True:
        s = input('Enter something : ')  # 3.x用input()代替raw_input(),且会获取结尾输入的换行符
        s = s[:-1] # 去掉结尾的换行符
        if s == 'quit':
            break
        if len(s) < 3:
            print('Input is not of sufficient length')
            continue
        # Do other kinds of processing here...
        print('Length of the string is', len(s))


函数:

定义函数
    函数通过def关键字定义。
    def关键字后跟一个函数的 标识符 名称，然后跟一对圆括号。圆括号之中可以包括一些变量名，该行以冒号结尾。
    接下来是一块语句，它们是函数体。

    例:
    def sayHello():
        print('Hello World!') # block belonging to the function

    sayHello() # call the function


函数形参
    函数中的参数名称为 形参 而你提供给函数调用的值称为 实参 。

局部变量
    当你在函数定义内声明变量的时候，它们与函数外具有相同名称的其他变量没有任何关系，即变量名称对于函数来说是 局部 的。
    这称为变量的 作用域 。所有变量的作用域是它们被定义的块，从它们的名称被定义的那点开始。

    例:
    x = 50
    def func(x):
        print('x is', x)
        x = 2
        print('Changed local x to', x) # 打印: 2
    func(x)
    print('x is still', x) # 打印: 50, 值没有变


global 语句
    如果要为一个定义在函数外的变量赋值，那么你就得告诉Python这个变量名不是局部的，而是 全局 的。使用global语句完成这一功能。
    没有global语句，是不可能为定义在函数外的变量赋值的。
    你可以使用定义在函数外的变量的值(假设在函数内没有同名的变量)。然而，应避免这样做，因为这降低程序的可读性,不清楚变量在哪里定义的。
    使用global语句可以清楚地表明变量是在外面的块定义的。
    注:可以使用同一个global语句指定多个全局变量。例如 global x, y, z。

    例:
    def func():
        global x
        print('x is', x)
        x = 2
        print('Changed local x to', x)  # 打印: 2

    x = 50
    func()
    print('Value of x is', x)  # 打印: 2, 值被改变了


默认参数值
    如果希望一些参数是 可选 的，这些参数可使用默认值。
    可以在函数定义的形参名后加上赋值运算符(=)和默认值，从而给形参指定默认参数值。
    注意，默认参数值应该是一个参数。

    例:
    def say(message, times = 2):
        print(message * times)

    say('Hello ')     # 打印:Hello Hello
    say('World ', 5)  # 打印:World World World World World

    重要:
    只有在形参表末尾的那些参数可以有默认参数值，即不能在声明函数形参的时候，先声明有默认值的形参而后声明没有默认值的形参。
    这是因为赋给形参的值是根据位置而赋值的。例如，def func(a, b=5)是有效的，但是def func(a=5, b)是 无效 的。


关键参数
    如果某个函数有许多参数，而你只想指定其中的一部分，那么可以通过命名来为这些参数赋值
    ——这被称作 关键参数 ——使用名字(关键字)而不是位置来给函数指定实参。
    这样做有两个优势:
      一、由于我们不必担心参数的顺序，使用函数变得更加简单了。
      二、假设其他参数都有默认值，我们可以只给我们想要的那些参数赋值。

    例:
    def func(a, b=5, c=10):
        print('a is', a, 'and b is', b, 'and c is', c)

    func(3, 7)        # 参数a得到值3，参数b得到值7，而参数c使用默认值10。
    func(25, c=24)    # 根据实参的位置,变量a得到值25。根据命名，即关键参数，参数c得到值24。变量b根据默认值，为5。
    func(c=50, a=100) # 使用关键参数来完全指定参数值。a得到值100,c得到值50。变量b根据默认值，为5。


return 语句
    return语句用来从一个函数 返回 即跳出函数。我们也可选从函数 返回一个值 。

    例:
    def maximum(x, y):
        if x > y:
            return x
        else:
            return y

    print(maximum(2, 3)) # 打印 3


None
    None 是Python中表示没有任何东西的特殊类型(相当于java的 null)。例如，如果一个变量的值为None，可以表示它没有值。
    注意:函数没有返回值的,等价于最后返回return None。通过运行print someFunction()，你可以明白这一点。

    例:
    def someFunction():
        # pass语句在Python中表示一个空的语句块。它后面的代码会照常运行。
        pass

    print(someFunction())


DocStrings
    DocStrings:文档字符串。它是一个重要的工具，帮助你的程序文档更加简单易懂，应该尽量使用它。甚至可以在程序运行的时候，从函数恢复文档字符串！
    在函数的第一个逻辑行的字符串是这个函数的 文档字符串 。注意，DocStrings也适用于模块和类。
    文档字符串的惯例是一个多行字符串，它的首行以大写字母开始，句号结尾。第二行是空行，从第三行开始是详细的描述。 强烈建议遵循这个惯例。

    例:
    def printMax(x, y):
        '''Prints the maximum of two numbers.

        The two values must be integers.'''

        x = int(x) # convert to integers, if possible
        y = int(y)
        if x > y:
            print(x, 'is maximum')
        else:
            print(y, 'is maximum')

    printMax(3, 5)  # 打印: 5 is maximum
    print(printMax.__doc__)   # 打印: Prints the maximum ... must be integers.

    注:
    使用__doc__(注意是两个下划线)调用printMax函数的文档字符串属性。请记住Python把 每一样东西 都作为对象，包括这个函数。
    Python中help()函数即是使用DocStings的了,它只是抓取函数的__doc__属性，然后整洁地展示给你。可以对上面的函数尝试一下: help(printMax)。记住按q退出help。
    自动化工具也可以以同样的方式从你的程序中提取文档。因此强烈建议你对你所写的任何正式函数编写文档字符串。


函数属性 func_*
    在Python 2里，函数的里的代码可以访问到函数本身的特殊属性。在Python 3里，为了一致性，这些特殊属性被重新命名了。

    Python 2 与 Python 3 的比较
          Python 2                  Python 3                说明
      ① a_function.func_name      a_function.__name__     # 包含了函数的名字。
      ② a_function.func_doc       a_function.__doc__      # 包含了在函数源代码里定义的文档字符串(docstring)。
      ③ a_function.func_defaults  a_function.__defaults__ # 是一个保存参数默认值的元组。
      ④ a_function.func_dict      a_function.__dict__     # 一个支持任意函数属性的名字空间。
      ⑤ a_function.func_closure   a_function.__closure__  # 一个由cell对象组成的元组，包含了函数对自由变量(free variable)的绑定。
      ⑥ a_function.func_globals   a_function.__globals__  # 一个对模块全局名字空间的引用，函数本身在这个名字空间里被定义。
      ⑦ a_function.func_code      a_function.__code__     # 一个代码对象，表示编译后的函数体。

 

模块:
    如果要在其他程序中重用很多函数，那么你该使用模块。
    模块基本上就是一个包含了所有你定义的函数和变量的文件。
    为了在其他程序中重用模块，模块的文件名必须以.py为扩展名。

sys模块(标准库模块)
    sys模块包含了与Python解释器和它的环境有关的函数。

    例:
    import sys  # 输入 sys模块。基本上，这句语句告诉Python，我们想要使用这个模块。
    print('The command line arguments are:')
    # 打印调用文件的命令行参数
    for i in sys.argv:
        print(i)

    print('\nThe PYTHONPATH is', sys.path)

    输出:
    $ python using_sys.py we are arguments
    The command line arguments are:
    using_sys.py
    we
    are
    arguments

    The PYTHONPATH is ['/home/swaroop/byte/code', '/usr/lib/python23.zip',
    '/usr/lib/python2.3', '/usr/lib/python2.3/plat-linux2',
    '/usr/lib/python2.3/lib-tk', '/usr/lib/python2.3/lib-dynload',
    '/usr/lib/python2.3/site-packages', '/usr/lib/python2.3/site-packages/gtk-2.0']

    注:
    执行 import sys 语句的时候，它在 sys.path 变量中所列目录中寻找 sys.py 模块。
    如果找到了这个文件，这个模块的主块中的语句将被运行，然后这个模块将能够被你使用。
    注意，初始化过程仅在我们 第一次 输入模块的时候进行。另外，“sys”是“system”的缩写。
    脚本的名称总是sys.argv列表的第一个参数。所以，在这里，'using_sys.py'是sys.argv[0]、'we'是sys.argv[1]。

    sys.path包含输入模块的目录名列表。
    可以观察到sys.path的第一个字符串是空的——这个空的字符串表示当前目录也是sys.path的一部分，这与PYTHONPATH环境变量是相同的。
    这意味着你可以直接输入位于当前目录的模块。否则，你得把你的模块放在sys.path所列的目录之一。

    另外:
    sys.exit() # 程序结束
    sys.stdin、 sys.stdout 和 sys.stderr 分别对应你的程序的标准输入、标准输出和标准错误流。


字节编译的.pyc文件
    输入一个模块相对来说是一个比较费时的事情，所以Python做了一些技巧，以便使输入模块更加快一些。
    一种方法是创建 字节编译的文件，这些文件以.pyc作为扩展名。另外，这些字节编译的文件也是与平台无关的。
    当你在下次从别的程序输入这个模块的时候，.pyc文件是十分有用的——它会快得多，因为一部分输入模块所需的处理已经完成了。


from ... import 语句
    如果你想要直接输入 argv 变量到你的程序中(避免在每次使用它时打sys.)，那么你可以使用 from sys import argv 语句。
    如果你想要输入所有 sys 模块使用的名字，那么你可以使用 from sys import *语句。
    这对于所有模块都适用。
    注意:
        1.使用 from package import item 方式导入包时，这个子项(item)既可以是包中的一个子模块(或一个子包)，也可以是包中定义的其它命名，像函数、类或变量。
          import 语句首先核对是否包中有这个子项，如果没有，它假定这是一个模块，并尝试加载它。如果没有找到它，会引发一个 ImportError 异常。
        2.使用像 import item.subitem.subsubitem 这样的语句时，这些子项必须是包，最后的子项可以是包或模块，但不能是前面子项中定义的类、函数或变量。
        3.应该避免使用 from...import 而使用 import 语句，因为这样可以使你的程序更加易读，也可以避免名称的冲突。


import ... as
    为 import 的模块起一个简称。如: import cPickle as p
    起简称后,下面的语句即可使用简称,如原本的 cPickle.dump() 可写成 p.dump()

模块的 __name__
    每个模块都有一个名称，在模块中可以通过语句来找出模块的名称。
    这在一个场合特别有用——就如前面所提到的，当一个模块被第一次输入的时候，这个模块的主块将被运行。
    假如我们只想在程序本身被使用的时候运行主块，而在它被别的模块输入的时候不运行主块，我们该怎么做呢？这可以通过模块的__name__属性完成。
    每个Python模块都有它的__name__，如果它是'__main__'，这说明这个模块被用户单独运行，我们可以进行相应的恰当操作。

    例:
    # Filename: using_name.py
    if __name__ == '__main__':
        print('This program is being run by itself')
    else:
        print('I am being imported from another module')

    输出:
    $ python using_name.py
    This program is being run by itself

    $ python
    >>> import using_name
    I am being imported from another module


自定义模块
    每个Python程序也是一个模块。

    模块,例:
    # Filename: mymodule.py

    def sayhi():
        print('Hi, this is mymodule speaking.')

    version = '0.1'

    # End of mymodule.py

   上面是一个 模块 的例子。你已经看到，它与我们普通的Python程序相比并没有什么特别之处。
   记住这个模块应该被放置在我们输入它的程序的同一个目录中，或者在 sys.path 所列目录之一。

    用例1:
    import mymodule
    mymodule.sayhi()
    print('Version', mymodule.version)

    注:函数和成员都以点号来使用。

    用例2:  使用from..import语法的版本。
    from mymodule import sayhi, version  # 或者写: from mymodule import *

    sayhi()
    print('Version', version)
