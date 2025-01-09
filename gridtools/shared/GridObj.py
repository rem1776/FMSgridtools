import numpy as np
import numpy.typing as npt
import xarray as xr
from typing import List, Optional, Type
import dataclasses

@dataclasses.dataclass
class GridObj():
    tile: str = None
    geometry: str = None
    north_pole: str = None
    projection: str = None
    discretization: str = None
    conformal: bool = None
    x: npt.NDArray[np.float64] = None
    y: npt.NDArray[np.float64] = None
    dx: npt.NDArray[np.float64] = None
    dy: npt.NDArray[np.float64] = None
    area: npt.NDArray[np.float64] = None
    angle_dx: npt.NDArray[np.float64] = None
    angle_dy: npt.NDArray[np.float64] = None
    arcx: str = None

    @classmethod
    def from_file(cls, file_path: str) -> "GridObj":
        with xr.open_dataset(file_path) as ds:
            return cls(
                tile = ds.tile.values.item(),
                geometry = ds.tile.attrs["geometry"],
                north_pole = ds.tile.attrs["north_pole"],
                projection = ds.tile.attrs["projection"],
                discretization = ds.tile.attrs["discretization"],
                conformal = ds.tile.attrs["conformal"],
                x = ds.x.values,
                y = ds.y.values,
                dx = ds.dx.values,
                dy = ds.dy.values,
                area = ds.area.values,
                angle_dx = ds.angle_dx.values,
                angle_dy = ds.angle_dy.values,
                arcx = ds.arcx.values.item(),
            )
        
    def write_out_grid(self, file_path: str):
        if self.tile is not None:
            tile = xr.DataArray(
            [self.tile],
            attrs=dict(
                standard_name="grid_tile_spec",
                geometry=self.geometry,
                north_pole=self.north_pole,
                projection=self.projection,
                discretization=self.discretization,
                conformal=self.conformal,
            )
        )
        else:
            tile = None
        if self.x is not None:
            x = xr.DataArray(
            data=self.x,
            dims=["nyp", "nxp"],
            attrs=dict(
                standard_name="geographic_longitude",
                units="degree_east",
                _FillValue=False,
            )
        )
        else:
            x = None
        if self.y is not None:
            y = xr.DataArray(
            data=self.y,
            dims=["nyp", "nxp"],
            attrs=dict(
                standard_name="geographic_latitude",
                units="degree_north",
                _FillValue=False,
            )
        )
        else:
            y = None
        if self.dx is not None:
            dx = xr.DataArray(
            data=self.dx,
            dims=["nyp", "nx"],
            attrs=dict(
                standard_name="grid_edge_x_distance",
                units="meters",
                _FillValue=False,
            )
        )
        else:
            dx = None
        if self.dy is not None:
            dy = xr.DataArray(
            data=self.dy,
            dims=["ny", "nxp"],
            attrs=dict(
                standard_name="grid_edge_y_distance",
                units="meters",
                _FillValue=False,
            )
        )
        else:
            dy = None
        if self.area is not None:
            area = xr.DataArray(
            data=self.area,
            dims=["ny", "nx"],
            attrs=dict(
                standard_name="grid_cell_area",
                units="m2",
                _FillValue=False,
            )
        )
        else:
            area = None
        if self.angle_dx is not None:
            angle_dx = xr.DataArray(
            data=self.angle_dx,
            dims=["nyp", "nxp"],
            attrs=dict(
                standard_name="grid_vertex_x_angle_WRT_geographic_east",
                units="degrees_east",
                _FillValue=False,
            )
        )
        else:
            angle_dx = None
        if self.angle_dy is not None:
            angle_dy = xr.DataArray(
            data=self.angle_dy,
            dims=["nyp", "nxp"],
            attrs=dict(
                standard_name="grid_vertex_y_angle_WRT_geographic_north",
                units="degrees_north",
                _FillValue=False,
            )
        )
        else:
            angle_dy = None
        if self.arcx is not None:
            arcx = xr.DataArray(
            [self.arcx],
            attrs=dict(
                standard_name="grid_edge_x_arc_type",
                north_pole="0.0 90.0",
                _FillValue=False,
            )
        )
        else:
            arcx = None

        out = xr.Dataset(
            data_vars={
                "tile": tile,
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "area": area,
                "angle_dx": angle_dx,
                "angle_dy": angle_dy,
                "arcx": arcx,
            }
        )
        out.to_netcdf(file_path)
    
    #TODO: I/O method for passing to the host