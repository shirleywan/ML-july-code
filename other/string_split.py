from textwrap import wrap
a = 'urivthvtlqqerctlxmjvkgvfclaaduwmaadedpadanl'
a='123456'
b = 'batkqdhjnrwtsmzidswdnenqpsblsszldyttytrgenaizwehntqiaaufble'
print '\n'.join(wrap('0'*(4-len(a)%4)+a, 4))
# print '\n'.join(wrap(b+'0'*(4-len(b)%4), 4))
