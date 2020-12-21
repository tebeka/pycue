import pytest
from pathlib import Path

import cue

here = Path(__file__).absolute().parent
ok_data_file = here / 'data_ok.yml'
bad_data_file = here / 'data_bad.yml'
cue_file = here / 'schema.cue'


def test_files_fail():
    with pytest.raises(cue.Error):
        cue.vet.files(cue_file, bad_data_file)


def test_files_ok():
    cue.vet.files(cue_file, ok_data_file)


def test_data_str_fail():
    with bad_data_file.open() as fp:
        data = fp.read()

    with cue_file.open() as fp:
        cue_data = fp.read()

    with pytest.raises(cue.Error):
        cue.vet.data(cue_data, data, cue.YAML)


def test_data_bytes_fail():
    with bad_data_file.open('rb') as fp:
        data = fp.read()

    with cue_file.open('rb') as fp:
        cue_data = fp.read()

    with pytest.raises(cue.Error):
        cue.vet.data(cue_data, data, cue.YAML)


def test_data_str_ok():
    with ok_data_file.open() as fp:
        data = fp.read()

    with cue_file.open() as fp:
        cue_data = fp.read()

    cue.vet.data(cue_data, data, cue.YAML)


def test_data_bytes_ok():
    with ok_data_file.open('rb') as fp:
        data = fp.read()

    with cue_file.open('rb') as fp:
        cue_data = fp.read()

    cue.vet.data(cue_data, data, cue.YAML)
