# coding=utf-8
d = {"field":"name"}

field = d['field']  if 'field' in d else '*'
print(field)
