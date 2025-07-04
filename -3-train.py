from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(model="yolo11m")
    # model.load('best.pt') # 加载预训练权重,改进或者做对比实验时候不建议打开，因为用预训练模型整体精度没有很明显的提升
    model.train(data=r'data.yaml',
                imgsz=512,
                epochs=1000,
                batch=-1,
                device='0',
                optimizer='SGD',
                close_mosaic=10,
                resume=False,
                project='runs/train',
                name='exp',
                single_cls=True,
                cache=False,
                )
