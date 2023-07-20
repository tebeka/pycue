"""cue is a Python wrapper for https://cuelang.org"""
from os import environ
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import IO, Any

import yaml

__version__ = '0.1.2'


class Error(Exception):
    pass


cue_exe = environ.get('CUE_EXE', 'cue')

# File types
GO = 'go'
JSON = 'json'
JSONL = 'jsonl'
PROTO = 'proto'
TEXT = 'text'
YAML = 'yaml'

# File types (cue filetypes)
extension: dict[str, str] = {
    GO: '.go',
    JSON: '.json',
    JSONL: '.jsonl',
    PROTO: '.proto',
    TEXT: '.txt',
    YAML: '.yml',
}


class vet:
    @staticmethod
    def files(cue_file: str, data_file: str) -> None:
        """Validate from files"""
        out = run([cue_exe, 'vet', cue_file, data_file], capture_output=True)
        if out.returncode != 0:
            raise Error(out.stderr.decode())

    @staticmethod
    def data(cue_data: str | bytes, data: str | bytes, data_type: str) -> None:
        """Validate from data (str or bytes)"""
        ext = extension.get(data_type)
        if ext is None:
            raise ValueError(f'unknown data type - {data_type!r}')

        with _tmp_file(cue_data, '.cue') as cf, _tmp_file(data, ext) as df:
            vet.files(cf.name, df.name)


class Validator:
    def __init__(self, schema: bytes | str):
        self.schema = schema

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, 'rb') as fp:
            schema = fp.read()
        return cls(schema)

    def validate(self, obj: Any) -> None:
        data = yaml.safe_dump(obj)
        vet.data(self.schema, data, YAML)


def check_install() -> None:
    """Validate that the "cue" command line is installed"""
    out = run([cue_exe, 'version'])
    if out.returncode != 0:
        raise Error(f'{cue_exe} not found in PATH')


def _tmp_file(data: str | bytes, ext: str) -> IO:
    if isinstance(data, str):
        data = data.encode('utf-8')

    tmp = NamedTemporaryFile(suffix=ext)
    tmp.write(data)
    tmp.flush()
    return tmp
