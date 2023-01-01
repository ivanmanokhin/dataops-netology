import sys

stream = sys.stdin
previous_word = None
count = 0

for line in stream:
    word, cost = line.strip().split(',')
    cost = int(cost)

    if previous_word:
        if previous_word == word:
            count += cost
        else:
            print(previous_word, count)
            previous_word = word
            count = cost
    else:
        previous_word = word
        count = cost

print(previous_word, count)
