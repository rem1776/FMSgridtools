from typing import List
import xarray as xr
import numpy as np
import numpy.typing as npt
import dataclasses

# represents topography output file created by make_topog
# contains parameters for topography generation that aren't tied to a specific topography type
# and depth values from specified topog_type algorithm once generated.
# if multiple tiles are used, the third index of depth will be the the tile number
@dataclasses.dataclass
class TopogObj():
    output_name: str = None
    ntiles: int = None
    nx: int = None
    ny: int = None
    x_refine: int = None
    y_refine: int = None
    scale_factor: float = None
    depth: npt.NDArray[np.float64] = None

    ds: xr.Dataset = None
    data_is_generated: bool = None

    # sets up dataset variables
    def __post_init__(self):
        depth_vars = dict()
        depth_attrs = dict()
        depth_attrs["standard_name"] = "topographic depth at T-cell centers"
        depth_attrs["units"] = "meters"
        depth_coords = xr.Coordinates( {'ny': np.empty(self.ny), 'nx': np.empty(self.nx)} )
        # TODO check dims of depth
        # if single tile exclude tile number in variable name
        if (self.ntiles == 1):
            depth_vars["depth"]= xr.DataArray(
                coords=depth_coords,
                dims=["ny", "nx"],
                attrs=depth_attrs,
            )
        # loop through ntiles and add depth_tile<n> variable for each
        else:
            for i in range(1,self.ntiles):
                depthVarName = "depth_tile" + str(i)
                depth_vars[depthVarName] = xr.DataArray(
                    coords=depth_coords,
                    dims=["ny", "nx"],
                    attrs=depth_attrs,
                )
        # create dataset from vars
        self.ds = xr.Dataset(
            data_vars = depth_vars,
        )
        self.ds = self.ds.expand_dims({'ntiles': self.ntiles})
        self.ds = self.ds.drop_vars(['ny', 'nx'])
        self.data_is_generated = False
        # TODO add global attrs

    # just writes out the file
    def write_topog_file(self):
        if(not self.data_is_generated):
            print("Warning: write routine called but depth data not yet generated")
        self.ds.to_netcdf(self.output_name)

    def make_topog_realistic( self, topog_file, topog_field, min_depth,
                              num_filter_pass, flat_bottom, fill_first_row, filter_topog, round_shallow, fill_shallow,
                              deepen_shallow, smooth_topo_allow_deepening, vgrid_file, full_cell,
                              dont_fill_isolated_cells, on_grid, dont_change_landmask, kmt_min, dont_adjust_topo,
                              fraction_full_cell, dont_open_very_this_cell, min_thickness):
        pass

    def make_rectangular_basin(self, bottom_depth):
        pass

    def make_topog_gaussian(self, gauss_scale, gauss_amp, slope_x, slope_y):
        pass

    def make_topog_bowl(self, bottom_depth, min_depth, bowl_south, bowl_north, bowl_west, bowl_east):
        pass

    def make_topog_box_idealized(self, bottom_depth, min_depth):
        pass

    def make_topog_box_channel(self, jwest_south, jwest_north, ieast_south, ieast_north, bottom_depth):
        pass

    def make_topog_dome(dome_slope, dome_bottom, dome_embayment_west, dome_embayment_east, dome_embayment_south,
                        dome_embayment_depth):
        pass
