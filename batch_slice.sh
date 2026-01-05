# !/bin/bash

sahi coco slice --image_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO --dataset_json_path /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO/annotations_4200K.json --output_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO-4200K-tiled --slice_size 640
sahi coco slice --image_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO --dataset_json_path /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO/annotations_4800K.json --output_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO-4800K-tiled --slice_size 640
sahi coco slice --image_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO --dataset_json_path /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO/annotations_5300K.json --output_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO-5300K-tiled --slice_size 640