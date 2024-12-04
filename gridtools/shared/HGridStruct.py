import numpy as np
from typing import Optional

REGULAR_LONLAT_GRID = 1
TRIPOLAR_GRID = 2
FROM_FILE = 3
SIMPLE_CARTESIAN_GRID = 4
SPECTRAL_GRID = 5
CONFORMAL_CUBIC_GRID = 6
GNOMONIC_ED = 7
F_PLANE_GRID = 8
BETA_PLANE_GRID = 9
MISSING_VALUE = -9999.

from gridtools.wrappers import (
    mpp_close,
    mpp_dim_exist,
    mpp_get_dimlen,
    mpp_open,
    mpp_error,
)

class HGridStruct:
    method = "conformal"
    orientation = "center_pole"
    num_nest_args = 0
    present_stretch_factor = 0
    present_target_lon = 0
    present_target_lat = 0
    use_great_circle_algorithm = 0
    use_angular_midpoint = 0
    output_length_angle = 1
    verbose = 0
    geometry = "spherical"
    projection = "none"
    arcx = "small_circle"
    north_pole_tile = "0.0 90.0"
    north_pole_arcx = "0.0 90.0"
    discretization = "logically_rectangular"
    conformal = "true"
    grid_version = "0.2"

    def __init__(
            self,
            args: str,
            grid_type: str = "regular_lonlat_grid",
            my_grid_file: str = "",
            nxbnds: int = 2,
            nybnds: int = 2,
            xbnds: str,
            ybnds: str,
            nlon: str,
            nlat: str,
            dlon: str,
            dlat: str,
            lat_join: float = 65.0,
            nratio: int = 1,
            simple_dx: float = 0.0,
            simple_dy: float = 0.0,
            grid_name: str = "horizontal_grid",
            center: str = "none",
            shift_fac: float = 18.0,
            f_plane_latitude: float = 100.0,
            do_schmidt: Optional[int] = 0,
            do_cube_transform: Optional[int] = 0,
            stretch_factor: float = 0.0,
            target_lon: float = 0.0,
            target_lat: float = 0.0,
            nest_grids: int = 0,
            parent_tile: str,
            refine_ratio: str,
            istart_nest: str,
            iend_nest: str,
            jstart_nest: str,
            jend_nest: str,
            halo: int = 0,
            great_circle_algorithm: Optional[bool] = False,
            out_halo: int = 0,
            no_length_angle: Optional[bool] = False,
            angular_midpoint: Optional[bool] = False,
            rotate_poly: Optional[bool] = False,
            verbose: Optional[bool] = False,
    ):
        self._history = " ".join(args)
        self._grid_type = grid_type
        self._nxbnds = nxbnds
        self._nybnds = nybnds
        self._xbnds = xbnds.split(',')
        self._ybnds = ybnds.split(',')
        self._nlon = nlon.split(',')
        self._nlat = nlat.split(',')
        self._dlon = dlon.split(',')
        self._dlat = dlat.split(',')
        self._lat_join = lat_join
        self._nratio = nratio
        self._simple_dx = simple_dx
        self._simple_dy = simple_dy
        self._grid_name = grid_name
        self._center = center
        self._halo = halo
        self._out_halo = out_halo
        self._stretch_factor = stretch_factor
        self._shift_fac = shift_fac
        self._target_lon = target_lon
        self._target_lat = target_lat
        self._dx_bnds = self._dlon
        self._dy_bnds = self._dlat
        self._nx = None
        self._ny = None
        self._nxp = None
        self._nyp = None
        self._isc = None
        self._iec = None
        self._jsc = None
        self._jec = None
        self._x = None
        self._y = None
        self._dx = None
        self._area = None
        self._angle_dx = None
        self._angle_dy = None
        self._my_grid_file = my_grid_file.split(',')
        self._ntiles_file = len(self._my_grid_file)
        self._nxbnds0 = nxbnds
        self._nybnds0 = nybnds
        self._nxbnds1 = len(self._xbnds)
        self._nybnds1 = len(self._ybnds)
        self._nxbnds2 = len(self._nlon)
        self._nybnds2 = len(self._nlat)
        self._nxbnds3 = len(self._dlon)
        self._nybnds3 = len(self._dlat)
        self._f_plane_latitude = f_plane_latitude
        if self._stretch_factor:
            self.present_stretch_factor = 1
        if self._target_lon:
            self.present_target_lon = 1
        if self._target_lat:
            self.present_target_lat = 1
        self._nest_grids = nest_grids
        if refine_ratio:
            self._refine_ratio = refine_ratio.split(',')
            self._num_nest_args = len(self._refine_ratio)
        if parent_tile:
            self._parent_tile = parent_tile.split(',')
            self._num_nest_args = len(self._parent_tile)
        if istart_nest:
            self._istart_nest = istart_nest.split(',')
            self._num_nest_args = len(self._istart_nest)
        if iend_nest:
            self._iend_nest = iend_nest.split(',')
            self._num_nest_args = len(self._iend_nest)
        if jstart_nest:
            self._jstart_nest = jstart_nest.split(',')
            self._num_nest_args = len(self._jstart_nest)
        if jend_nest:
            self._jend_nest = jend_nest.split(',')
            self._num_nest_args = len(self._jend_nest)
        if great_circle_algorithm:
            self.use_great_circle_algorithm = 1
        if no_length_angle:
            self.output_length_angle = 0
        if angular_midpoint:
            self.use_angular_midpoint = 1
        if rotate_poly:
            set_rotate_poly_true()
        self._do_schmidt = do_schmidt
        self._do_cube_transform = do_cube_transform
        self._verbose = verbose
        if grid_type == "regular_lonlat_grid":
            self._my_grid_type = REGULAR_LONLAT_GRID
        elif grid_type == "tripolar_grid":
            self._my_grid_type = TRIPOLAR_GRID
        elif grid_type == "from_file":
            self._my_grid_type = FROM_FILE
        elif grid_type == "simple_cartesian_grid":
            self._my_grid_type = SIMPLE_CARTESIAN_GRID
        elif grid_type == "spectral_grid":
            self._my_grid_type = SPECTRAL_GRID
        elif grid_type == "conformal_cubic_grid":
            self._my_grid_type = CONFORMAL_CUBIC_GRID
        elif grid_type == "gnomonic_ed":
            self._my_grid_type = GNOMONIC_ED
        elif grid_type == "f_plane_grid":
            self._my_grid_type = F_PLANE_GRID
        elif grid_type == "beta_plane_grid":
            self._my_grid_type = BETA_PLANE_GRID
        else:
            mpp_error("GridStruct: only grid_type = 'regular_lonlat_grid', 'tripolar_grid', 'from_file', "
                      "'gnomonic_ed', 'conformal_cubic_grid', 'simple_cartesian_grid', "
                      "'spectral_grid', 'f_plane_grid' and 'beta_plane_grid' is implemented")
            
        if(self._my_grid_type != GNOMONIC_ED and self._out_halo  != 0):
            mpp_error("GridStruct: out_halo should not be set when grid_type = gnomonic_ed")
        if(self._out_halo !=0 and self._out_halo != 1):
            mpp_error("GridStruct: out_halo should be 0 or 1")
        if( self._my_grid_type != GNOMONIC_ED and self._do_schmidt ):
            mpp_error("GridStruct: --do_schmidt should not be set when grid_type is not 'gnomonic_ed'")
        if( self._my_grid_type != GNOMONIC_ED and self._do_cube_transform ):
            mpp_error("GridStruct: --do_cube_transform should not be set when grid_type is not 'gnomonic_ed'")
        if ( self._do_cube_transform and self._do_schmidt ):
            mpp_error("GridStruct: both --do_cube_transform and --do_schmidt are set")

        self.use_legacy = 0

        # check the command-line arguments to make sure the values are suitable

        self.command_line_check()

        self._nxl = None
        self._nyl = None
        self._ntiles = 1
        self._ntiles_global = 1

        self.get_super_grid_size()

        self.allocate_space()


    def command_line_check(self):
        if( self._my_grid_type == REGULAR_LONLAT_GRID or self._my_grid_type == TRIPOLAR_GRID or
           self._my_grid_type == F_PLANE_GRID or self._my_grid_type == BETA_PLANE_GRID ):
            self._nxbnds = self._nxbnds0
            self._nybnds = self._nybnds0
            if( self._nxbnds <2 or self._nybnds < 2):
                mpp_error("GridStruct: grid type is 'regular_lonlat_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', " 
                          "both nxbnds and nybnds should be no less than 2")
            if( self._nxbnds != self._nxbnds1 ):
                mpp_error("GridStruct: grid type is 'regular_lonlat_grid, 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', " 
                          "nxbnds does not match number of entry in xbnds")
            if( self._nybnds != self._nybnds1 ):
                mpp_error("GridStruct: grid type is 'regular_lonlat_grid, 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', " 
                          "nybnds does not match number of entry in ybnds")
            num_specify = 0
            if( self._nxbnds2 > 0 and self._nybnds2 > 0 ):
                num_specify += 1
            if( self._nxbnds3 > 0 and self._nybnds3 > 0 ):
                num_specify += 1
                self.use_legacy = 1
            if( num_specify == 0 ):
                mpp_error("GridStruct: grid type is 'regular_lonlat_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', "
                          "need to specify one of the pair --nlon --nlat or --dlon --dlat")
            if( num_specify == 2 ):
                mpp_error("GridStruct: grid type is 'regular_lonlat_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', "
                          "can not specify both --nlon --nlat and --dlon --dlat")
            if self.use_legacy:
                if( self._nxbnds != self._nxbnds3 ):
                    mpp_error("GridStruct: grid type is 'tripolar_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', "
                              "nxbnds does not match number of entry in dlon")
                if( self._nybnds != self._nybnds3 ):
                    mpp_error("GridStruct: grid type is 'tripolar_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', "
                              "nybnds does not match number of entry in dlat")
            else:
                if( self._nxbnds != self._nxbnds2+1 ):
                    mpp_error("GridStruct: grid type is 'tripolar_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', "
                              "nxbnds does not match number of entry in nlon")
                if( self._nybnds != self._nybnds2+1 ):
                    mpp_error("GridStruct: grid type is 'tripolar_grid', 'tripolar_grid', 'f_plane_grid' or 'beta_plane_grid', "
                              "nybnds does not match number of entry in nlat")
                    
        if( self._my_grid_type == CONFORMAL_CUBIC_GRID or self._my_grid_type == GNOMONIC_ED ):
            self._ntiles = 6
            self._ntiles_global = 6
        if( self._my_grid_type != GNOMONIC_ED and self._nest_grids ):
            mpp_error("GridStruct: --nest_grids can be set only when grid_type = 'gnomonic_ed'")
        if( self._my_grid_type == TRIPOLAR_GRID ):
            self.projection = "tripolar"
            if( self._nxbnds != 2):
                mpp_error("GridStruct: grid type is 'tripolar_grid', nxbnds should be 2")
        elif( self._my_grid_type == FROM_FILE):
            if(self._ntiles_file == 0):
                mpp_error("GridStruct: grid_type is 'from_file', but my_grid_file is not specified")
            self._ntiles = self._ntiles_file
            self._ntiles_global = self._ntiles_file
            for n in range(self._ntiles):
                if ".nc" in self._my_grid_file:
                    fid = mpp_open(self._my_grid_file[n], MPP_READ)
                    if(mpp_dim_exist(fid, "grid_xt")):
                        if(mpp_dim_exist(fid, "grid_yt") == 0):
                            mpp_error("GridStruct: grid_yt should be a dimension when grid_xt is a dimension")
                        self._nlon[n] = mpp_get_dimlen(fid, "grid_xt")*2
                        self._nlat[n] = mpp_get_dimlen(fid, "grid_yt")*2
                    elif(mpp_dim_exist(fid, "rlon")):
                        if(mpp_dim_exist(fid, "rlat") == 0):
                            mpp_error("GridStruct: rlat should be a dimension when rlon is a dimension")
                        self._nlon[n] = mpp_get_dimlen(fid, "rlon")*2
                        self._nlat[n] = mpp_get_dimlen(fid, "rlat")*2
                    elif(mpp_dim_exist(fid, "lon")):
                        if( mpp_dim_exist(fid, "lat") == 0):
                            mpp_error("GridStruct: lat should be a dimension when lon is a dimension")
                        self._nlon[n] = mpp_get_dimlen(fid, "lon")*2
                        self._nlat[n] = mpp_get_dimlen(fid, "lat")*2
                    elif(mpp_dim_exist(fid, "i")):
                        if( mpp_dim_exist(fid, "j") == 0):
                            mpp_error("GridStruct: j should be a dimension when i is a dimension")
                        self._nlon[n] = mpp_get_dimlen(fid, "i")*2
                        self._nlat[n] = mpp_get_dimlen(fid, "j")*2
                    elif(mpp_dim_exist(fid, "x")):
                        if( mpp_dim_exist(fid, "y") == 0):
                            mpp_error("GridStruct: y should be a dimension when x is a dimension")
                        self._nlon[n] = mpp_get_dimlen(fid, "x")*2
                        self._nlat[n] = mpp_get_dimlen(fid, "y")*2
                    else:
                        mpp_error("GridStruct: none of grid_xt, rlon, lon, x, and i is a dimension in input file")
                    mpp_close(fid)
                else:
                    if(self._nxbnds2 != self._ntiles or self._nybnds2 != self._ntiles ):
                        mpp_error("GridStruct: grid type is 'from_file', number entry entered "
                                  "through --nlon and --nlat should be equal to number of files "
                                  "specified through --my_grid_file")
            for n in range(1,self._ntiles):
                if( self._nlon[n] != self._nlon[0] or self._nlat[n] != self._nlat[0]):
                    mpp_error("GridStruct: grid_type is from_file, all the tiles should "
                              "have same grid size, contact developer")
        elif(my_grid_type == SIMPLE_CARTESIAN_GRID):
            self.geometry = "planar"
            self.north_pole_tile = "none"
            if(self._nxbnds1 != 2 or self._nybnds1 != 2 ):
                mpp_error("GridStruct: grid type is 'simple_cartesian_grid', number entry entered "
                          "through --xbnds and --ybnds should be 2")
            if(self._nxbnds2 != 1 or self._nybnds2 != 1 ):
                mpp_error("GridStruct: grid type is 'simple_cartesian_grid', number entry entered "
                          "through --nlon and --nlat should be 1")
            if(self._simple_dx == 0 or self._simple_dy == 0):
                mpp_error("GridStruct: grid_type is 'simple_cartesian_grid', "
                          "both simple_dx and simple_dy both should be specified")
        elif( self._my_grid_type == SPECTRAL_GRID ):
            if(self._nxbnds2 != 1 or self._nybnds2 != 1 ):
                mpp_error("GridStruct: grid type is 'spectral_grid', number entry entered "
                          "through --nlon and --nlat should be 1")
        elif( self._my_grid_type == CONFORMAL_CUBIC_GRID ):
            self.projection = "cube_gnomonic"
            self.conformal = "FALSE"
            if(self._nxbnds2 != 1 ):
                mpp_error("GridStruct: grid type is 'conformal_cubic_grid', number entry entered "
                          "through --nlon should be 1")
            if(self._nratio < 1): 
                mpp_error("make_hgrid: grid type is 'conformal_cubic_grid', nratio should be a positive integer")
        elif( my_grid_type == GNOMONIC_ED ):
            self.projection = "cube_gnomonic"
            self.conformal = "FALSE"
            if( self._do_schmidt or self._do_cube_transform ):
                if( self.present_stretch_factor == 0 or self.present_target_lon == 0 or self.present_target_lat == 0 ):
                    mpp_error("GridStruct: grid type is 'gnomonic_ed, --stretch_factor, --target_lon "
                              "and --target_lat must be set when --do_schmidt or --do_cube_transform is set")
            # if nest_grids >= 1
            for n in range(self._nest_grids):
                if(self._refine_ratio[n] == 0): 
                    mpp_error("GridStruct: --refine_ratio must be set when --nest_grids is set")
                if(self._parent_tile[n] == 0 and mpp_pe()==mpp_root_pe()):
                    print("NOTE from make_hgrid: parent_tile is 0, the output grid will have resolution refine_ration*nlon")
                else:
                    if(self._istart_nest[n] == 0):
                        mpp_error("GridStruct: --istart_nest must be set when --nest_grids is set")
                    if(self._iend_nest[n] == 0):
                        mpp_error("GridStruct: --iend_nest must be set when --nest_grids is set")
                    if(self._jstart_nest[n] == 0):
                        mpp_error("GridStruct: --jstart_nest must be set when --nest_grids is set")
                    if(self._jend_nest[n] == 0):
                        mpp_error("GridStruct: --jend_nest must be set when --nest_grids is set")
                    if(self._halo == 0 ):
                        mpp_error("GridStruct: --halo must be set when --nest_grids is set")
                    self._ntiles += 1
                    if (self._verbose):
                        print(f"Configuration for nest {ntiles} validated.")
            if self._verbose:
                print(f"Updated number of tiles, including nests (ntiles): {ntiles}")
            if(self._nxbnds2 != 1):
                mpp_error("GridStruct: grid type is 'gnomonic_cubic_grid', number entry entered "
                          "through --nlon should be 1")
        elif(self._my_grid_type == F_PLANE_GRID or  self._my_grid_type == BETA_PLANE_GRID):
            if(self._f_plane_latitude > 90 or self._f_plane_latitude < -90.):
                mpp_error("GridStruct: f_plane_latitude should be between -90 and 90.")
            if(self._f_plane_latitude > self._ybnds[self._nybnds-1] or self._f_plane_latitude < self._ybnds[0] ):
                if(mpp_pe() == mpp_root_pe()):
                    print("Warning from GridStruct: f_plane_latitude is not inside the latitude range of the grid")
                if(mpp_pe() == mpp_root_pe()):
                    print(f"GridStruct: setting geometric factor according to f-plane with f_plane_latitude = {f_plane_latitude}")
    
    def get_super_grid_size(self):
        self._nxl = np.zeros(shape=self._ntiles, dtype=int)
        self._nyl = np.zeros(shape=self._ntiles, dtype=int)
        if self.use_legacy:
            self._nxl[0] = get_legacy_grid_size(self._nxbnds, self._xbnds, self._dx_bnds)
            self._nyl[0] = get_legacy_grid_size(self._nybnds, self._ybnds, self._dy_bnds)
        elif(self._my_grid_type == GNOMONIC_ED or self._my_grid_type == CONFORMAL_CUBIC_GRID):
            #    NOTE: The if-block in the loop below is changed with multiple nests.
            #    It appeared to allow refinement of the global grid
            #    without using any nests. However, the method used the
            #    nesting parameters "parent_tile" and "refine_ratio" to
            #    achieve this, which was enabled by setting parent_tile = 0 .
            #    This is no longer possible, as parent_tile is now an array.
            #    Instead, if the first value in the list of parent_tile values is 0,
            #    then the first value in the list of refine_ratio values will be
            #    applied to the global grid. This global-refinement application
            #    may not be valid for all permutations of nesting and refinement. [Ahern]
            for n in range(self._ntiles_global):
                self._nxl[n] = self._nlon[0]
                self._nyl[n] = self._nxl[n]
                if(self._nest_grids and self._parent_tile[0] == 0):
                    self._nxl[n] *= self._refine_ratio[0]
                    self._nyl[n] *= self._refine_ratio[0]
            
            for n in range(self._ntiles_global,self._ntiles):
                nn = n - self._ntiles_global
                self._nxl[n] = (self._iend_nest[nn] - self._istart_nest[nn] + 1) * self._refine_ratio[nn]
                self._nyl[n] = (self._jend_nest[nn] - self._jstart_nest[nn] + 1) * self._refine_ratio[nn]
        elif(self._my_grid_type == FROM_FILE):
            for n in range(self._ntiles_global):
                self._nxl[n] = self._nlon[n]
                self._nyl[n] = self._nlat[n]
        else:
            self._nxl[0] = 0
            self._nyl[0] = 0
            for n in range(self._nxbnds - 1):
                self._nxl[0] += self._nlon[n]
            for n in range(self._nybnds - 1):
                self._nyl[0] += self._nlat[n]
        self._nx = self._nxl[0]
        self._ny = self._nyl[0]
        self._nxp = self._nx + 1
        self._nyp = self._ny + 1
        
        # --no_length_angle should only be set when grid_type == GNOMONIC_ED
        if (not self.output_length_angle and self._my_grid_type != GNOMONIC_ED):
            mpp_error("GridStruct: --no_length_angle is set but grid_type is not 'gnomonic_ed'")

    def allocate_space(self):
        for n_nest in range(self._ntiles):
            print(f"[INFO] tile: {n_nest}, nxl[{nxl[n_nest]}], nyl[{nyl[n_nest]}], ntiles: {ntiles}")
        
        if (self._my_grid_type == FROM_FILE):
            self._size1 = self._size2 = self._size3 = self._size4 = 0
            for n in range(self._ntiles_global):
                self._size1 += (self._nlon[n] + 1) * (self._nlat[n] + 1)
                self._size2 += (self._nlon[n] + 1) * (self._nlat[n] + 1 + 1)
                self._size3 += (self._nlon[n] + 1 + 1) * (self._nlat[n] + 1)
                self._size4 += (self._nlon[n] + 1) * (self._nlat[n] + 1)
        else:
            self._size1 = self._nxp * self._nyp * self._ntiles_global
            self._size2 = self._nxp * (self._nyp + 1) * self._ntiles_global
            self._size3 = (self._nxp + 1) * self._nyp * self._ntiles_global
            self._size4 = self._nxp * self._nyp * self._ntiles_global
        
        if(not(self._nest_grids==1 and self._parent_tile[0] == 0)):
            for n_nest in range(self._ntiles_global,self._ntiles_global+self._nest_grids):
                if self._verbose:
                    print(f"[INFO] Adding memory size for nest {n_nest}, nest_grids: {nest_grids}")
                self._size1 += (self._nxl[n_nest]+1) * (self._nyl[n_nest]+1)
                self._size2 += (self._nxl[n_nest]+1) * (self._nyl[n_nest]+2)
                self._size3 += (self._nxl[n_nest]+2) * (self._nyl[n_nest]+1)
                self._size4 += (self._nxl[n_nest]+1) * (self._nyl[n_nest]+1)
        
        if self._verbose:
            print(f"[INFO] Allocating arrays of size {size1} for x, y based on nxp: {nxp} nyp: {nyp} ntiles: {ntiles}")
        self._x = np.zeros(shape=self._size1, dtype=float)
        self._y = np.zeros(shape=self._size1, dtype=float)
        self._area = np.zeros(shape=self._size4, dtype=float)
        if self.output_length_angle:
            self._dx = np.zeros(shape=self._size2, dtype=float)
            self._dy = np.zeros(shape=self._size3, dtype=float)
            self._angle_dx = np.zeros(shape=self._size1, dtype=float)
            if (self.conformal == "true"):
                self._angle_dy = np.zeros(shape=self._size1, dtype=float)
        self._isc = 0
        self._iec = self._nx - 1
        self._jsc = 0
        self._jec = self._ny - 1

    def fill_cubic_grid_halo(
            self,
            nx: int,
            ny: int,
            halo: int,
            data: np.ndarray,
            data1_all: np.ndarray,
            data2_all: np.ndarray,
            tile: int,
            ioff: int,
            joff: int,
    ):
        nxp = nx+ioff
        nyp = ny+joff
        nxph = nx+ioff+2*halo
        nyph = ny+joff+2*halo
        
        for i in range(nxph*nyph):
            data[i] = MISSING_VALUE
        
        # first copy computing domain data
        for j in range(1, nyp+1):
            for i in range(1, nxp+1):
                data[j*nxph+1] = data1_all[tile*nxp*nyp+(j-1)*nxp+(i-1)]
        
        ntiles = 6
        
        if(tile%2 == 1):
            # tile 2, 4, 6
            lw = (tile+ntiles-1)%ntiles
            le = (tile+ntiles+2)%ntiles
            ls = (tile+ntiles-2)%ntiles
            ln = (tile+ntiles+1)%ntiles
            for j in range(1,nyp+1):
                data[j*nxph] = data1_all[lw*nxp*nyp+(j-1)*nxp+nx-1]  # west halo
                data[j*nxph+nxp+1] = data2_all[le*nxp*nyp+ioff*nxp+nyp-j]  # east halo
            for i in range(1,nxp+1):
                data[i] = data2_all[ls*nxp*nyp+(nxp-i)*nyp+(nx-1)]  # south
                data[(nyp+1)*nxph+i] = data1_all[ln*nxp*nyp+joff*nxp+i-1]  # north
        else:
            # tile 1, 3, 5
            lw = (tile+ntiles-2)%ntiles
            le = (tile+ntiles+1)%ntiles
            ls = (tile+ntiles-1)%ntiles
            ln = (tile+ntiles+2)%ntiles
            for j in range(1,nyp+1):
                data[j*nxph] = data2_all[lw*nxp*nyp+(ny-1)*nxp+nyp-j]  # west halo
                data[j*nxph+nxp+1] = data1_all[le*nxp*nyp+(j-1)*nxp+ioff]  # east halo
            for i in range(1,nxp+1):
                data[i] = data1_all[ls*nxp*nyp+(ny-1)*nxp+i-1] # south
                data[(nyp+1)*nxph+i] = data2_all[ln*nxp*nyp+(nxp-i)*nyp+joff] # north

    def write_data(self):
        dimlist = np.zeros(shape=5, dtype=int)
        dims = np.zeros(shape=2, dtype=int)
        start = np.zeros(shape=2, dtype=int)
        nwrite = np.zeros(shape=4, dtype=int)
        pos_c = 0
        pos_e = 0
        pos_t = 0
        pos_n = 0

        for n in range(self._ntiles):
            tilename = f"tile{n+1}"
            if self._ntiles > 1:
                outfile = f"{self._grid_name}.tile{n+1}.nc"
            else:
                outfile = f"{self._grid_name}.nc"

            if self._verbose:
                print(f"Writing out {outfile}")

            fid = mpp_open(outfile, MPP_WRITE)
            # define dimension
            nx = self._nxl[n]
            ny = self._nyl[n]
            if self._verbose:
                print(f"[INFO] Outputting arrays of size nx: {nx} and ny: {ny} for tile: {n}")
            nxp = nx + 1
            nyp = ny + 1
            dimlist[0] = mpp_def_dim(fid, "string", STRINGLEN)
            dimlist[1] = mpp_def_dim(fid, "nx", nx+2*self._out_halo)
            dimlist[2] = mpp_def_dim(fid, "ny", ny+2*self._out_halo)
            dimlist[3] = mpp_def_dim(fid, "nxp", nxp+2*self._out_halo)
            dimlist[4] = mpp_def_dim(fid, "nyp", nyp+2*self._out_halo)
            # define variable
            if self.north_pole_tile == "none":
                id_tile = mpp_def_var(fid, "tile", MPP_CHAR, 1, dimlist, 4, "standard_name", "grid_tile_spec",
                                      "geometry", self.geometry, "discretization", self.discretization, "conformal", self.conformal )
            elif self.projection == "none":
                id_tile = mpp_def_var(fid, "tile", MPP_CHAR, 1, dimlist, 5, "standard_name", "grid_tile_spec",
                                      "geometry", self.geometry, "north_pole", self.north_pole_tile, "discretization",
                                      self.discretization, "conformal", self.conformal )
            else:
                id_tile = mpp_def_var(fid, "tile", MPP_CHAR, 1, dimlist, 6, "standard_name", "grid_tile_spec",
                                      "geometry", self.geometry, "north_pole", self.north_pole_tile, "projection", self.projection,
                                      "discretization", self.discretization, "conformal", self.conformal )
            dims[0] = dimlist[4]
            dims[1] = dimlist[3]
            id_x = mpp_def_var(fid, "x", MPP_DOUBLE, 2, dims, 2, "standard_name", "geographic_longitude",
                               "units", "degree_east") 
            if self._out_halo > 0:
                mpp_def_var_att_double(fid, id_x, "_FillValue", MISSING_VALUE)
            id_y = mpp_def_var(fid, "y", MPP_DOUBLE, 2, dims, 2, "standard_name", "geographic_latitude",
                               "units", "degree_north")
            if self._out_halo > 0:
                mpp_def_var_att_double(fid, id_y, "_FillValue", MISSING_VALUE)
            if self.output_length_angle:
                dims[0] = dimlist[4]
                dims[1] = dimlist[1]
                id_dx = mpp_def_var(fid, "dx", MPP_DOUBLE, 2, dims, 2, "standard_name", "grid_edge_x_distance",
                                    "units", "meters")
                if self._out_halo > 0:
                    mpp_def_var_att_double(fid, id_dx, "_FillValue", MISSING_VALUE)
                dims[0] = dimlist[2]
                dims[1] = dimlist[3]
                id_dy = mpp_def_var(fid, "dy", MPP_DOUBLE, 2, dims, 2, "standard_name", "grid_edge_y_distance",
                                    "units", "meters")
                if self._out_halo > 0:
                    mpp_def_var_att_double(fid, id_dy, "_FillValue", MISSING_VALUE)
            dims[0] = dimlist[2]
            dims[1] = dimlist[1]
            id_area = mpp_def_var(fid, "area", MPP_DOUBLE, 2, dims, 2, "standard_name", "grid_cell_area",
                                  "units", "m2" )
            if self._out_halo > 0:
                mpp_def_var_att_double(fid, id_area, "_FillValue", MISSING_VALUE)
            if self.output_length_angle:
                dims[0] = dimlist[4]
                dims[1] = dimlist[3]
                id_angle_dx = mpp_def_var(fid, "angle_dx", MPP_DOUBLE, 2, dims, 2, "standard_name",
                                          "grid_vertex_x_angle_WRT_geographic_east", "units", "degrees_east")
                if self._out_halo > 0:
                    mpp_def_var_att_double(fid, id_angle_dx, "_FillValue", MISSING_VALUE)
                if self.conformal != "true":
                    id_angle_dy = mpp_def_var(fid, "angle_dy", MPP_DOUBLE, 2, dims, 2, "standard_name",
                                              "grid_vertex_y_angle_WRT_geographic_north", "units", "degrees_north")
                    if self._out_halo > 0:
                        mpp_def_var_att_double(fid, id_angle_dy, "_FillValue", MISSING_VALUE)
            if self.north_pole_arcx == "none":
                id_arcx = mpp_def_var(fid, "arcx", MPP_CHAR, 1, dimlist, 1, "standard_name", "grid_edge_x_arc_type" )
            else:
                id_arcx = mpp_def_var(fid, "arcx", MPP_CHAR, 1, dimlist, 2, "standard_name", "grid_edge_x_arc_type",
                                      "north_pole", north_pole_arcx )
            print_provenance_gv_gca(fid, self._history, self.grid_version, self.use_great_circle_algorithm)
            if n >= self._ntiles_global:
                mpp_def_global_att(fid, "nest_grids", "TRUE")
            mpp_end_def(fid)

            for m in range(4):
                start[m] = 0
                nwrite[m] = 0
            nwrite[0] = len(tilename)
            mpp_put_var_value_block(fid, id_tile, start, nwrite, tilename )

            if self._out_halo == 0:
                if self._verbose:
                    print(f"[INFO] START NC XARRAY write out_halo=0 tile number = n: {n} offset = pos_c: {pos_c}")
                    print(f"[INFO] XARRAY: n: {n} x[0]: {self._x[pos_c]} x[1]: {self._x[pos_c+1]} x[2]: {self._x[pos_c+2]} 
                          x[3]: {self._x[pos_c+3]} x[4]: {self._x[pos_c+4]} x[5]: {self._x[pos_c+5]} x[10]: {self._x[pos_c+10]}")
                    if n > 0:
                        print(f"[INFO] XARRAY: n: {n} x[0]: {self._x[pos_c]} x[-1]: {self._x[pos_c-1]} x[-2]: {self._x[pos_c-2]} 
                              x[-3]: {self._x[pos_c-3]} x[-4]: {self._x[pos_c-4]} x[-5]: {self._x[pos_c-5]} x[-10]: {self._x[pos_c-10]}")
                mpp_put_var_value(fid, id_x, self._x+pos_c)
                mpp_put_var_value(fid, id_y, self._y+pos_c)
                if self.output_length_angle:
                    mpp_put_var_value(fid, id_dx, self._dx+pos_n)
                    mpp_put_var_value(fid, id_dy, self._dy+pos_e)
                mpp_put_var_value(fid, id_area, self._area+pos_t)
                if self.output_length_angle:
                    mpp_put_var_value(fid, id_angle_dx, self._angle_dx+pos_c)
                    if self.conformal != "true":
                        mpp_put_var_value(fid, id_angle_dy, self._angle_dy+pos_c)
            else:
                tmp = np.zeros(shape=(nxp+2*self._out_halo)*(nyp+2*self._out_halo), dtype=float)
                if self._verbose:
                    print(f"[INFO] INDEX NC write with halo tile number = n: {n}")
                self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._x, self._x, n, 1, 1)
                mpp_put_var_value(fid, id_x, tmp)
                self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._y, self._y, n, 1, 1)
                mpp_put_var_value(fid, id_y, tmp)
                if self.output_length_angle:
                    self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._angle_dx, self._angle_dx, n, 1, 1)
                    mpp_put_var_value(fid, id_angle_dx, tmp)
                    if self.conformal != "true":
                        self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._angle_dy, self._angle_dy, n, 1, 1)
                        mpp_put_var_value(fid, id_angle_dy, tmp)
                    self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._dx, self._dy, n, 0, 1)
                    mpp_put_var_value(fid, id_dx, tmp)
                    self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._dy, self._dx, n, 1, 0)
                    mpp_put_var_value(fid, id_dy, tmp)
                self.fill_cubic_grid_halo(nx, ny, self._out_halo, tmp, self._area, self._area, n, 0, 0)
                mpp_put_var_value(fid, id_area, tmp)

            nwrite[0] = len(self.arcx)
            mpp_put_var_value_block(fid, id_arcx, start, nwrite, self.arcx )

            if self._verbose:
                print(f"About to close {outfile}")
            mpp_close(fid)

            nx = self._nxl[n]
            ny = self._nyl[n]
            nxp = nx + 1
            nyp = ny + 1

            if self._verbose:
                print(f"[INFO] INDEX Before increment n: {n} pos_c {pos_c} nxp {nxp} nyp {nyp} nxp*nyp {nxp*nyp}")
            pos_c += nxp*nyp
            if self._verbose:
                print(f"[INFO] INDEX After increment n: {n} pos_c {n}.")
            pos_e += nxp*ny
            pos_n += nx*nyp
            pos_t += nx*ny

    @property
    def history(self):
        return self._history
    
    @property
    def grid_type(self):
        return self._grid_type
    
    @property
    def nxbnds(self):
        return self._nxbnds
    
    @property
    def nybnds(self):
        return self._nybnds
    
    @property
    def nxbnds0(self):
        return self._nxbnds0
    
    @property
    def nybnds0(self):
        return self._nybnds0
    
    @property
    def nxbnds1(self):
        return self._nxbnds1
    
    @property
    def nybnds1(self):
        return self._nybnds1
    
    @property
    def nxbnds2(self):
        return self._nxbnds2
    
    @property
    def nybnds2(self):
        return self._nybnds2
    
    @property
    def nxbnds3(self):
        return self._nxbnds3
    
    @property
    def nybnds3(self):
        return self._nybnds3
    
    @property
    def xbnds(self):
        return self._xbnds
    
    @property
    def ybnds(self):
        return self._ybnds
    
    @property
    def nlon(self):
        return self._nlon
    
    @property
    def nlat(self):
        return self._nlat
    
    @property
    def dlon(self):
        return self._dlon
    
    @property
    def dlat(self):
        return self._dlat
    
    @property
    def lat_join(self):
        return self._lat_join
    
    @property
    def nratio(self):
        return self._nratio
    
    @property
    def simple_dx(self):
        return self._simple_dx
    
    @property
    def simple_dy(self):
        return self._simple_dy
    
    @property
    def grid_name(self):
        return self._grid_name
    
    @property
    def my_grid_file(self):
        return self._my_grid_file
    
    @property
    def center(self):
        return self._center
    
    @property
    def halo(self):
        return self._halo
    
    @property
    def out_halo(self):
        return self._out_halo
    
    @property
    def stretch_factor(self):
        return self._stretch_factor
    
    @property
    def shift_fac(self):
        return self._shift_fac
    
    @property
    def target_lon(self):
        return self._target_lon
    
    @property
    def target_lat(self):
        return self._target_lat
    
    @property
    def dx_bnds(self):
        return self._dx_bnds
    
    @property
    def dy_bnds(self):
        return self._dy_bnds
    
    @property
    def nx(self):
        if self._nx is None:
            self.get_super_grid_size()
        return self._nx
    
    @property
    def ny(self):
        if self._ny is None:
            self.get_super_grid_size()
        return self._ny
    
    @property
    def nxp(self):
        if self._nxp is None:
            self.get_super_grid_size()
        return self._nxp
    
    @property
    def nyp(self):
        if self._nyp is None:
            self.get_super_grid_size()
        return self._nyp
    
    @property
    def nxl(self):
        if self._nxl is None:
            self.get_super_grid_size()
        return self._nxl
    
    @property
    def nyl(self):
        if self._nyl is None:
            self.get_super_grid_size()
        return self._nyl
    
    @property
    def ntiles(self):
        if self._ntiles is None:
            self.command_line_check()
        return self._ntiles
    
    @property
    def ntiles_global(self):
        if self._ntiles_global is None:
            self.command_line_check()
        return self._ntiles_global
    
    @property
    def isc(self):
        if self._isc is None:
            self.allocate_space()
        return self._isc
    
    @property
    def iec(self):
        if self._iec is None:
            self.allocate_space()
        return self._iec
    
    @property
    def jsc(self):
        if self._jsc is None:
            self.allocate_space()
        return self._jsc
    
    @property
    def jec(self):
        if self._jec is None:
            self.allocate_space()
        return self._jec
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def dx(self):
        return self._dx
    
    @property
    def dy(self):
        return self._dy
    
    @property
    def area(self):
        return self._area
    
    @property
    def angle_dx(self):
        return self._angle_dx
    
    @property
    def angle_dy(self):
        return self._angle_dy
    
    @property
    def ntiles_file(self):
        return self._ntiles_file
    
    @property
    def f_plane_latitude(self):
        return self._f_plane_latitude
    
    @property
    def nest_grids(self):
        return self._nest_grids
    
    @property
    def refine_ratio(self):
        return self._refine_ratio
    
    @property
    def parent_tile(self):
        return self._parent_tile
    
    @property
    def istart_nest(self):
        return self._istart_nest
    
    @property
    def iend_nest(self):
        return self._iend_nest
    
    @property
    def jstart_nest(self):
        return self._jstart_nest
    
    @property
    def jend_nest(self):
        return self._jend_nest
    
    @property
    def do_schmidt(self):
        return self._do_schmidt
    
    @property
    def do_cube_transform(self):
        return self._do_cube_transform
    
    @property
    def verbose(self):
        return self._verbose