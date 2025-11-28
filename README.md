# dataset_tools
Small set of tools I have made to process my dataset of various training needs

place this repo into the root of your dataset that you will be working on

# slicing my dataset with sahi

```sh
sahi coco slice --image_dir root/zfs-crow-compute/datasets/PCN/all-bottles/PCN_Dish_B1+2_COCO_unsplit/images --dataset_json_path /root/zfs-crow-compute/datasets/PCN/all-bottles/PCN_Dish_B1+2_COCO_unsplit/annotations.json --out_dir ./tiled_dataset --slice_size 2048
```

# why this exists

I needed tools to help prep my PCN dataset from exporting from Label Studio.
