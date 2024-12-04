import numpy as np
import xarray as xr
from typing import List, Optional
import dataclasses

@dataclasses.dataclass
class GridStruct:
    nx: int
    ny: int
    nxp: int
    nyp: int
    nlon: np.ndarray
    nlat: np.ndarray
    halo: int
    x: np.ndarray
    y: np.ndarray
    dx: np.ndarray
    dy: np.ndarray
    angle_dx: np.ndarray
    angle_dy: np.ndarray
    area: np.ndarray

    @classmethod
    def from_file(cls, file_path: str):
        with xr.open_dataset(file_path) as ds:
            _nx = ds.nx.values.item()
            _ny = ds.ny.values.item()
            _nxp = ds.nxp.values.item()
            _nyp = ds.nyp.values.item()
            _nlon = ds.nlon.values.size
            _nlat = ds.nlat.values.size
            _halo = ds.halo.values.size
            _x = ds.x.values
            _y = ds.y.values
            _dx = ds.dx.values
            _dy = ds.dy.values
            _angle_dx = ds.angle_dx.values
            _angle_dy = ds.angle_dy.values
            _area = ds.area.values
        return cls(
            nx=_nx,
            ny=_ny,
            nxp=_nxp,
            nyp=_nyp,
            nlon=_nlon,
            nlat=_nlat,
            halo=_halo,
            x=_x,
            y=_y,
            dx=_dx,
            dy=_dy,
            angle_dx=_angle_dx,
            angle_dy=_angle_dy,
            area=_area
        )
        