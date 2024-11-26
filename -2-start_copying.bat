python generate_classes.py
cd X-Anylabeling
python tools\label_converter.py --task rectangle --src_path ..\pre_datasets\labels --dst_path ..\pre_datasets\txt_labels --classes ..\classes.txt --mode custom2yolo
cd ..
python split.py
python generate_datayaml.py
