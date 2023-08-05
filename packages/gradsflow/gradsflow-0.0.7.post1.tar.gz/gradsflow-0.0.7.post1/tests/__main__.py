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

from pathlib import Path

from flash.core.data.utils import download_data

cwd = str(Path.cwd())

download_data("https://pl-flash-data.s3.amazonaws.com/hymenoptera_data.zip", f"{cwd}/data")

download_data(
    "https://github.com/gradsflow/test-data/archive/refs/tags/cat-dog-v0.zip",
    f"{cwd}/data",
)
