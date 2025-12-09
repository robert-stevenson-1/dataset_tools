# dataset_tools
Small set of tools I have made to process my dataset of various training needs

place this repo into the root of your dataset that you will be working on

# slicing my dataset with sahi

```sh
sahi coco slice --image_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO --dataset_json_path /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO/result.json --output_dir /root/zfs-crow-compute/datasets/PCN/v2/B1-8-COCO-tiled --slice_size 2048
```

## train-val split

 use `split_coco.py`, but remember to update the paths and filenames inside

# why this exists

I needed tools to help prep my PCN dataset from exporting from Label Studio.
