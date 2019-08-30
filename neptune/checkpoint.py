#
# Copyright (c) 2019, Neptune Labs Sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class Checkpoint(object):
    """It contains all the information about checkpoint

        Args:
            _id (:obj:`str`): checkpoint uuid
            _notebook_id (:obj:`str`): uuid of the notebook that this checkpoint belong to
            _name (:obj:`str` or ``None``): checkpoint name
            _description (:obj:`str` or ``None``): checkpoint description
    """
    def __init__(self, _id, _notebook_id, _name, _description, _path):
        self.id = _id
        self.notebook_id = _notebook_id
        self.name = _name
        self.description = _description
        self.path = _path

    def download(self, destination_path):
        """Download this checkpoint (.ipynb file).

        Args:
            destination_path (:obj:`str`): The path where the file will be downloaded.

        Examples:
            Assuming that `checkpoint` is an instance of the :class:`~neptune.checkpoint.Checkpoint`.

            .. code:: python3

                # download latest checkpoint of 'my-notebook'
                checkpoint.download('/home/james/project/my-downloaded-notebook.ipynb')
        """
        pass
