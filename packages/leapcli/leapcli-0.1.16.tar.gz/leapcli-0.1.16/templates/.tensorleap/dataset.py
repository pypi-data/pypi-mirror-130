from typing import Union, List
import math
import numpy as np

from leapcli.dataset.contract import DatasetInputType, DatasetOutputType, DatasetMetadataType
from leapcli.dataset.datasetbinder import SubsetResponse, DatasetBinder

crop_size = 128
leap = DatasetBinder()


def subset_func() -> List[SubsetResponse]:
    base_path = 'ISBICellSegmentation/'
    filename = f'{base_path}train-volume2.npy'
    train_path = storage.download(filename, filename)
    scans = np.load(train_path) / 255
    filename = f'{base_path}train-labels2.npy'
    train_path = storage.download(filename, filename)
    masks = np.load(train_path) / 255
    image_size = scans.shape[-1]

    val_split = int(len(scans) * 0.8)
    train_scans = scans[:val_split]
    val_scans = scans[val_split:]
    train_masks = masks[:val_split]
    val_masks = masks[val_split:]

    crop_per_image = int(image_size / crop_size) ** 2
    train_length = crop_per_image * len(train_scans)
    val_length = crop_per_image * len(val_scans)
    crop_per_image = int(image_size / crop_size) ** 2

    train = SubsetResponse(length=train_length, data={'images': train_scans, 'masks': train_masks,
                                                      'shape': image_size, 'crop_per_image': crop_per_image})
    val = SubsetResponse(length=val_length, data={'images': val_scans, 'masks': val_masks, 'shape': image_size,
                                                  'crop_per_image': crop_per_image})
    response = [train, val]
    return response


def input_encoder_1(idx: int, subset: SubsetResponse) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['images'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]

    return crop[..., np.newaxis]


def output_encoder_1(idx: int, subset: Union[SubsetResponse, list]) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['masks'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]

    return crop[..., np.newaxis]


def metadata_encoder_1(idx: int, subset: Union[SubsetResponse, list]) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['masks'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]
    return float(np.mean(crop))


def metadata_encoder_2(idx: int, subset: Union[SubsetResponse, list]) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['masks'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]
    return float(np.std(crop))


leap.set_subset(ration=1, function=subset_func, name='MicroscopeCellImages')

leap.set_input(function=input_encoder_1, subset='MicroscopeCellImages', input_type=DatasetInputType.Image, name='Crops')

leap.set_ground_truth(function=output_encoder_1, subset='MicroscopeCellImages',
                      ground_truth_type=DatasetOutputType.Mask,
                      name='segments', labels=['Background', 'Cell'], masked_input='Crops')

leap.set_metadata(function=metadata_encoder_1, subset='MicroscopeCellImages', metadata_type=DatasetMetadataType.float,
                  name='label_mean')
leap.set_metadata(function=metadata_encoder_2, subset='MicroscopeCellImages', metadata_type=DatasetMetadataType.float,
                  name='laebl_std')
