import os, shutil, random
from tqdm import tqdm


def split_img(img_path, label_path, split_list):
    Data = './datasets'
    train_img_dir = Data + '/labels/train'
    val_img_dir = Data + '/labels/val'
    test_img_dir = Data + '/labels/test'

    train_label_dir = Data + '/images/train'
    val_label_dir = Data + '/images/val'
    test_label_dir = Data + '/images/test'

    try:
        os.makedirs(train_img_dir)
        os.makedirs(train_label_dir)
        os.makedirs(val_img_dir)
        os.makedirs(val_label_dir)
        os.makedirs(test_img_dir)
        os.makedirs(test_label_dir)
    except:
        print()

    exist_files = get_file(Data+'/images/')
    print(exist_files)
    train, val, test = split_list
    all_img = os.listdir(label_path)
    tmp = []
    for a in range(len(all_img)):
        j = all_img[a].split('\\')[-1].strip()
        if j not in exist_files:
            tmp.append(j)
    all_img = tmp
    all_img_path = [os.path.join(label_path, img) for img in all_img]
    # all_label = os.listdir(label_path)
    # all_label_path = [os.path.join(label_path, label) for label in all_label]
    train_img = random.sample(all_img_path, int(train * len(all_img_path)))
    train_img_copy = [os.path.join(train_img_dir, img.split('\\')[-1]) for img in train_img]
    train_label = [toLabelPath(img, img_path) for img in train_img]
    train_label_copy = [os.path.join(train_label_dir, label.split('\\')[-1]) for label in train_label]
    for i in tqdm(range(len(train_img)), desc='train ', ncols=80, unit='img'):
        _copy(train_img[i], train_img_dir)
        _copy(train_label[i], train_label_dir)
        all_img_path.remove(train_img[i])
    val_img = random.sample(all_img_path, int(val / (val + test) * len(all_img_path)))
    val_label = [toLabelPath(img, img_path) for img in val_img]
    for i in tqdm(range(len(val_img)), desc='val ', ncols=80, unit='img'):
        _copy(val_img[i], val_img_dir)
        _copy(val_label[i], val_label_dir)
        all_img_path.remove(val_img[i])
    test_img = all_img_path
    test_label = [toLabelPath(img, img_path) for img in test_img]
    for i in tqdm(range(len(test_img)), desc='test ', ncols=80, unit='img'):
        _copy(test_img[i], test_img_dir)
        _copy(test_label[i], test_label_dir)


def _copy(from_path, to_path):
    try:
        shutil.copy(from_path, to_path)
    except FileNotFoundError:
        print("文件妹有！")


def toLabelPath(img_path, label_path):
    img = img_path.split('\\')[-1]
    label = img.split('.txt')[0] + '.jpg'
    return os.path.join(label_path, label)


def get_file(root_path):
    ret = []
    for dir_name in os.listdir(root_path):
        # 获取目录或文件的路径
        file_path = os.path.join(root_path, dir_name)
        # 判断路径为文件还是路径
        if os.path.isdir(file_path):
            # print(file_path)
            ret += get_file(file_path)
        else:
            ret.append(dir_name.split('\\')[-1].strip().split(".jpg")[0]+'.txt')
    return ret

def main():
    img_path = r'./pre_datasets/images'
    label_path = r'./pre_datasets/txt_labels'
    split_list = [0.7, 0.2, 0.1]  # 数据集划分比例[train:val:test]
    split_img(img_path, label_path, split_list)

if __name__ == '__main__':
    main()
