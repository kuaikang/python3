递归的两个特点：调用自身,结束条件

时间复杂度：用来估计算法运行时间的一个式子(单位)
常见复杂度排序：
    O(1) < O(logn) < O(n) < O(nlogn) < O(n的平方) < O(n的平方 logn) < O(n的三次方)
1.print("HelloWorld")   O(1)
2.print("HelloWorld")   O(1)
  print("HelloWorld")
2.for i in range(n):    O(n的平方)
      for j in range(n):
          print("HelloWorld")
3.for i in range(n):    O(n的平方)
      print("HelloWorld")
          for j in range(n):
              print("HelloWorld")
4.while n > 1:          O(log₂n)或O(logn) 一般写后面这个
      print(n)
      n = n // 2

空间复杂度：算法占用内存看空间的的大小