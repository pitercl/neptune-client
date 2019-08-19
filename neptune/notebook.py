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

    def add_checkpoint(self, file_path=None, tag=None, name=None):
        """Uploads new checkpoint of the notebook to Neptune.

        If called without parameters - add checkpoint to notebook from which it is called.

        Args:
            file_path (:obj:`str`, optional, default is ``None``):
                | File path containing notebook contents (.ipynb file).
                  If ``None``, assume that method is called from Notebook.
            tag (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | checkpoint tag like ``'exploration'`` or list of tags like ``['exploration', 'client']``.
            name (:obj:`str`, optional, default is ``None``):
                | If ``None``, checkpoint will be assigned timestamp name,
                | If ``str`` is passed, checkpoint will be assigned this name.

        Example:

            .. code:: python3

                # Create a notebook.
                notebook = project.create_notebook('file.ipynb')

                # Change content in your notebook & save it

                # Upload new checkpoint
                notebook.add_checkpoint('file.ipynb')

                # Upload new checkpoint (call made from notebook cell)
                notebook.add_checkpoint()

                # Upload new checkpoint and name it
                notebook.add_checkpoint('file.ipynb', name='visualizations')
        """
        validate_notebook_path(file_path)

        with open(file_path) as f:
            return self._client.create_checkpoint(self.id, os.path.abspath(file_path), f)

    def get_checkpoints(self, tag=None):
        """List all checkpoints matching the specified criteria.

        Args:
            tag (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | checkpoint tag like ``'exploration'`` or list of tags like
                  ``['exploration', 'client']``. Only checkpoints tagged with all tags in the list
                  will be returned.

        Returns:
            :obj:`list` of :class:`~neptune.checkpoint.Checkpoint` objects.

        Examples:

            .. code:: python3

                # list everything
                notebook.list_checkpoints()

                # list checkpoints with any of two tags.
                notebook.list_checkpoints(tag=['visualizations', 'client-update'])

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
