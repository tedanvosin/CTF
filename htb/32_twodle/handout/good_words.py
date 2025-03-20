valid_words = []
with open('valid_words.txt','r') as file:
    for i in range(12542):
        valid_words.append(file.readline().strip())

good_words=[]
for word in valid_words:
    if len(set(word))!=5:
        continue
    vowels = 'aeiou'
    count = sum(1 for char in word if char in vowels)
    if count == 1:
        good_words.append(word)

print(len(good_words))
