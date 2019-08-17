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

    def list_tags(self, notebook_name=None, owner=None):
        """List tags in notebooks.

        Args:
            notebook_name (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | notebook name like ``'my-notebook'`` or list of notebook names like
                  ``['my-notebook', 'model-training', 'visualizations']``.
            owner (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | owner (username) of the notebook like ``'james'`` or list of usernames like
                  ``[james', 'andrey']``.

        Returns:
            :obj:`list` of :obj:`str` - list of tags or empty list if no tags.
        """
        pass

    def list_checkpoints(self, notebook_name=None, tag=None, owner=None):
        """List all checkpoints matching the specified criteria.

        All parameters are optional, each of them specifies a single criterion.
        Only checkpoints matching all of the criteria will be returned.

        If a specific criterion accepts a :obj:`list` (like ``tag``),
        then matching with any element of the list is sufficient to pass criterion.

        Args:
            notebook_name (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | notebook name like ``'my-notebook'`` or list of notebook names like
                  ``['my-notebook', 'model-training', 'visualizations']``.
            tag (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | checkpoint tag like ``'exploration'`` or list of tags like
                  ``['exploration', 'client']``.
            owner (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | owner (username) of the notebook like ``'james'`` or list of usernames like
                  ``[james', 'andrey']``.

        Returns:
            :obj:`pandas.DataFrame` with columns `owner`, `notebook name`, `checkpoint`, `checkpoint timestamp`, `tags`.

        Examples:

            .. code:: python3

                # list everything
                notebook.list_checkpoints()

                # list checkpoints with any of two tags.
                notebook.list_checkpoints(tag=['visualizations', 'client-update'])

        """
        pass

    def download_checkpoint(self, destination_dir, notebook_name, checkpoint=None, tag=None, owner=None):
        """Download single checkpoint (.ipynb files) matching the specified criteria.

        | If multiple checkpoints match specified criteria, then most recent one will be downloaded.
        | Downloaded `.ipynb` file has name: **<checkpoint>.ipynb**.
        | If no checkpoint satisfies the criteria, warning is printed to `stdout`.

        Args:
            destination_dir (:obj:`str`): The directory where the file will be downloaded.
            notebook_name (:obj:`str`): notebook name like ``'my-notebook'``.
            checkpoint (:obj:`str`, optional, default is ``None``): checkpoint name like ``'new-visualizations'``.
            tag (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | checkpoint tag like ``'exploration'`` or list of tags like ``['exploration', 'client-update']``.
                | If list is passed, checkpoint must have all tags to match with the criterion.
            owner (:obj:`str`, optional, default is ``None``): owner (username) of the notebook like ``'james'``.

        Examples:

            .. code:: python3

                # download latest checkpoint of 'my-notebook'
                notebook.download_checkpoint('/home/james/project/', 'my-notebook')

                # download specific checkpoint of 'my-notebook'
                notebook.download_checkpoint('/home/james/project/', 'my-notebook',
                                             checkpoint='new-visualizations')

        Note:
            Neptune allows you to have multiple notebooks and checkpoints with the same name.
            Keep that in mind when you are selecting criteria.
        """
        pass

    def remove_checkpoint(self, notebook_name, checkpoint, tag=None, owner=None):
        """Removes checkpoint from Neptune.

        | If checkpoint does not exist, method's invoke has no effect.
        | If multiple checkpoints match specified criteria, then warning is printed to stdout. No checkpoint is removed.

        Args:
            notebook_name (:obj:`str` ): notebook name like ``'my-notebook'``.
            checkpoint (:obj:`str`): checkpoint name like ``'new-visualizations'``.
            tag (:obj:`str` or :obj:`list` of :obj:`str`, optional, default is ``None``):
                | checkpoint tag like ``'exploration'`` or list of tags like ``['exploration', 'client-update']``.
                | If list is passed, checkpoint must have all tags to match with the criterion.
            owner (:obj:`str`, optional, default is ``None``): owner (username) of the notebook like ``'james'``.
        """
        pass
