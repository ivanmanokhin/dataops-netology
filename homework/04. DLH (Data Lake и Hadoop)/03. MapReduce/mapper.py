import sys

stream = sys.stdin
next(stream) # пропускаем первую строку

for line in stream:
    words = line.strip().split(',')[0].split()
    for word in words:
        print(f'{word},1')
