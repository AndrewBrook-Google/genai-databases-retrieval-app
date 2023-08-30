# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
from typing import List

import asyncio

import datastore
import models
from server import parse_config


async def main():
    toys: List[models.Toy] = []
    with open("data/product_dataset.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        toys = [models.Toy.model_validate(line) for line in reader]

    embeddings: List[models.Embedding] = []
    with open("data/product_embeddings_dataset.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        embeddings = [models.Embedding.model_validate(line) for line in reader]

    cfg = parse_config("config.yml")
    ds = await datastore.create(cfg.datastore)
    await ds.initialize_data(toys, embeddings)
    await ds.close()


if __name__ == "__main__":
    asyncio.run(main())
