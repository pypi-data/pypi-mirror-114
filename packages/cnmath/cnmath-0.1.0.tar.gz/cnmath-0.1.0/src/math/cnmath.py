#判断质数
def zhishu(n):
    for x in range(2,n-1):
        if n%x == 0:
            return False
    return True
def shuangshu(n):
    if n%2 == 0:
        return True
    else:
        return False
def pingfang(n):
    return n*n
def jitutonglong(n,m):
    flag = [0,0]
    for x in range(n):
        if 2*x+4*(n-x) == m:
            flag[0] = x
            flag[1] = n-x
            return flag
    return "不可能出现的情况"

