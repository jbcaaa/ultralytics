import os

pre_images = r"pre_datasets\images"
pre_labels = r'pre_datasets\txt_labels'
images = os.listdir(pre_images)
labels = os.listdir(pre_labels)
for i in range(len(images)):
    images[i] = images[i].strip().split('.jpg')[0]
for i in range(len(labels)):
    labels[i] = labels[i].strip().split('.txt')[0]
for image in images:
    if image not in labels:
        os.remove(os.path.join(pre_images,image+'.jpg'))
        print("o~kk")
