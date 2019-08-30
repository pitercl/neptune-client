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

import os

from neptune.utils import validate_notebook_path


class Notebook(object):
    """It contains all the information about a Neptune Notebook

        Args:
            client (:class:`~neptune.client.Client`): Client object
            project (:class:`~neptune.projects.Project`): Project object
            _id (:obj:`str`): Notebook uuid
            owner (:obj:`str`): Creator of the notebook is the Notebook owner

        Examples:
            .. code:: python3

                # Create a notebook in Neptune.
                notebook = project.create_notebook('data_exploration.ipynb')

    """
    def __init__(self, client, project, _id, owner):
        self._client = client
        self._project = project
        self._id = _id
        self._owner = owner

    @property
    def id(self):
        return self._id

    @property
    def owner(self):
        return self._owner

    def add_checkpoint(self, file_path=None, name=None, description=None):
        """Upload new checkpoint to the notebook in Neptune.

        Args:
            file_path (:obj:`str`, optional, default is ``None``):
                | File path containing notebook contents (.ipynb file).
                  If ``None``, assume that method is called from Notebook.
            name (:obj:`str`, optional, default is ``None``):
                | If ``None``, checkpoint will be assigned timestamp as name,
                | If ``str`` is passed, checkpoint will be assigned this name.
            description (:obj:`str`, optional, default is ``None``):
                | description of the checkpoint.

        Example:
            Assuming that `notebooks` is instance of the :class:`~neptune.notebooks.Notebook`.

            .. code:: python3

                # Create a notebook.
                notebook = project.create_notebook('file.ipynb')

                # Change content in your notebook & save it

                # Upload new checkpoint
                notebook.add_checkpoint('file.ipynb')

                # Upload new checkpoint and name it
                notebook.add_checkpoint('file.ipynb', name='visualizations')
        """
        validate_notebook_path(file_path)

        with open(file_path) as f:
            return self._client.create_checkpoint(self.id, os.path.abspath(file_path), f)

    def get_checkpoints(self, checkpoint_id=None):
        """List all checkpoints matching the specified criteria.

        Args:
            checkpoint_id (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | checkpoint id like ``'b4e67856-998b-48ac-a328-1ee13568daec'`` or list of checkpoint ids like
                  ``['4207f877-7a01-4dcb-a149-5a1ae340c9c5', '1e448d21-4aea-4f1c-a953-7b0647930769']``.
                | If ``None`` - all checkpoints are matching.

        Returns:
            :obj:`list` of :class:`~neptune.notebooks.Checkpoint` objects.
            They are sorted by created date in descending order (latest first).

        Examples:
            Assuming that `notebooks` is instance of the :class:`~neptune.notebooks.Notebook`.

            .. code:: python3

                # get all checkpoints
                notebook.get_checkpoints()

                # get checkpoints by providing their ids
                notebook.get_checkpoints(checkpoint_id=['4207f877-7a01-4dcb-a149-5a1ae340c9c5',
                                                        '1e448d21-4aea-4f1c-a953-7b0647930769'])

        """
        pass

    def get_path(self):
        """Returns the path used to upload the current checkpoint of this notebook

        Returns:
            :obj:`str`: path of the current checkpoint
        """
        return self._client.get_last_checkpoint(self._project, self._id).path

    def get_name(self):
        """Returns the name used to upload the current checkpoint of this notebook

        Returns:
            :obj:`str`: the name of current checkpoint
        """
        return self._client.get_last_checkpoint(self._project, self._id).name


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
            Assuming that `checkpoint` is an instance of the :class:`~neptune.notebooks.Checkpoint`.

            .. code:: python3

                # download latest checkpoint of 'my-notebook'
                checkpoint.download('/home/james/project/my-downloaded-notebook.ipynb')
        """
        pass
