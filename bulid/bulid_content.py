#!/usr/bin/python3
import leancloud
import time

leancloud.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")

Chat = leancloud.Object.extend('talk')
# todo = Chat.create_without_data('')

todo = Chat()
s = []
size = 100
for i in range(size):
    s.append('')
todo.set('contents', s)
todo.set('size', size)
todo.set('point', 0)
todo.set('times', 0)
todo.save()
