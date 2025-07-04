import os
import shutil
import random
from tqdm import tqdm

def get_corresponding_image_path(label_file_path, source_images_dir, image_extension=".jpg"):
    """
    根据标签文件路径获取对应的图像文件路径。
    例如: label_file_path = 'path/to/labels/file1.txt'
          source_images_dir = 'path/to/images'
          返回 'path/to/images/file1.jpg'
    """
    base_name = os.path.basename(label_file_path)  # "file1.txt"
    image_name_without_ext = os.path.splitext(base_name)[0] # "file1"
    image_name = image_name_without_ext + image_extension
    return os.path.join(source_images_dir, image_name)

def split_dataset(source_images_dir, source_labels_dir, output_base_dir, split_ratios, image_extension=".jpg", label_extension=".txt"):
    """
    将图像和标签数据集分割为训练集、验证集和测试集。

    参数:
    source_images_dir (str): 存放原始图片的目录路径。
    source_labels_dir (str): 存放原始标签文件的目录路径。
    output_base_dir (str): 输出数据集的根目录 (例如 './datasets')。
    split_ratios (list): 包含训练、验证、测试集比例的列表，例如 [0.7, 0.2, 0.1]。
    image_extension (str): 图像文件的扩展名，默认为 ".jpg"。
    label_extension (str): 标签文件的扩展名，默认为 ".txt"。
    """

    # 定义输出目录结构
    train_img_dir = os.path.join(output_base_dir, 'images', 'train')
    val_img_dir = os.path.join(output_base_dir, 'images', 'val')
    test_img_dir = os.path.join(output_base_dir, 'images', 'test')

    train_label_dir = os.path.join(output_base_dir, 'labels', 'train')
    val_label_dir = os.path.join(output_base_dir, 'labels', 'val')
    test_label_dir = os.path.join(output_base_dir, 'labels', 'test')

    # 创建输出目录 (如果不存在)
    for dir_path in [train_img_dir, val_img_dir, test_img_dir, train_label_dir, val_label_dir, test_label_dir]:
        os.makedirs(dir_path, exist_ok=True) # exist_ok=True 避免已存在时报错

    # 获取所有标签文件名 (不含路径，不含扩展名)
    # 我们以标签文件为基准，因为通常标签是手动创建的，图片是对应的
    label_files_names_only = [
        os.path.splitext(f)[0]
        for f in os.listdir(source_labels_dir)
        if f.endswith(label_extension)
    ]

    valid_file_pairs = []
    print(f"Scanning files in {source_labels_dir} and {source_images_dir}...")
    for name_only in tqdm(label_files_names_only, desc="Checking file pairs"):
        label_file = name_only + label_extension
        image_file = name_only + image_extension

        source_label_path = os.path.join(source_labels_dir, label_file)
        source_image_path = os.path.join(source_images_dir, image_file)

        if os.path.exists(source_label_path) and os.path.exists(source_image_path):
            valid_file_pairs.append((source_image_path, source_label_path))
        else:
            if not os.path.exists(source_image_path):
                print(f"Warning: Image file not found for label '{label_file}': {source_image_path}")
            if not os.path.exists(source_label_path): # Should not happen if listing from source_labels_dir
                print(f"Warning: Label file not found (this shouldn't happen): {source_label_path}")

    if not valid_file_pairs:
        print("Error: No valid image-label pairs found. Check your source directories and file names.")
        return

    print(f"Found {len(valid_file_pairs)} valid image-label pairs.")
    random.shuffle(valid_file_pairs)

    total_files = len(valid_file_pairs)
    train_split_idx = int(split_ratios[0] * total_files)
    val_split_idx = train_split_idx + int(split_ratios[1] * total_files)

    train_files = valid_file_pairs[:train_split_idx]
    val_files = valid_file_pairs[train_split_idx:val_split_idx]
    test_files = valid_file_pairs[val_split_idx:]

    def copy_files(file_list, dest_img_dir, dest_label_dir, set_name):
        print(f"\nCopying {set_name} files...")
        for img_src, label_src in tqdm(file_list, desc=f'Copying {set_name}', ncols=80, unit='pair'):
            try:
                shutil.move(img_src, os.path.join(dest_img_dir, os.path.basename(img_src)))
                shutil.move(label_src, os.path.join(dest_label_dir, os.path.basename(label_src)))
            except FileNotFoundError as e:
                print(f"Error copying file: {e}. Source image: {img_src}, Source label: {label_src}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    copy_files(train_files, train_img_dir, train_label_dir, 'train')
    copy_files(val_files, val_img_dir, val_label_dir, 'val')
    copy_files(test_files, test_img_dir, test_label_dir, 'test')

    print("\nDataset splitting complete.")
    print(f"Train: {len(train_files)} pairs")
    print(f"Validation: {len(val_files)} pairs")
    print(f"Test: {len(test_files)} pairs")


def main():
    # --- 配置参数 ---
    # 原始数据集路径
    source_images_folder = r'./pre_datasets/images'    # 存放图片的文件夹
    source_labels_folder = r'./pre_datasets/txt_labels' # 存放 YOLO txt 标签的文件夹

    # 输出数据集的根目录
    output_dataset_folder = r'./datasets'

    # 数据集划分比例 [train, val, test]
    # 例如: 70% 训练, 20% 验证, 10% 测试
    split_proportions = [0.7, 0.2, 0.1]

    # 文件扩展名 (如果你的图片不是 .jpg 或标签不是 .txt，请修改)
    img_ext = ".png"
    lbl_ext = ".txt"
    # --- 配置结束 ---

    # 确保源目录存在
    if not os.path.isdir(source_images_folder):
        print(f"Error: Source images folder not found: {source_images_folder}")
        return
    if not os.path.isdir(source_labels_folder):
        print(f"Error: Source labels folder not found: {source_labels_folder}")
        return

    split_dataset(source_images_folder, source_labels_folder, output_dataset_folder,
                  split_proportions, image_extension=img_ext, label_extension=lbl_ext)

if __name__ == '__main__':
    main()
