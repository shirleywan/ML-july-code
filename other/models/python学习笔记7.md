Python标准库:

os 模块
    这个模块包含普遍的操作系统功能。如果你希望你的程序能够与平台无关的话，这个模块是尤为重要的。
    os.sep  获取操作系统特定的路径分割符。比如在Linux、Unix下它是'/'，在Windows下它是'\\'，而在Mac OS下它是':'。
    os.name 字符串指示你正在使用的平台。比如对于Windows，它是'nt'，而对于Linux/Unix用户，它是'posix'。
    os.getcwd() 函数得到当前工作目录，即当前Python脚本工作的目录路径。
    os.getenv(key) 函数用来读取环境变量。
    os.putenv(key, value) 函数用来设置环境变量。
    os.listdir(path) 返回指定目录下的所有文件和目录名。
    os.remove(filePath) 函数用来删除一个文件。
    os.system(shellStr) 函数用来运行shell命令，windows平台则是运行批处理命令。
    os.linesep  字符串给出当前平台使用的行终止符。例如，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'。
    os.path.split(pathname)  函数返回一个路径的目录名和文件名。
    os.path.isfile(path) 函数检验给出的路径是否一个文件。
    os.path.isdir(path)  函数分别检验给出的路径是否目录。
    os.path.existe(path) 函数用来检验给出的路径是否真地存在。


unittest 模块(单元测试)
    单元测试的好处：
      在编写代码之前，通过编写单元测试来强迫你使用有用的方式细化你的需求。
      在编写代码时，单元测试可以使你避免过度编码。当所有测试用例通过时，实现的方法就完成了。
      重构代码时，单元测试用例有助于证明新版本的代码跟老版本功能是一致的。
      在维护代码期间，可验证代码是否破坏原有代码的状态。
      在团队编码中，缜密的测试套件可以降低你的代码影响别人代码的机率，提前发现代码与其他人的不可以良好工作。
    单元测试的原则：
      完全自动运行，而不需要人工干预。单元测试几乎是全自动的。
      自主判断被测试的方法是通过还是失败，而不需要人工解释结果。
      独立运行，而不依赖其它测试用例(即使测试的是同样的方法)。即，每一个测试用例都是一个孤岛。

    例：

        #### roman1.py 文件的内容  ####

        # 定义异常类型(这里仅做范例，不执行什么)
        class OutOfRangeError(ValueError): pass
        class NotIntegerError(ValueError): pass

        roman_numeral_map = (('M',  1000),
             ('CM', 900), ('D',  500), ('CD', 400), ('C',  100),
             ('XC', 90),  ('L',  50),  ('XL', 40),  ('X',  10),
             ('IX', 9),   ('V',  5),   ('IV', 4),   ('I',  1))

        # 被测试函数
        def to_roman(n):
            '''convert integer to Roman numeral'''
            # 数值范围判断
            if not ( 0 < n < 4000 ):
                raise OutOfRangeError('number out of range (must be less than 4000)')
            # 类型判断, 内建的 isinstance() 方法可以检查变量的类型
            # isinstance(n, int) 与 type(n) is int 等效
            if not isinstance(n, int):
                raise NotIntegerError('non-integers can not be converted')
            result = ''
            for numeral, integer in roman_numeral_map:
                while n >= integer:
                    result += numeral
                    n -= integer
            return result

 

        #### 测试文件的内容 ####

        import roman1 # 导入被测试的类
        import unittest

        # 需继承 unittest 模块的TestCase 类。TestCase 提供了很多可以用于测试特定条件的有用的方法。
        class KnownValues(unittest.TestCase):
            def setUp(self):
                """初始化"""
                #执行数据库连接，数据初始化等,此函数可不写
                pass

            # setUp 和 tearDown 在执行每个测试函数的前后都会执行
            def tearDown(self):
                """销毁"""
                pass

            # 每一个独立的测试都有它自己的不含参数及没有返回值的方法。如果方法不抛出异常而正常退出则认为测试通过;否则，测试失败。
            # 测试本身是类一个方法，并且该方法以 test 开头命名。如果不是 test 开头，则不会执行。
            def test_to_roman_known_values(self):
                # 对于每一个测试用例， unittest 模块会打印出测试方法的 docstring ，并且说明该测试失败还是成功。
                # 失败时必然打印docstring, 成功时需使用“-v”命令行参数来查看。
                '''to_roman 方法传回的值与用例的数据不相等时,则测试不通过'''
                # 测试的用例，一般是所有明显的边界用例。
                known_values = ( (1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'),
                    (5, 'V'), (6, 'VI'), (7, 'VII'), (8, 'VIII'),
                    (9, 'IX'), (10, 'X'), (50, 'L'), (100, 'C'),
                    (500, 'D'), (1000, 'M'), (31, 'XXXI'), (148, 'CXLVIII'),
                    (3888, 'MMMDCCCLXXXVIII'), (3940, 'MMMCMXL'), (3999, 'MMMCMXCIX') )
                for integer, numeral in known_values:
                    result = roman1.to_roman(integer) # 这里调用真实的方法。如果该方法抛出了异常，则测试被视为失败。
                    self.assertEqual(numeral, result) # 检查两个值是否相等。如果两个值不一致，则抛出异常，并且测试失败。
                    self.assertNotEqual(0, result, '这两个值不应该相等') # 检查两个值是否不相等。
                    self.assertTrue(5 > 0, '5 > 0 都出错，不是吧')
                    self.assertFalse(5 < 0)
                # 对于每一个失败的测试用例， unittest 模块会打印出详细的跟踪信息。
                # 如果所有返回值均与已知的期望值一致，则 self.assertEqual 不会抛出任何异常，于是此次测试最终会正常退出，这就意味着 to_roman() 通过此次测试。
                assert 5 > 0 # 为了更灵活的判断，可使用 assert

            # 测试异常,让被测试的方法抛出异常，这里来验证异常类型。如果预期的异常没有抛出，则测试失败。
            def test_over_value(self):
                '''参数过大或者过小时, to_roman 方法应该抛出异常信息'''
                # assertRaises 方法需要以下参数：你期望的异常、你要测试的方法及传入给方法的参数。
                #(如果被测试的方法需要多个参数的话，则把所有参数依次传入 assertRaises， 它会正确地把参数传递给被测方法的。)
                self.assertRaises(roman1.OutOfRangeError, roman1.to_roman, 4000)
                # 注意是把 to_roman() 方法作为参数传递;没有调用被测方法，也不是把被测方法作为一个字符串名字传递进去
                self.assertRaises(roman1.OutOfRangeError, roman1.to_roman, 0)
                self.assertRaises(roman1.OutOfRangeError, roman1.to_roman, -1)

            # 验证参数类型
            def test_non_integer(self):
                '''如果参数不是 int 类型时， to_roman 方法应该抛出异常'''
                self.assertRaises(roman1.NotIntegerError, roman1.to_roman, 0.5)
                self.assertRaises(roman1.NotIntegerError, roman1.to_roman, 6.0)

        # 在说明每个用例的详细执行结果之后， unittest 打印出一个简述来说明“多少用例被执行了”和“测试执行了多长时间”。
        if __name__ == '__main__':
            # main 方法会执行每个测试用例
            unittest.main()


with 关键字
    从Python 2.5开始有，需要 from __future__ import with_statement。自python 2.6开始，成为默认关键字。
    with 是一个控制流语句, 跟 if/for/while/try 之类的是一类的，with 可以用来简化 try finally 代码，看起来可以比 try finally 更清晰。
    with obj 语句在控制流程进入和离开其后的相关代码中，允许对象obj管理所发生的事情。
    执行 with obj 语句时，它执行 obj.__enter__() 方法来指示正在进入一个新的上下文。当控制流离开该上下文的时候，它就会执行 obj.__exit__(type, value, traceback)。

    "上下文管理协议"context management protocol: 实现方法是为一个类定义 __enter__ 和 __exit__ 两个函数。
    with expresion as variable的执行过程是，首先执行 __enter__ 函数，它的返回值会赋给 as 后面的 variable, 想让它返回什么就返回什么，如果不写 as variable，返回值会被忽略。
    然后，开始执行 with-block 中的语句，不论成功失败(比如发生异常、错误，设置sys.exit())，在with-block执行完成后，会执行__exit__函数。
    这样的过程其实等价于：
    try:
        执行 __enter__()
        执行 with_block.
    finally:
        执行 __exit__()

    只不过，现在把一部分代码封装成了__enter__函数，清理代码封装成__exit__函数。

    例：
        import sys

        class test:
            def __enter__(self):
                print("enter...")
                return 1

            def __exit__(self,*args):
                print("exit...")
                return True

        with test() as t:
            print("t is not the result of test(), it is __enter__ returned")
            print("t is 1, yes, it is {0}".format(t))
            raise NameError("Hi there")
            sys.exit()
            print("Never here")

    注意:
        1) t不是test()的值，test()返回的是"context manager object"，是给with用的。t获得的是__enter__函数的返回值，这是with拿到test()的对象执行之后的结果。t的值是1.
        2) __exit__函数的返回值用来指示with-block部分发生的异常是否要 re-raise ，如果返回 False,则会抛出 with-block 的异常，如果返回 True,则就像什么都没发生。

    在Python2.5中, file objec t拥有 __enter__ 和 __exit__ 方法，__enter__ 返回 object 自己，而 __exit__ 则关闭这个文件：
    要打开一个文件，处理它的内容，并且保证关闭它，你就可以简简单单地这样做：

        with open("x.txt") as f:
            data = f.read()
            do something with data

    补充：
        数据库的连接好像也可以和with一起使用，我在一本书上看到以下内容：
        conn = sqlite.connect("somedb")
        with conn:
            conn.execute("insert into sometable values (?,?)",("foo","bar"))
        在这个例子中，commit()是在所有with数据块中的语句执行完毕并且没有错误之后自动执行的，如果出现任何的异常，将执行rollback()
        操作，再次提示异常
