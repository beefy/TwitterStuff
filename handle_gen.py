
import random
import string

username = ''
for i in range(12):
    choice = random.choice(string.letters + str(range(1, 10)) + '_')
    forbidden = [',',' ',']','[']
    if not choice in forbidden:
        username += choice
    else:
        i -= 1

print ''.join(username)

