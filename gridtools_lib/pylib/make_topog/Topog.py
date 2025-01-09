from typing import List
import xarray
import numpy as np
import numpy.typing as npt
import dataclasses

# holds data to write to make_topog output file (ie. 'depth' variable values)
# Also handles writing out the output file.
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

    def write_topog_file(self): 
        print("ntiles from obj: " + str(self.ntiles))

        depth_vars = dict()
        depth_attrs = dict()
        depth_attrs["standard_name"] = "topographic depth at T-cell centers"
        depth_attrs["units"] = "meters"

        # if single tile exclude tile number in variable name
        if (self.ntiles == 1):
            depth_vars["depth"]= xarray.DataArray(
                data=self.depth,
                dims=["ny", "nx"],
                attrs=depth_attrs,
            )
        # loop through ntiles and add depth_tile<n> variable for each
        else:
            for i in range(1,self.ntiles):
                depthVarName = "depth_tile" + str(i)
                depth_vars[depthVarName] = xarray.DataArray(
                    data=self.depth[:,:,i-1],
                    dims=["ny", "nx"],
                    attrs=depth_attrs,
                )
    
        # create dataset from vars
        ds = xarray.Dataset(
            data_vars = depth_vars,
        )
        ds = ds.expand_dims({'ntiles': self.ntiles})
        # TODO add global attributes
        ds.to_netcdf(self.output_name)

    @classmethod
    def make_topog_realistic( self, topog_file, topog_field, min_depth,
                              num_filter_pass, flat_bottom, fill_first_row, filter_topog, round_shallow, fill_shallow,
                              deepen_shallow, smooth_topo_allow_deepening, vgrid_file, full_cell,
                              dont_fill_isolated_cells, on_grid, dont_change_landmask, kmt_min, dont_adjust_topo,
                              fraction_full_cell, dont_open_very_this_cell, min_thickness):
        pass

    @classmethod
    def make_rectangular_basin(self, bottom_depth):
        pass

    @classmethod
    def make_topog_gaussian(self, gauss_scale, gauss_amp, slope_x, slope_y):
        pass

    @classmethod
    def make_topog_bowl(self, bottom_depth, min_depth, bowl_south, bowl_north, bowl_west, bowl_east):
        pass

    @classmethod
    def make_topog_box_idealized(self, bottom_depth, min_depth):
        pass

    @classmethod
    def make_topog_box_channel(self, jwest_south, jwest_north, ieast_south, ieast_north, bottom_depth):
        pass

    @classmethod
    def make_topog_dome(dome_slope, dome_bottom, dome_embayment_west, dome_embayment_east, dome_embayment_south,
                        dome_embayment_depth):
        pass