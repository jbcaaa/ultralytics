import os
import shutil

org = "./runs/train/"
paths = os.listdir(org)
lists = []
for a in paths:
    b = a.split("exp")[1]
    if not b:
        continue
    lists.append(int(b))
maxxxx = max(lists)
maxxxx = 'exp' + str(maxxxx)
ret = os.path.join(org, maxxxx)
try:
    shutil.copy(ret + '/weights/best.pt', '.')
    print("success!!!")
    print(ret)
except:
    print('failed!!!')