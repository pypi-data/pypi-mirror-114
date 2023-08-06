def main():
  start = 60
  while start > 1:
    str = 'x'
    str = str.rjust(start - 2, ' ')
    str = str + ' ?'
    print(str)
    start = int(start / 2)
  print('!')
