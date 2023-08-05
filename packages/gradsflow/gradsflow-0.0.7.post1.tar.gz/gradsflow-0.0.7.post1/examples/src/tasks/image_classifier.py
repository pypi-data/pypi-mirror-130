#  Copyright (c) 2021 GradsFlow. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

from flash.image import ImageClassificationData

from gradsflow import AutoImageClassifier
from gradsflow.data.image import image_dataset_from_directory

# 1. Create the DataModule
data_dir = os.getcwd() + "/data"
# download_data("https://pl-flash-data.s3.amazonaws.com/hymenoptera_data.zip", data_dir)

datamodule = ImageClassificationData.from_folders(
    train_folder=f"{data_dir}/hymenoptera_data/train/",
    val_folder=f"{data_dir}/hymenoptera_data/val/",
)
image_size = (64, 64)
train_data = image_dataset_from_directory(f"{data_dir}/hymenoptera_data/train/", image_size=image_size, transform=True)

val_data = image_dataset_from_directory(f"{data_dir}/hymenoptera_data/val/", image_size=image_size, transform=True)

num_classes = len(train_data.dataset.classes)

model = AutoImageClassifier(
    train_dataloader=train_data.dataloader,
    val_dataloader=val_data.dataloader,
    num_classes=num_classes,
    max_epochs=1,
    optimization_metric="val_loss",
    max_steps=5,
    n_trials=1,
)
print("AutoImageClassifier initialised!")

model.hp_tune()
