import numpy as np
import numpy.typing as npt
import xarray as xr
from typing import List, Optional, Type
import dataclasses
from math import cos, sin, ceil

D2R = np.pi/180

#Adapted from tools/libfrencutils/mpp_domain.h

@dataclasses.dataclass
class domain1d:
    start: int = None
    end: int = None
    size: int = None
    sizeg: int = None
    beglist: npt.NDArray[np.int32] = None
    endlist: npt.NDArray[np.int32] = None

@dataclasses.dataclass
class domain2d:
    isc: int = None
    iec: int = None
    jsc: int = None
    jec: int = None
    isd: int = None
    ied: int = None
    jsd: int = None
    jed: int = None
    nxc: int = None
    nyc: int = None
    nxd: int = None
    nyd: int = None
    nxg: int = None
    nyg: int = None
    isclist: npt.NDArray[np.int32] = None
    ieclist: npt.NDArray[np.int32] = None
    jsclist: npt.NDArray[np.int32] = None
    jeclist: npt.NDArray[np.int32] = None
    xhalo: int
    yhalo: int

#Adapted from tools/fregrid/globals.h

@dataclasses.dataclass
class GridStruct:
    is_cyclic: int = None
    is_tripolar: int = None
    halo: int = None
    nx: int = None
    ny: int = None
    nx_fine: int = None
    ny_fine: int = None
    isc: int = None
    iec: int = None
    jsc: int = None
    jec: int = None
    nxc: int = None
    nyc: int = None
    lonc: npt.NDArray[np.float64] = None
    latc: npt.NDArray[np.float64] = None
    lont: npt.NDArray[np.float64] = None
    latt: npt.NDArray[np.float64] = None
    xt: npt.NDArray[np.float64] = None
    yt: npt.NDArray[np.float64] = None
    xc: npt.NDArray[np.float64] = None
    yc: npt.NDArray[np.float64] = None
    zt: npt.NDArray[np.float64] = None
    dx: npt.NDArray[np.float64] = None
    dy: npt.NDArray[np.float64] = None
    area: npt.NDArray[np.float64] = None  # used for computing gradient
    lonc1D: npt.NDArray[np.float64] = None
    latc1D: npt.NDArray[np.float64] = None
    lont1D: npt.NDArray[np.float64] = None
    latt1D: npt.NDArray[np.float64] = None
    latt1D_fine: npt.NDArray[np.float64] = None
    en_e: npt.NDArray[np.float64] = None
    en_n: npt.NDArray[np.float64] = None
    edge_w: npt.NDArray[np.float64] = None
    edge_e: npt.NDArray[np.float64] = None
    edge_s: npt.NDArray[np.float64] = None
    edge_n: npt.NDArray[np.float64] = None
    vlon_t: npt.NDArray[np.float64] = None
    vlat_t: npt.NDArray[np.float64] = None
    cosrot: npt.NDArray[np.float64] = None
    sinrot: npt.NDArray[np.float64] = None
    weight: npt.NDArray[np.float64] = None
    cell_area: npt.NDArray[np.float64] = None  # cell area
    weight_exist: int = None
    rotate: int = None
    domain: Type[domain2d] = None

    @classmethod
    def from_file(cls, file_path: str):
        with xr.open_dataset(file_path) as ds:
            return cls(
                is_cyclic = ds.is_cyclic.values.item(),
                is_tripolar = ds.is_tripolar.values.item(),
                halo = ds.halo.values.item(),
                nx = ds.nx.values.item(),
                ny = ds.ny.values.item(),
                nx_fine = ds.nx_fine.values.item(),
                ny_fine = ds.ny_fine.values.item(),
                isc = ds.isc.values.item(),
                iec = ds.iec.values.item(),
                jsc = ds.jsc.values.item(),
                jec = ds.jec.values.item(),
                nxc = ds.nxc.values.item(),
                nyc = ds.nyc.values.item(),
                lonc = ds.lonc.values,
                latc = ds.latc.values,
                lont = ds.lont.values,
                latt = ds.latt.values,
                xt = ds.xt.values,
                yt = ds.yt.values,
                xc = ds.xc.values,
                yc = ds.yc.values,
                zt = ds.zt.values,
                dx = ds.dx.values,
                dy = ds.dy.values,
                area = ds.area.values,
                lonc1D = ds.lonc1D.values,
                latc1D = ds.latc1D.values,
                lont1D = ds.lont1D.values,
                latt1D = ds.latt1d.values,
                latt1D_fine = ds.latt1d_fine.values,
                en_e = ds.en_e.values,
                en_n = ds.en_n.values,
                edge_w = ds.edge_w.values,
                edge_e = ds.edge_e.values,
                edge_s = ds.edge_s.values,
                edge_n = ds.edge_n.values,
                vlon_t = ds.vlon_t.values,
                vlat_t = ds.vlat_t.values,
                cosrot = ds.cosrot.values,
                sinrot = ds.sinrot.values,
                weight = ds.weight.values,
                cell_area = ds.cell_area.values,
                weight_exist = ds.weight_exist.values.item(),
                rotate = ds.rotate.value.item(),
            )
        
# Adapted from tools/fregrid/fregrid_util.c
    
    def get_grid_by_size(
            self, lonbegin: float, lonend: float, latbegin: float, latend: float,
            nlon: int, nlat: int, finer_steps: int, center_y: int, opcode: str     
    ):
        layout = np.array(shape=2, dtype=int)
        self.nx = nlon
        self.ny = nlat
        self.nx_fine = (finer_steps**2)*nlon
        self.ny_fine = (finer_steps**2)*(nlat-1)+1
        nx_fine = self.nx_fine
        ny_fine = self.ny_fine
        lon_range = lonend - lonbegin
        lat_range = latend - latbegin
        self.is_tripolar = 0
        self.lont1D = np.zeros(shape=nlon, dtype=np.float64)
        self.latt1D = np.zeros(shape=nlat, dtype=np.float64)
        self.lonc1D = np.zeros(shape=nlon+1, dtype=np.float64)
        self.latc1D = np.zeros(shape=nlat+1, dtype=np.float64)

        dlon = lon_range/nlon
        for i in range(nlon):
            self.lont1D[i] = (lonbegin + (i +0.5)*dlon)*D2R
        for i in range(nlon+1):
            self.lonc1D[i] = (lonbegin + i*dlon)*D2R

        layout[0] = 1
        layout[1] = mpp_npes()
        GridStruct.mpp_define_domains2d(self.nx, self.ny, layout, 0, 0, self.domain)
        GridStruct.mpp_get_compute_domains2d(self.domain, self.isc, self.iec, self.jsc, self.jec)
        self.nxc = self.iec - self.isc + 1
        self.nyc = self.jec - self.jsc + 1
        nxc = self.nxc
        nyc = self.nyc
        if center_y:
            dlat = lat_range/nlat
            for j in range(nlat):
                self.latt1D[j] = (latbegin + (j + 0.5) * dlat) * D2R
            for j in range(nlat+1):
                self.latc1D[j] = (latbegin + j * dlat) * D2R
        else:
            dlat = lat_range/(nlat + 1)
            for j in range(nlat):
                self.latt1D[j] = (latbegin + j * dlat) * D2R
            for j in range(nlat+1):
                self.latc1D[j] = (latbegin + (j - 0.5) * dlat) * D2R

        if opcode == "bilinear":
            self.latt1D_fine = np.zeros(shape=ny_fine, dtype=np.float64)
            self.lont = np.zeros(shape=nx_fine*ny_fine, dtype=np.float64)
            self.latt = np.zeros(shape=nx_fine*ny_fine, dtype=np.float64)
            self.xt = np.zeros(shape=nx_fine*ny_fine, dtype=np.float64)
            self.yt = np.zeros(shape=nx_fine*ny_fine, dtype=np.float64)
            self.zt = np.zeros(shape=nx_fine*ny_fine, dtype=np.float64)
            self.vlon_t = np.zeros(shape=3*nx_fine*ny_fine, dtype=np.float64)
            self.vlat_t = np.zeros(shape=3*nx_fine*ny_fine, dtype=np.float64)

            dlon = lon_range/nx_fine
            for i in range(nx_fine):
                lon_fine = (lonbegin + (i + 0.5) * dlon) * D2R
                for j in range(ny_fine):
                    self.lont[j*nx_fine+i] = lon_fine

            if center_y:
                dlat = lat_range/ny_fine
                for j in range(ny_fine):
                    self.latt1D_fine[j] = (latbegin + (j + 0.5) * dlat) * D2R
            else:
                dlat = lat_range/(ny_fine - 1)
                for j in range(ny_fine):
                    self.latt1D_fine[j] = (latbegin + j * dlat) * D2R
            
            for j in range(ny_fine):
                for i in range(nx_fine):
                    self.latt[j*nx_fine+i] = self.latt1D_fine[j]

            GridStruct.latlon2xyz(nx_fine*ny_fine, self.lont, self.latt, self.xt, self.yt, self.zt)

            GridStruct.unit_vect_latlon(nx_fine*ny_fine, self.lont, self.latt, self.vlon_t, self.vlat_t)

        self.lonc = np.zeros(shape=(nxc+1)*(nyc+1), dtype=np.float64)
        self.latc = np.zeros(shape=(nxc+1)*(nyc+1), dtype=np.float64)
        for j in range(nyc):
            jj = j + self.jsc
            for i in range(nxc):
                ii = i + self.isc
                self.lonc[j*(nxc+1)+i] = self.lonc1D[ii]
                self.latc[j*(nxc+1)+i] = self.latc1D[jj]
        if opcode and 8:
            self.rotate = 0



# These can be removed and use the C-based versions, they were just easy to port and thought these were a good place for them

    @staticmethod
    def latlon2xyz(size: int, lon: npt.NDArray, lat: npt.NDArray, x: npt.NDArray, y: npt.NDArray, z: npt.NDArray):
        for n in range(size):
            x[n] = cos(lat[n]) * cos(lon[n])
            y[n] = cos(lat[n]) * sin(lon[n])
            z[n] = sin(lat[n])

    @staticmethod
    def unit_vect_latlon(size: int, lon: npt.NDArray, lat: npt.NDArray, vlon: npt.NDArray, vlat: npt.NDArray):
        for n in range(size):
            sin_lon = sin(lon[n])
            cos_lon = cos(lon[n])
            sin_lat = sin(lat[n])
            cos_lat = cos(lat[n])

            vlon[3*n] = -sin_lon
            vlon[3*n+1] = cos_lon
            vlon[3*n+2] = 0.0

            vlat[3*n] = -sin_lat * cos_lon
            vlat[3*n+1] = -sin_lat * sin_lon
            vlat[3*n+2] = cos_lat

    @staticmethod
    def compute_extent(npts: int, ndivs: int, ibegin: npt.NDArray, iend: npt.NDArray):
        ndivs_is_odd = ndivs%2
        npts_is_odd = npts%2
        symmetrize = 0
        if ndivs_is_odd and npts_is_odd:
            symmetrize = 1
        if ndivs_is_odd == 0 and npts_is_odd == 0:
            symmetrize = 1
        if ndivs_is_odd and npts_is_odd == 0 and ndivs < npts/2:
            symmetrize = 1

        isg = 0
        ieg = npts - 1
        iss = isg
        for ndiv in range(ndivs):
            if ndiv == 0:
                imax = ieg
                ndmax = ndivs
            if ndiv < (ndivs - 1)/2 + 1:
                ie = iss + ceil((imax - iss + 1.0)/(ndmax - ndiv)) - 1
                ndmirror = (ndivs - 1) - ndiv
                if ndmirror > ndiv and symmetrize:
                    ibegin[ndmirror] = max(isg + ieg - ie, ie + 1)
                    iend[ndmirror] = max(isg + ieg - iss, ie + 1)
                    imax = ibegin[ndmirror] - 1
                    ndmax -= 1
            else:
                if symmetrize:
                    iss = ibegin[ndiv]
                    ie = iend[ndiv]
                else:
                    ie = iss + ceil((imax - iss + 1.0)/(ndmax - ndiv)) - 1
            
            ibegin[ndiv] = iss
            iend[ndiv] = ie
            iss = ie + 1

    @staticmethod
    def define_domain1d(npts: int, ndivs: int, domain: Type[domain1d]):
        domain.beglist = np.zeros(shape=ndivs, dtype=int)
        domain.endlist = np.zeros(shape=ndivs, dtype=int)

        GridStruct.compute_extent(npts, ndivs, domain.beglist, domain.endlist)

        npes = mpp_npes()
        pe = mpp_pe()

        if npes == ndivs:
            domain.start = domain.beglist[pe]
            domain.end = domain.endlist[pe]
            domain.size = domain.end - domain.start + 1
            domain.sizeg = npts

    @staticmethod
    def define_domain2d(ni: int, nj: int, layout: npt.NDArray, xhalo: int, yhalo: int, domain: Type[domain2d]):
        domx = domain1d()
        domy = domain1d()

        domain.isclist = np.zeros(shape=layout[0]*layout[1], dtype=int)
        domain.ieclist = np.zeros(shape=layout[0]*layout[1], dtype=int)
        domain.jsclist = np.zeros(shape=layout[0]*layout[1], dtype=int)
        domain.jeclist = np.zeros(shape=layout[0]*layout[1], dtype=int)

        GridStruct.define_domain1d(ni, layout[0], domx)
        GridStruct.define_domain1d(nj, layout[1], domy)

        n = 0
        for j in range(layout[1]):
            for i in range(layout[0]):
                domain.isclist[n] = domx.beglist[i] + xhalo
                domain.ieclist[n] = domx.endlist[i] + xhalo
                domain.jsclist[n] = domy.beglist[j] + yhalo
                domain.jeclist[n] = domy.endlist[j] + yhalo
                n += 1

        pe = mpp_pe()

        domain.xhalo = xhalo
        domain.yhalo = yhalo
        domain.isc = domain.isclist[pe]
        domain.iec = domain.ieclist[pe]
        domain.jsc = domain.jsclist[pe]
        domain.jec = domain.jeclist[pe]
        domain.isd = domain.isc - xhalo
        domain.ied = domain.iec + xhalo
        domain.jsd = domain.jsc - yhalo
        domain.jed = domain.jec + yhalo
        domain.nxc = domain.iec - domain.isc + 1
        domain.nyc = domain.jec - domain.jsc + 1
        domain.nxd = domain.ied - domain.isd + 1
        domain.nyd = domain.jed - domain.jsd + 1
        domain.nxg = ni
        domain.nyg = nj

    
