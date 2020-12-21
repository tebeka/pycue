"""cue is a Python wrapper for https://cuelang.org"""
from subprocess import run
from tempfile import NamedTemporaryFile

__version__ = '0.1.0'


class Error(Exception):
    pass


cue_exe = 'cue'

# File types
GO = 'go'
JSON = 'json'
JSONL = 'jsonl'
PROTO = 'proto'
TEXT = 'text'
YAML = 'yaml'

# File types (cue filetypes)
extension = {
    GO: '.go',
    JSON: '.json',
    JSONL: '.jsonl',
    PROTO: '.proto',
    TEXT: '.txt',
    YAML: '.yml',
}


class vet:
    @staticmethod
    def files(cue_file, data_file):
        """Validate from files"""
        out = run([cue_exe, 'vet', cue_file, data_file], capture_output=True)
        if out.returncode != 0:
            raise Error(out.stderr.decode())

    @staticmethod
    def data(cue_data, data, data_type):
        """Validate from data (str or bytes)"""
        ext = extension.get(data_type)
        if ext is None:
            raise ValueError(f'unknown data type - {data_type!r}')

        with _tmp_file(cue_data, '.cue') as cf, _tmp_file(data, ext) as df:
            vet.files(cf.name, df.name)


def check_install():
    """Validate that the "cue" command line is installed"""
    out = run([cue_exe, 'version'])
    if out.returncode != 0:
        raise Error(f'{cue_exe} not found in PATH')


def _tmp_file(data, ext):
    if isinstance(data, str):
        data = data.encode('utf-8')

    tmp = NamedTemporaryFile(suffix=ext)
    tmp.write(data)
    tmp.flush()
    return tmp
