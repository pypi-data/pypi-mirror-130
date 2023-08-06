from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union, Callable

import firefly as ff
import pandas as pd

from ..data_catalog.table import Table


class Dal(ABC):
    @abstractmethod
    def store(self, data: pd.DataFrame, table: Table, **kwargs):
        pass

    @abstractmethod
    def load(self, table: Table, criteria: Union[Callable, ff.BinaryOp] = None, **kwargs) -> pd.DataFrame:
        pass

    @abstractmethod
    def delete(self, criteria: ff.BinaryOp, table: Table, **kwargs):
        pass

    @abstractmethod
    def get_partitions(self, table: Table, criteria: ff.BinaryOp = None, **kwargs) -> List[str]:
        pass

    @abstractmethod
    def wait_for_tmp_files(self, files: list, **kwargs):
        pass

    @abstractmethod
    def read_tmp_files(self, files: list, **kwargs) -> pd.DataFrame:
        pass

    @abstractmethod
    def write_tmp_file(self, file: str, data: pd.DataFrame, **kwargs):
        pass

    @abstractmethod
    def compact(self, table: Table, path: str, **kwargs):
        pass

    @abstractmethod
    def deduplicate_partition(self, table: Table, path: str, **kwargs):
        pass
