import sys

classes = './classes.txt'
datayaml = './data.yaml'

with open(classes, 'r', encoding='utf-8') as f:
    classes = f.readlines()

new_classes = []
for a in classes:
    new_classes.append(a.strip())

with open(datayaml, 'a+', encoding='utf-8') as f:
    f.truncate(0)
    f.write(f'''train: ./datasets/images/train
val: ./datasets/images/val
test: ./datasets/images/test

nc: {len(new_classes)}
names: {new_classes}
''')