# ============================================================================
# FILE: file.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from pathlib import Path
import typing

from defx.base.source import Base
from defx.context import Context
from defx.util import error
from neovim import Nvim


class Source(Base):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'file'

    def get_root_candidate(self, context: Context, path: str) -> dict:
        return {
            'word': self.vim.call('fnamemodify',
                                  path + ('/' if path != '/' else ''), ':~'),
            'is_directory': True,
            'action__path': Path(path),
        }

    def gather_candidates(self, context: Context, path: str) -> typing.List:
        candidates = []
        directory = Path(path)
        if not directory.is_dir():
            error(self.vim, f'"{directory}" is not directory.')
            return []
        for entry in directory.iterdir():
            candidates.append({
                'word': entry.name + ('/' if entry.is_dir() else ''),
                'is_directory': entry.is_dir(),
                'action__path': entry,
            })
        return candidates
