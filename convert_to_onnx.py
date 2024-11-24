from ultralytics import YOLO

model = YOLO("best.pt")

model.export(format='onnx')

with open('classes.txt', 'r', encoding='utf-8') as f:
    classes = f.readlines()
new_classes = []
for a in classes:
    new_classes.append('  - '+a)
with open('model.yaml', 'a+', encoding='utf-8') as f:
    f.truncate(0)
    f.write(f'''type: yolov8
name: yolov5s-r20230520
display_name: YOLOv5s Ultralytics
model_path: best.onnx
input_width: 1280
input_height: 1280
stride: 32
nms_threshold: 0.45
confidence_threshold: 0.45
classes:\n''')
    f.writelines(new_classes)