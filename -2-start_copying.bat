python generate_classes.py
python label_converter.py --task rectangle --src_path .\pre_datasets\labels --dst_path .\pre_datasets\txt_labels --classes .\classes.txt --mode custom2yolo
python split.py
python generate_datayaml.py
