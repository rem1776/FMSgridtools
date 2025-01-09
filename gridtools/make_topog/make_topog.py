#!/home/Ryan.Mulhall/.conda/envs/dev/bin/python3
# make_topog entrypoint script

import click
import xarray
from pathlib import Path

from gridtools_lib import TopogObj

MOSAIC_FILE_OPT_HELP="Path to a netCDF mosaic grid file to create a topography for"
TOPOG_TYPE_OPT_HELP="Specify 'type' of topography to generate, determines which algorithm is used to populate data." 
TOPOG_FILE_OPT_HELP="Specific to 'realistic' topog_type option; path to a netCDF file containing topography data or realistic topography option"
# TODO add rest of the help descriptions

@click.command()
# required args regardless of topog_type
@click.option("-m",
              "--mosaic",
              type = str,
              help = MOSAIC_FILE_OPT_HELP,
              required = True)
@click.option("-t",
              "--topog_type",
              type = str,
              help = TOPOG_TYPE_OPT_HELP,
              required = True)
# not specific to a type
@click.option("--x_refine",
              type = int,
              default = 2,
              help = "")
@click.option("--y_refine",
              type = int,
              default = 2,
              help = "")
@click.option("--output",
              type = str,
              default = "topog.nc",
              help = "The name of the created netCDF file that contains mosaic topography. Default value is topog.nc")
# shared between topog type opts
# TODO change one of these args to either min/max depth or top/bottom depth
@click.option("--bottom_depth",
              type = float,
              default = 5000,
              help = "")
@click.option("--min_depth",
              type = float,
              default = 10,
              help = "")
@click.option("--scale_factor",
              type = float,
              default = 1,
              help = "")
# realistic
@click.option("--topog_file",
              type = str,
              help = "",
              required = False)
@click.option("--topog_field",
              type = str,
              help = "",
              required = False)
@click.option("--num_filter_pass",
              type = int,
              default = 1,
              help = "")
@click.option("--flat_bottom",
              is_flag = True,
              help = "")
@click.option("--fill_first_row",
              is_flag = True,
              help = "")
@click.option("--filter_topog",
              is_flag = True,
              help = "")
@click.option("--full_cell",
              is_flag = True,
              help = "")
@click.option("--dont_fill_isolated_cells",
              is_flag = True,
              help = "")
@click.option("--dont_change_landmask",
              is_flag = True,
              help = "")
@click.option("--kmt_min",
              type = int,
              default = 2,
              help = "Minimum number of vertical levels")
@click.option("--dont_adjust_topo",
              is_flag = True,
              help = "")
@click.option("--fraction_full_cell",
              type = float,
              default = 0.2,
              help = "")
@click.option("--dont_open_very_this_cell",
              is_flag = True,
              help = "")
@click.option("--min_thickness",
              type = float,
              default = 0.1,
              help = "Minimum vertical thickness allowed")
@click.option("--rotate_poly",
              is_flag = True,
              help = "")
@click.option("--on_grid",
              is_flag = True,
              help = "")
@click.option("--round_shallow",
              is_flag = True,
              help = "")
@click.option("--fill_shallow",
              is_flag = True,
              help = "")
@click.option("--deepen_shallow",
              is_flag = True,
              help = "")
@click.option("--smooth_topo_allow_deepening",
              is_flag = True,
              help = "")
@click.option("--vgrid_file",
              type = str,
              required = False,
              help = "")
# gaussian
@click.option("--gauss_amp",
              type = float,
              default = 0.5,
              help = "")
@click.option("--gauss_scale",
              type = float,
              default = 0.25,
              help = "")
@click.option("--slope_x",
              type = float,
              default = 0,
              help = "")
@click.option("--slope_y",
              type = float,
              default = 0,
              help = "")
# bowl
@click.option("--bowl_south",
              type = int,
              default = 60,
              help = "")
@click.option("--bowl_north",
              type = int,
              default = 70,
              help = "")
@click.option("--bowl_west",
              type = int,
              default = 0,
              help = "")
@click.option("--bowl_east",
              type = int,
              default = 20,
              help = "")
# box channel
@click.option("--jwest_south",
              type = int,
              default = 0,
              help = "")
@click.option("--jwest_north",
              type = int,
              default = 0,
              help = "")
@click.option("--ieast_south",
              type = int,
              default = 0,
              help = "")
@click.option("--ieast_north",
              type = int,
              default = 0,
              help = "")
# dome
@click.option("--dome_slope",
              type = int,
              default = 0,
              help = "")
@click.option("--dome_bottom",
              type = int,
              default = 0,
              help = "")
@click.option("--dome_embayment_west",
              type = int,
              default = 0,
              help = "")
@click.option("--dome_embayment_east",
              type = int,
              default = 0,
              help = "")
@click.option("--dome_embayment_south",
              type = int,
              default = 0,
              help = "")
@click.option("--dome_embayment_depth",
              type = int,
              default = 0,
              help = "")
def make_topog(mosaic, topog_type, x_refine, y_refine, bottom_depth, min_depth, scale_factor, topog_file, topog_field,
               num_filter_pass, flat_bottom, fill_first_row, filter_topog, full_cell, dont_fill_isolated_cells,
               dont_change_landmask, kmt_min, dont_adjust_topo, fraction_full_cell, dont_open_very_this_cell,
               min_thickness, rotate_poly, on_grid, round_shallow, fill_shallow, deepen_shallow,
               smooth_topo_allow_deepening, vgrid_file, gauss_amp, gauss_scale, slope_x, slope_y, bowl_south,
               bowl_north, bowl_west, bowl_east, jwest_south, jwest_north, ieast_south, ieast_north, dome_slope,
               dome_bottom, dome_embayment_west, dome_embayment_east, dome_embayment_south, dome_embayment_depth, output):

    # check valid mosaic path and get tiles 
    if(not Path(mosaic).exists()):
        print("Invalid path given for mosaic file. Exiting...")
        exit(1)
    with xarray.open_dataset(mosaic) as ds:
        if 'ntiles' in ds.dims:
            ntiles = ds.sizes['ntiles']
        else:
            ntiles = 1

    # read in object fields from file
    mosaicGrid = "placeHolderForMosaicGridConstructor()"

    # create new TopogStruct for output
    topogOut = TopogObj(output_name=output, ntiles=ntiles)
    
    # call the specified algorithm for generating topography data
    if (topog_type == "realistic"):
        topogOut.make_topog_realistic(mosaicGrid, x_refine, y_refine, min_depth, scale_factor, num_filter_pass,
                                      flat_bottom, fill_first_row, filter_topog, round_shallow, fill_shallow,
                                      deepen_shallow, smooth_topo_allow_deepening, vgrid_file)
    elif (topog_type == "rectangular_basin"):
        topogOut.make_topog_rectangular_basin(mosaicGrid, x_refine, y_refine, scale_factor, bottom_depth)
    elif (topog_type == "gaussian"):
        topogOut.make_topog_gaussian()
    elif (topog_type == "bowl"):
        topogOut.make_topog_bowl()
    elif (topog_type == "idealized"):
        topogOut.make_topog_idealized()
    elif (topog_type == "box_channel"):
        topogOut.make_topog_box_channel()
    elif (topog_type == "dome"):
        topogOut.make_topog_dome()
    else:
        print("Error: invalid topog_type argument given, must be one of [realistic, gaussian, bowl, box_channel, dome]")
        exit(1)

    # write out the result
    topogOut.write_topog_file()

if __name__ == "__main__":
    make_topog()
