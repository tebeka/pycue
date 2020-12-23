from pathlib import Path

import pytest
import yaml

import cue

here = Path(__file__).absolute().parent
ok_data_file = here / 'data_ok.yml'
with ok_data_file.open() as fp:
    ok_data = fp.read()
bad_data_file = here / 'data_bad.yml'
with bad_data_file.open() as fp:
    bad_data = fp.read()
cue_file = here / 'schema.cue'
with cue_file.open() as fp:
    cue_data = fp.read()


def test_files_fail():
    with pytest.raises(cue.Error):
        cue.vet.files(cue_file, bad_data_file)


def test_files_ok():
    cue.vet.files(cue_file, ok_data_file)


def test_data_str_fail():
    with pytest.raises(cue.Error):
        cue.vet.data(cue_data, bad_data, cue.YAML)


def test_data_bytes_fail():
    schema, data = cue_data.encode('utf-8'), bad_data.encode('utf-8')
    with pytest.raises(cue.Error):
        cue.vet.data(schema, data, cue.YAML)


def test_data_str_ok():
    cue.vet.data(cue_data, ok_data, cue.YAML)


def test_data_bytes_ok():
    schema, data = cue_data.encode('utf-8'), ok_data.encode('utf-8')
    cue.vet.data(schema, data, cue.YAML)


def test_validator_ok():
    v = cue.Validator(cue_data)
    obj = yaml.safe_load(ok_data)
    v.validate(obj)


def test_validator_fail():
    v = cue.Validator(cue_data)
    obj = yaml.safe_load(bad_data)
    with pytest.raises(cue.Error):
        v.validate(obj)
