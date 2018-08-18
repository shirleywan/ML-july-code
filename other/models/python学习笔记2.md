数据类型
   共4种: 整数、长整数、浮点数和复数。
   1.整数,如:2
   2.长整数,如:22L  # 长整数不过是大一些的整数。Python 3已经取消这种类型,被int取代了。
   3.浮点数,如:3.23 和 52.3E-4  # E标记表示10的幂。在这里，52.3E-4表示52.3 * 10-4。
   4.复数,如:(-5+4j) 和 (2.3-4.6j)

   在Python 2和Python 3的变化:
   1.八进制(octal)数:
     Python 2: x = 0755   # 0开头
     Python 3: x = 0o755  # 0o开头
   2.long 类型
     Python 2有为非浮点数准备的 int 和 long 类型。 int 类型的最大值不能超过 sys.maxint,而且这个最大值是平台相关的。
       整数可以通过在数字的末尾附上一个L来定义长整型，显然，它比 int 类型表示的数字范围更大。
     Python 3里，只有一种整数类型 int,大多数情况下，它很像Python 2里的长整型。
       由于已经不存在两种类型的整数，所以就没有必要使用特殊的语法去区别他们。

     由于 long 类型在Python 3的取消,引起以下改变
          Python 2              Python 3            说明
      ① x = 1000000000000L    x = 1000000000000   # 十进制的普通整数
      ② x = 0xFFFFFFFFFFFFL   x = 0xFFFFFFFFFFFF  # 十六进制的普通整数
      ③ long(x)               int(x)              # long()函数没有了。可以使用int()函数强制转换一个变量到整型。
      ④ type(x) is long       type(x) is int      # 检查一个变量是否是整型
      ⑤ isinstance(x, long)   isinstance(x, int)  # 也可以使用 isinstance()函数来检查数据类型
   3.sys.maxint(sys.maxsize)
     由于长整型和整型被整合在一起了, sys.maxint常量不再精确。
     因为这个值对于检测特定平台的能力还是有用处的，所以它被Python 3保留，并且重命名为 sys.maxsize。
         Python 2                Python 3
     ① from sys import maxint  from sys import maxsize  # maxint变成了maxsize。
     ② a_function(sys.maxint)  a_function(sys.maxsize)  # 所有的sys.maxint都变成了sys.maxsize。

  int 是 types.IntType 的代名词
    print(id(int)) # 打印如：505210872
    import types;print(id(types.IntType)) # 打印如：505210872


标识符的命名
    变量是标识符的例子。 标识符 是用来标识 某样东西 的名字。在命名标识符的时候，你要遵循这些规则：
    1.标识符的第一个字符必须是字母表中的字母(大写或小写)或者一个下划线(‘_’)。
    2.标识符名称的其他部分可以由字母(大写或小写)、下划线(‘_’)或数字(0-9)组成。
    3.标识符名称是对大小写敏感的。例如，myname和myName不是一个标识符。
    有效 标识符名称的例子有i、__my_name、name_23和a1b2_c3。
    无效 标识符名称的例子有2things、this is spaced out和my-name。

 

逻辑行与物理行
  物理行是在编写程序时文本的一行。逻辑行是程序的一个语句。
  Python假定每个 物理行 对应一个 逻辑行 。 他希望每行都只使用一个语句，这样使得代码更加易读。
  1. 如果你想要在一个物理行中使用多于一个逻辑行，那么你需要使用分号(;)来特别地标明这种用法。
     分号表示一个逻辑行/语句的结束。
     如: i = 5; print i; # 强烈建议你坚持在每个物理行只写一句逻辑行。 让程序见不到分号，而更容易阅读。
  2. 明确的行连接
     在多个物理行中写一个逻辑行,行结尾用反斜杠标明
     如: s = 'This is a string. \
         This continues the string.'
         # 上面这两行是一个逻辑行,打印是: This is a string. This continues the string.
         print \
         i
         # 上面这两行也是一个逻辑行, 等同于: print i
  3. 暗示的行连接
     在多个物理行中写一个逻辑行,行结尾不需要使用反斜杠标明。
     这种情况出现在逻辑行中使用了圆括号、方括号或波形括号的时候。
  4. 缩进
     行首的空白是重要的。在逻辑行首的空白(空格和tab符)用来决定逻辑行的缩进层次，从而用来决定语句的分组。
     同一层次的语句必须有相同的缩进。每一组这样的语句称为一个块。
     不要混合使用tab符和空格来缩进，因为这在跨越不同的平台的时候，无法正常工作。强烈建议只使用一种风格来缩进。


语法规则
   1.缩进规则
     一个模块的界限，完全是由每行的首字符在这一行的位置来决定的(而不是花括号{})。这一点曾经引起过争议。
     不过不可否认的是，通过强制程序员们缩进，Python确实使得程序更加清晰和美观。
     在逻辑行首的空白(空格和tab)用来决定逻辑行的缩进层次，从而用来决定语句的分组。错误的缩进会引发错误。
     注意: 强制缩进的问题,最常见的情况是tab符和空格的混用会导致错误，而这是用肉眼无法分别的。
   2.变量没有类型
     使用变量时只需要给它们赋值。 不需要声明或定义数据类型。
   3.单语句块
     如果你的语句块只包含一句语句，那么你可以在条件语句或循环语句的同一行指明它。如: if 1!=2: print('Yes')
     强烈建议不要使用这种缩略方法。这会破坏Python清晰美观的代码风格,违背设计者的初衷。
     如果是在Python解释器输入,它的把提示符会改变为...以表示语句还没有结束。这时按回车键用来确认语句已经完整了。然后，Python完成整个语句的执行，并且返回原来的提示符来等待下一句输入。

 

运算符与表达式:

运算符
   运算符   名称          说明
     +       加          两个对象相加,也可以字符串拼接
     -       减          得到负数或是一个数减去另一个数
     *       乘          两个数相乘 或是返回一个被重复若干次的字符串
     **      幂          返回x的y次幂
     /       除          x除以y
     //      取整除      返回商的整数部分
     %       取模        返回除法的余数  # 8%3得到2。 -25.5%2.25得到1.5
     <<      左移        把一个数的二进制向左移一定数目 # 2 << 2得到8
     >>      右移        把一个数的二进制向右移一定数目 # 11 >> 1得到5
     &       按位与      数的按位与 # 5 & 3得到1。
     |       按位或      数的按位或 # 5 | 3得到7。
     ^       按位异或    数的按位异或 # 5 ^ 3得到6
     ~       按位翻转    x的按位翻转是-(x+1) # ~5得到6。
     <       小于        返回x是否小于y
     >       大于        返回x是否大于y
     <=      小于等于    返回x是否小于等于y
     >=      大于等于    返回x是否大于等于y
     ==      等于        比较对象是否相等
     !=      不等于      比较两个对象是否不相等(python3删除了“<>”符号)
     not     布尔“非”  如果x为True，返回False。如果x为False，它返回True。 # x = True; not x返回False。
     and     布尔“与”  如果x为False，x and y返回False，否则它返回y的计算值。 # x=False; y=True; x and y返回False。
     or      布尔“或”  如果x是True，它返回True，否则它返回y的计算值。# x = True; y = False; x or y返回True。
     in, not in          成员测试 (由类里面的 __contains__ 函数指定返回值)
     is, is not          同性测试 (两值的 is 运算是判断引用,与“==”的比较有所不同)


   说明:
     1.加号“+”:有数学相加，也有字符串拼接作用,注意:不能字符串和数字相加。如: 3 + 5得到8; 'a' + 'b'得到'ab'。
     2.乘号“*”:两个数相乘，也可以把字符串重复拼接若干次,如: 2 * 3得到6; 'la' * 3得到'lalala'。
     3.幂“**” :这种写法,其他语言好像没见到过,如: 3 ** 4得到81(即3 * 3 * 3 * 3)
     4.除号“/”:整数的除法得到整数结果,浮点数的得到浮点数,如:4/3得到1(返回相除后结果的向下取整(floor)); 4.0/3或4/3.0得到1.333...
       注意:Python 3.0开始,移除了含糊的除法符号('/')，而只返回浮点数。如:4/3得到1.333...
     5.取整除“//”:将两数相除,然后对结果取整,如: 7 // 3得到2; 4 // 3.0得到1.0
     6.比较运算符:所有比较运算符返回1表示真，返回0表示假。这分别与特殊的变量 True 和 False 等价。注意大小写。
       如果两个操作数都是数字，它们首先被转换为一个共同的类型(如double)。否则，它总是返回 False 。
       5 < 3返回0(即False); 而3 < 5返回1(即True)。比较可以被任意连接: 3 < 5 < 7返回True。
       大于、小于、小于等于、大于等于时:数字跟数字可以比较，字符串跟字符串可以比较，但数字不能跟字符串比较。
       等于、不等于时: 数字跟数字可以比较，字符串跟字符串可以比较，数字跟字符串比较返回 False (表示不相等)
       等于: Python 使用“==”来做比较，用“=”来赋值。但不允许内嵌的赋值，所以不会出现你本以为在做比较而意外的写成赋值的情况。
     7.布尔运算: and 和 or 都是短路运算,没有非短路运算的运算符。
       短路运算:当前面一个表达式可以决定结果时，后面的语句不用再判断。非短路运算时，还照样判断后面的。
       注意：在 and or 运算中，空字符串'',数字0,空列表[],空字典{},空元组(), None,在逻辑运算中都被当作假来处理。
     8.and 和 or 的特殊用法:
       由于语言的松散性,用 and 和 or 在赋值语句时有判断作用。
       1) or 用在赋值语句里，返回第一个逻辑为真的值, 没有逻辑为真的返回最后一个。(如下这写法比较常用)
          如:ss = False or None or 0 or '' or -1 or 'sss'; print(ss) # 打印:-1 (-1作if判断时返回 True)
          设定预设值的写法: edittype = edittype or "text"; # 如果 edittype 之前有值,则取之前的值; 之前为空,则取默认值
       2) and 用在赋值语句里，与 or 刚好相反，返回第一个逻辑为假的值, 没有逻辑为假的返回最后一个。
          如: a = 0 and 1; print(a) # 打印: 0
          a = 2 and 1; print(a) # 打印: 1
          应用： valid = True; valid = valid and checkLength(name, 16); valid = valid and checkLength(name, 16); # 如果前面的验证不通过，则后面的不再验证
       简便的记忆是: and 偏 False, or 偏 True
       要理解 and 和 or 的这种写法，得考虑到它的短路运算特性。它是在做逻辑判断，但返回的是前或后一个的值，而不是返回 True 或 False 。
     9.三目运算符：
       Python 没有三目运算符“cond ? a : b”,但可以使用 and 和 or 来代替(需理解前面的 and 和 or 的特殊用法)，如下：
       1) c = cond and a or b   # 这多数情况下是正确的，但当 a 是空字符串''、数字0等逻辑运算为假的情况下会出错。
       2) c = (cond and [a] or [b])[0] # 即使 a或者b为一个逻辑假的值，将他放入集合中后，就为真了，也就是[False] [None]都不为假。
       3) c = (b, a)[cond and 1 or 0] # 注意 a和b的位置是颠倒的,将表达式结果转成1和0来作为元组下标而选择结果。
       4) c = a if cond else b # 使用 if else 写条件(python特有的写法,建议使用,前3种写法难理解也容易出错)
     10.自增,自减:
       Python 没有“++”和“--”两个语法,自增自减时只能写: i = i + 1 或者 i += 1, 不能用 i++
       这在一定程度上避免出错，因为新手经常搞错“++”放前面还是放后面; 但这也导致 for 循环的写法与其它语言很不同
     11.switch/case 语句
        Python现在不支持这语句，但可以用 range(N) 生成一个 列表
     12.一次性的多比较
        “ if (0 < n < 4000) ”这种写法在python是允许的，它等价于“ if ((0 < n) and (n < 4000)) ”但前者更适合阅读。


运算符优先级
    下面这个表给出Python的运算符优先级，从最低的优先级(最松散地结合)到最高的优先级(最紧密地结合)。
    在一个表达式中，Python会首先计算下表中较下面的运算符，然后在计算列在下表上部的运算符。
    在下表中列在同一行的运算符具有 相同优先级 。例如，+和-有相同的优先级。
    建议使用圆括号来分组运算符和操作数，以便能够明确地指出运算的先后顺序，使程序尽可能地易读。例如，2 + (3 * 4)显然比2 + 3 * 4清晰。

    运算符                   描述
    lambda                  Lambda表达式
    or                      布尔“或”
    and                     布尔“与”
    not x                   布尔“非”
    in，not in              成员测试
    is，is not              同一性测试
    <，<=，>，>=，!=，==    比较
    |                       按位或
    ^                       按位异或
    &                       按位与
    <<，>>                  移位
    +，-                    加法与减法
    *，/，%                 乘法、除法与取余
    +x，-x                  正负号
    ~x                      按位翻转
    **                      指数
    x.attribute             属性参考
    x[index]                下标
    x[index:index]          寻址段
    f(arguments...)         函数调用
    (experession,...)       绑定或元组显示
    [expression,...]        列表显示
    {key:datum,...}         字典显示
    'expression,...'        字符串转换


计算顺序
    默认地，运算符优先级表决定了哪个运算符在别的运算符之前计算。然而，如果要改变它们的计算顺序，得使用圆括号。
    例如，你想要在一个表达式中让加法在乘法之前计算，那么你就得写成类似(2 + 3) * 4的样子。


结合规律
    运算符通常由左向右结合，即具有相同优先级的运算符按照从左向右的顺序计算。例如，2 + 3 + 4被计算成(2 + 3) + 4。
    一些如赋值运算符那样的运算符是由右向左结合的，即a = b + c被处理为a = (b + c)。

对象
    Python 将 "一切皆对象" 贯彻得非常彻底，不区分什么 "值类型" 和 "引用类型"。所谓变量，实质就是一个通用类型指针 (PyObject*)，它仅仅负责指路，至于目标是谁，一概不管。
    Python Object 对象的自身结构了。任何对象，就算一个最简单的整数，它的头部都会拥有 2 个特殊的附加信息，分别是："引用计数" 和 "类型 (type) 指针" 。前者指示 GC 何时回收，而后者标明了对象的身份，如此我们就可以在运行期动态执行对象成员调用。

    连同附加头，一个 "普通" 的整数起码得 12 字节：
    a = 8; import sys; print(sys.getsizeof(a)) # 打印： 12  (python3.2中，打印的是14)
    print(sys.getsizeof(None)) # 打印： 8


字符串
   1.使用单引号“'”引起来: 'Quote me on this'
   2.使用双引号“"”引起来: "What's your name?"
   3.使用三引号('''或"""): 可以指示一个多行的字符串。你可以在三引号中自由的使用单引号和双引号。 /'''
     如:
     """This is a multi-line string. This is the first line.
     "What's your name?," I asked.
     He said "Bond, James Bond."
     """
   4.转义符“\”
     \\  指示反斜杠本身
     \'  指示单引号
     \"  指示双引号
     注意: 行末的单独一个反斜杠表示字符串在下一行继续，而不是开始一个新的行。
   5.自然字符串
     自然字符串通过给字符串加上前缀r或R来指定，取消转义符的功能。例如: r"Newlines are indicated by \n"。
     三引号的字符串也可以同样用法，如：R'''Newlines are indicated by \n'''
   6.Unicode字符串
     Python允许你处理Unicode文本(超过拉丁文字范围的)——只需要在字符串前加上前缀u或U。
     例如，u"This is a Unicode string.哈哈.."。(Python3.x之后不需要这样了,可以直接写中文;而这样写会报错)
     Python 3.0开始对unicode全面支持，所有的文本(str)都是Unicode的；并引入了一个叫做bytes的新类型来处理字节序列。而编码过的Unicode会以二进制的数据来表示。
     因为在2.x的世界里，大量的bug都是因为已编码的文本和未编码的文本混杂在一起而产生的。
   7.按字面意义级连字符串
     如果你把两个字符串按字面意义相邻放着，他们会被Python自动级连。
     例如，"What's" ' your name?'会被自动转为"What's your name?"。
     即是说，两个字符串放在一起，会有字符拼接的效果。加号“+”也有字符拼接的效果。
   8.字符串拼接
     可以使用“str1.__add__(str2)”或者“str1 + str2”或者直接两个字符串放一起,来拼接字符串
     但字符串与其它类型拼接时，得先把其它类型转成字符串类型，否则会出错。如“str1 + 2”就会出错，需要“str1 + str(2)”
   9.格式化
     使用“%控制符”可以格式化字符串,非常方便。如: str1 = "Swaroop's age is %d, weight is %f" % (5, 65.5)
     “%(name)控制符”可按名称传参数(不写名称是按位置传参数)，如: str = "%(row)d Rows is %(value)s" % { 'value': 'kkkk', 'row': 22 }
     格式化的符号用法参考下面的“字符串格式化控制表”
     另外，string.format()函数也可以格式化字符串
     例如：'subtracting {0}, adding {1}'.format(1, 'haha') # 参数讲对应到“{number}”的位置上
   10.字符串序列(索引和切片)
     字符串可以使用下标来获取字符串中某个项目，以及截取字符串。详情参考“序列”
     用法如: name = 'swaroop'; name[1]; name[1:3]; name[1:-1]
   11.str(anything)函数和 unicode(anything)函数
     Python 2有两个全局函数可以把对象强制转换成字符串:unicode()把对象转换成Unicode字符串，还有 str()把对象转换为非Unicode字符串。
     Python 3只有一种字符串类型，Unicode字符串，所以 str()函数即可完成所有的功能。(unicode()函数在Python 3里不再存在了。)
   另外:
     没有专门的char数据类型，确实没有需要有这个类型。
     单引号和双引号字符串是完全相同的——它们没有在任何方面有不同。
     正则表达式: 一定要用自然字符串处理正则表达式。否则会需要使用很多的反斜杠。
     使用 help(str) 可查看字符串对象定义的所有方法及属性。
     由于百分号有特殊作用，所以字符串里面要用百分号的话需要使用“%%”，如："select * from my_table where name like '%%测试%%'"


字符串格式化控制：(未参考帮助文档，只是个人猜测)
   转义符 (Escape Sequence)：
   \ddd     1到3位8进制数指定Unicode字符输出(如：“\127”显示“W”)
   \uxxxx   1到4位16进制数指定Unicode字符输出(Python3.x开始支持此写法,如: \u54C8 显示“哈”字)
   \xhh     16进制数指定Unicode字符输出(如：“\xe5\x93\x88”显示“哈”)
   \\       \
   \        \ (单独的一个斜杠也显示斜杠,即不后接有转移作用的字符时，作为斜杠使用)
   \'       '
   \"       "
   \a       字符：0x07    响铃(ASCII控制字符)
   \b       字符：0x08    退格(光标向左走一格)(ASCII控制字符)
   \f       字符：0x0c    Formfeed(FF)(走纸转页,换页)(ASCII控制字符)
   \n       字符：0x0a    换行(ASCII控制字符)
   \N{name} Unicode字符   只能针对Unicode
   \r       字符：0x0d    回车
   \t       字符：0x09    跳格(tab符号),水平制表符
   \v       字符：0x0b    垂直制表符

   %%       %
   %d       输出10进制整数，只能是数字类型，输出字符串类型会出错；浮点类型的数字将被取整(直接删除小数部分)。
   %f,%F    以10进制输出浮点数，只能是数字类型，输出字符串类型会出错。
   %e,%E    以科学计数法输出10进制的浮点数，大小写的“e”反应在显示时科学计数法的“e/E”上，只能是数字类型。
   %a       Python3.0开始支持此写法，原样输出结果，字符串类型会加上单引号引起来。
   %o       (字母o)以8进制整数方式输出，只能是数字类型；浮点类型的数字将被取整(直接删除小数部分)。
   %x,%X    将数字以16进制方式输出，只能是数字类型；浮点类型的数字将被取整(直接删除小数部分)。
   %s       将字符串格式化输出(可输出任何类型)
   %c       以字符方式输出，提供的类型必须是 char 或 int 。
   注：布尔类型的 True 或 False,用数字类型输出是 1或0,字符串输出是 True 或 False。

   字符串转换成数字
    float(str)     转换成浮点数,如, float("1e-1") 结果：0.1
    int(str)       转换成整数,如, int("12") 结果：12
    int(str,base)  转换成base进制的整数,如, int("11",2) 转换成2进制的整数,结果：3
    long(str)      转换成长整数,Python3取消此语法,如, long("12L") 结果：12L
    long(str,base) 转换成base进制的长整数,Python3取消此语法,如, long("11L",2) 结果：3L

字符串用例
    name = 'Swaroop' # This is a string object

    # 检查字符串的开头部分
    if name.startswith('Swa'):  # 类似函数如 endswith()
        print('Yes, the string starts with "Swa"')

    # 检查是否包含有此内容
    if 'a' in name:
        print('Yes, it contains the string "a"')

    # 找出给定字符串的位置,找不到则返回-1
    if name.find('war') != -1:
        print('Yes, it contains the string "war"', 's')

    # join()函数把列表拼接起来
    delimiter = '; '
    mylist = ['Brazil', 'Russia', 'India', 'China']
    print(delimiter.join(mylist)) # 打印: Brazil; Russia; India; China

    # 大小写转换
    print("THIS IS TEST".lower())    # 转换成小写,打印：this is test
    print("this is test".upper())    # 转换成大写,打印：THIS IS TEST
    print("This Is Test".swapcase()) # 大小写互换,打印：tHIS iS tEST

    print("  This Is Test  ".strip()) # 去掉前后空格,打印：This Is Test

    # 常用 string 函数
    replace(string,old,new[,maxsplit])
        字符串的替换函数，把字符串中的old替换成new。默认是把string中所有的old值替换成new值，如果给出maxsplit值，还可控制替换的个数，如果maxsplit为1，则只替换第一个old值。
        如： a="11223344";print(string.replace(a,"1","one")) # 打印： oneone2223344
             print(string.replace(a,"1","one",1)) # 打印： one12223344
        b = "dfsdf   dfsdfsd dfsdf  ";print(a.replace(' ', '')) # 打印: dfsdfdfsdfsddfsdf

    capitalize(string)
        该函数可把字符串的首个字符替换成大字。
    如： import string; print(string.capitalize("python")) # 打印： Python

    split(string,sep=None,maxsplit=-1)
        从string字符串中返回一个列表，以sep的值为分界符。
    如： import string; ip="192.168.3.3"; print(string.split(ip,'.')) # 打印： ['192', '168', '3', '3']


控制台输入
    使用 raw_input()函数 或者 input()函数 能够很方便的控从制台读入数据，得到的是字符串。
    Python2.x时,raw_input()和 input()的区别:
        当输入为纯数字时:input()返回的是数值类型，如:int,float; raw_input()返回的是字符串类型
        input()会计算在字符串中的数字表达式，而 raw_input()不会。如输入“57+3”: input()得到整数60,raw_input()得到字符串'57+3'
    注:Python3.0将 raw_input()函数去除了,而用 input() 取代它的功能。另外,input()获取的字符串会包括结尾的换行符。
    例:(此处是Python2.6的写法，3.x时应该把 raw_input() 改成 input())
      1.输入字符串
        nID = raw_input("Input your id plz:\n"); print('your id is %s' % (nID))
      2.输入整数
        nAge = int(raw_input("input your age plz:\n")); print('your age is %d\n' % nAge)
      3.输入浮点型
        fWeight = float(raw_input("input your weight:\n")); print('your weight is %f' % fWeight)
      4.输入16进制数据
        nHex = int(raw_input('input hex value(like 0x20):\n'),16); print('nHex = %x,nOct = %d\n' %(nHex,nHex))
      5.输入8进制数据
        nOct = int(raw_input('input oct value(like 020):\n'),8); print('nOct = %o,nDec = %d\n' % (nOct,nOct))
    注:打印字符串时，“%”作为特殊符号，两个百分号才能打印出一个百分号

    Python 2 与 Python 3 的比较
       Python 2             Python 3
    ① raw_input()          input()          # 最简单的形式，raw_input()被替换成input()。
    ② raw_input('prompt')  input('prompt')  # 可以指定一个提示符作为参数
    ③ input()              eval(input())    # 如果想要请求用户输入一个Python表达式，计算结果
