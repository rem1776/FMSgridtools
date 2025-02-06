# unit test for Topog.py functionality

from FMSgridtools import TopogObj
from FMSgridtools import get_provenance_attrs
import numpy as np
import pytest
from pathlib import Path
from os import remove

def test_generate_rectangular_basin():
    out_file = "test_topog_rectangular_basin.nc"
    test_topog = TopogObj(output_name=out_file,
                          ntiles = 1,
                          global_attrs = get_provenance_attrs(),
                          nx = {'tile1': 16},
                          ny = {'tile1': 16},
                          x_refine = 1,
                          y_refine = 1,
                          scale_factor = 1)
    test_topog.make_rectangular_basin(bottom_depth=128)
    test_topog.write_topog_file()

@pytest.mark.skip(reason="TODO")
def test_generate_realistic():
    pass

@pytest.mark.skip(reason="TODO")
def test_generate_gaussian():
    pass

@pytest.mark.skip(reason="TODO")
def test_generate_dome():
    pass

@pytest.mark.skip(reason="TODO")
def test_generate_bowl():
    pass

@pytest.mark.skip(reason="TODO")
def test_generate_idealized():
    pass

@pytest.mark.skip(reason="TODO")
def test_generate_idealized():
    pass
