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

os.environ["GF_CI"] = "true"

from unittest.mock import MagicMock

from gradsflow.tasks import AutoTextClassifier


def test_build_model():
    suggested_conf = dict(
        optimizers=["adam"],
        lr=(5e-4, 1e-3),
    )
    datamodule = MagicMock()
    datamodule.num_classes = 2
    model = AutoTextClassifier(
        datamodule,
        num_classes=datamodule.num_classes,
        suggested_backbones=["sgugger/tiny-distilbert-classification"],
        suggested_conf=suggested_conf,
        max_epochs=1,
        optimization_metric="val_loss",
        timeout=5,
        n_trials=1,
    )

    model_confs = {
        "backbone": model._DEFAULT_BACKBONES[-1],
        "optimizer": "adam",
        "lr": 1e-3,
    }
    model.build_model(model_confs)
