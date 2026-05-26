#Challenge1

words = input().split(",")
result = ",".join([w for w in sorted(words)])
print(result)


#Challenge2

def longest_word(sentence):
    words = sentence.split()
    return max(words, key=len)