# rptree.py

"""This module provides RP Tree main module."""

import os
import sys
import pathlib
from collections import deque
from typing import Deque

PIPE = "|"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    """Creates the directory tree diagram and displays it on the screen."""

    def __init__(self, root_dir, dir_only="False", output_file=sys.stout):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self) -> None:
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            # Wrap the tree in a markdown code block
            tree.appendleft("```")
            tree.append("```")
            self._output_file = open(
                self._output_file,
                mode="w",
                encoding="UTF-8",
            )
        with self._output_file as stream:
            for entry in tree:
                print(entry, file=stream)


class _TreeGenerator:
    def __init__(self, root_dir, dir_only="False"):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = deque([])

    def build_tree(self) -> Deque:
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self) -> None:
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix="") -> None:
        entries = self._prepare_entries(directory)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry,
                    index,
                    entries_count,
                    prefix,
                    connector,
                )
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(
        self,
        directory,
        index,
        entries_count,
        prefix,
        connector,
    ) -> None:
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector) -> None:
        self._tree.append(f"{prefix}{connector} {file.name}")

    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries
