import numpy as np
import pyproj
from pyproj.crs.crs import CRS
import rasterio
import xarray as xr
import pandas as pd
import geopandas as gpd
from datetime import datetime
from configparser import ConfigParser
from shapely.geometry import LineString
from typing import List, Dict, Union, Tuple
from pathlib import Path
import io
import copy
import logging
import hydromt
from hydromt.io import write_xy
from scipy import ndimage

__all__ = [
    "read_inp",
    "write_inp",
    "read_binary_map",
    "write_binary_map",
    "read_binary_map_index",
    "write_binary_map_index",
    "read_ascii_map",
    "write_ascii_map",
    "read_timeseries",
    "write_timeseries",
    "read_xy",
    "write_xy",
    "read_structures",
    "write_structures",
    "read_sfincs_map_results",
    "read_sfincs_his_results",
    "mask_bounds",
]

logger = logging.getLogger(__name__)


## CONFIG: sfincs.inp ##


class ConfigParserSfincs(ConfigParser):
    def __init__(self, **kwargs):
        defaults = dict(
            comment_prefixes=("!", "/", "#"),
            inline_comment_prefixes=("!"),
            allow_no_value=True,
            delimiters=("="),
        )
        defaults.update(**kwargs)
        super(ConfigParserSfincs, self).__init__(**defaults)

    def read_file(self, f, **kwargs):
        def add_header(f, header_name="dummy"):
            """add header"""
            yield "[{}]\n".format(header_name)
            for line in f:
                yield line

        super(ConfigParserSfincs, self).read_file(add_header(f), **kwargs)

    def _write_section(self, fp, section_name, section_items, delimiter):
        """Write a single section to the specified `fp'."""
        for key, value in section_items:
            value = self._interpolation.before_write(self, section_name, key, value)
            fp.write("{:<15} {:<1} {:<}\n".format(key, self._delimiters[0], value))
        fp.write("\n")


def read_inp(fn: Union[str, Path]) -> Dict:
    """Read sfincs.inp file and parse to dictionary."""
    return hydromt.config.configread(
        fn, abs_path=False, cf=ConfigParserSfincs, noheader=True
    )


def write_inp(fn: Union[str, Path], conf: Dict) -> None:
    """Write sfincs.inp file from dictionary."""
    return hydromt.config.configwrite(fn, conf, cf=ConfigParserSfincs, noheader=True)


def get_spatial_attrs(config: Dict, crs: Union[int, CRS] = None, logger=logger):
    """Returns geospatial attributes shape, crs and transform from config dict.

    The config dict should contain the following keys:

    * for shape: mmax, nmax
    * for crs: epsg
    * for transform: dx, dy, x0, y0, (rotation)

    NOTE: Rotation != 0 is not yet supported.

    Parameters
    ----------
    config: Dict
        sfincs.inp configuration
    crs: int, CRS
        Coordinate reference system

    Returns
    -------
    shape: tuple of int
        width, height
    transform: Affine.transform
        Geospatial transform
    crs: pyproj.CRS, None
        Coordinate reference system
    """
    # retrieve rows and cols
    cols = config.get("mmax")
    rows = config.get("nmax")
    if cols is None or rows is None:
        raise ValueError('"mmax" or "nmax" not defined in sfincs.inp')

    # retrieve CRS
    if crs is None and "epsg" in config:
        crs = pyproj.CRS.from_epsg(int(config.get("epsg")))
    elif crs is not None:
        crs = pyproj.CRS.from_user_input(crs)
    else:
        logger.warning('"epsg" code not defined in sfincs.inp, unknown CRS.')

    # retrieve spatial transform
    dx = config.get("dx")
    dy = config.get("dy")
    west = config.get("x0")
    south = config.get("y0")
    rotdeg = config.get("rotation", 0)  # clockwise rotation [degrees]
    if west is None or south is None:
        logger.warning(
            'Either one of "x0" or "y0" not defined in sfincs.inp, '
            "falling back to origin at (0, 0)."
        )
        west, south = 0, 0
    if dx is None or dy is None:
        logger.warning(
            'Either one of "dx" or "dy" not defined in sfincs.inp, '
            "falling back unity resolution (1, 1)."
        )
        dx, dy = 1, 1
    if rotdeg != 0:
        raise NotImplementedError("Rotated grids cannot be parsed yet.")
        # TODO: extend to use rotated grids with rotated affine
        # # code below generates a 2D coordinate grids.
        # xx = np.linspace(0, dx * (cols - 1), cols)
        # yy = np.linspace(0, dy * (rows - 1), rows)
        # xi, yi = np.meshgrid(xx, yy)
        # rot = rotdeg * np.pi / 180
        # # xgrid and ygrid not used for now
        # xgrid = x0 + np.cos(rot) * xi - np.sin(rot) * yi
        # ygrid = y0 + np.sin(rot) * xi + np.cos(rot) * yi
        # ...
    transform = rasterio.transform.from_origin(west, south, dx, -dy)

    return (rows, cols), transform, crs


## BINARY MAPS: sfincs.ind, sfincs.msk, sfincs.dep etc. ##


def write_binary_map_index(fn_ind: Union[str, Path], msk: np.ndarray) -> None:
    """Write flat index of binary map file.

    NOTE: The array should be in S->N and W->E orientation, with origin in the SW corner.

    Parameters
    ----------
    fn_ind: str, Path
        Path to output map index file.
    msk: np.ndarray
        2D array of sfincs mask map, where invalid cells have value 0.
    """
    # the index number file of sfincs starts with the length of the index numbers
    indices = np.where(msk.transpose().flatten() > 0)[0] + 1  # convert to 1-based index
    indices_ = np.array(np.hstack([np.array(len(indices)), indices]), dtype="u4")
    indices_.tofile(fn_ind)


def read_binary_map_index(fn_ind: Union[str, Path]) -> np.ndarray:
    """Read binary map index file.

    Parameters
    ----------
    fn_ind: str, Path
        Path to map index file.

    Returns
    -------
    ind: np.ndarray
        1D array of flat index of binary maps.
    """
    _ind = np.fromfile(fn_ind, dtype="u4")
    ind = _ind[1:] - 1  # convert to zero based index
    assert _ind[0] == ind.size
    return ind


def write_binary_map(
    fn: Union[str, Path],
    data: np.ndarray,
    msk: np.ndarray,
    dtype: Union[str, np.dtype] = "f4",
) -> None:
    """Write binary map file.

    NOTE: The array should be in S->N and W->E orientation, with origin in the SW corner.

    Parameters
    ----------
    fn str, Path
        Path to output map index file.
    data: np.ndarray
        2D array of sfincs map.
    msk: np.ndarray
        2D array of sfincs mask map, where invalid cells have value 0.
    dtype: str, np.dtype, optional
        Data type, by default "f4". For sfincs.msk file use dtype="u1".
    """
    data_out = np.asarray(data.transpose()[msk.transpose() > 0], dtype=dtype)
    data_out.tofile(fn)


def read_binary_map(
    fn: Union[str, Path],
    ind: np.ndarray,
    shape: Tuple[int],
    mv: float = -9999.0,
    dtype: str = "f4",
) -> np.ndarray:
    """Read binary map.

    Parameters
    ----------
    fn: str, Path
        Path to map file.
    ind: np.ndarray
        1D array of flat index of binary maps.
    shape: tuple of int
        (nrow, ncol) shape of output map.
    mv: int or float
        missing value, by default -9999.0.
    dtype: str, np.dtype, optional
        Data type, by default "f4". For sfincs.msk file use dtype="u1".

    Returns
    -------
    ind: np.ndarray
        1D array of flat index of binary maps.
    """
    assert ind.max() <= np.multiply(*shape)
    nrow, ncol = shape
    data = np.full((ncol, nrow), mv, dtype=dtype)
    data.flat[ind] = np.fromfile(fn, dtype=dtype)
    data = data.transpose()
    return data


## ASCII maps: sfincs.restart ##


def read_ascii_map(fn: Union[str, Path]) -> np.ndarray:
    """Read ascii map

    Parameters
    ----------
    fn : str, Path
        Path to ascii map file.

    Returns
    -------
    data : np.ndarray
        2D array of sfincs map.
    """
    data = np.loadtxt(fn).astype(np.float32)
    return data


def write_ascii_map(fn: Union[str, Path], data: np.ndarray, fmt: str = "%8.3f") -> None:
    """Write ascii map

    NOTE: The array should be in S->N and W->E orientation, with origin in the SW corner.

    Parameters
    ----------
    fn : str, Path
        Path to ascii map file.
    data : np.ndarray
        2D array of sfincs map.
    fmt : str, optional
        Value format, by default "%8.3f". See numpy.savetxt for more options.
    """
    with open(fn, "w") as f:
        np.savetxt(f, data, fmt=fmt)


## XY files: bnd / src ##
# write_xy defined in hydromt.io


def read_xy(fn: Union[str, Path], crs: Union[int, CRS] = None) -> gpd.GeoDataFrame:
    """Read sfincs xy files and parse to GeoDataFrame.

    Parameters
    ----------
    fn : str, Path
        Path to ascii xy file.
    crs: int, CRS
        Coordinate reference system

    Returns
    -------
    gdf: gpd.GeoDataFrame
        GeoDataFrame with point geomtries
    """
    gdf = hydromt.open_vector(fn, crs=crs, driver="xy")
    gdf.index = np.arange(1, gdf.index.size + 1, dtype=int)  # index starts at 1
    return gdf


## ASCII TIMESERIES: bzs / dis / precip ##


def parse_datetime(dt: Union[str, datetime], format="%Y%m%d %H%M%S") -> datetime:
    """Checks and/or parses datetime from a string, default sfincs datetime string format"""
    if isinstance(dt, str):
        dt = datetime.strptime(dt, format)
    elif not isinstance(dt, datetime):
        raise ValueError(f"Unknown type for datetime: {type(dt)})")
    return dt


def read_timeseries(fn: Union[str, Path], tref: Union[str, datetime]) -> pd.DataFrame:
    """Read ascii timeseries files such as sfincs.bzs, sfincs.dis and sfincs.precip.
    The first column (time index) is parsed to datetime format assumming it represents
    seconds from `tref`.

    Parameters
    ----------
    fn: str, Path
        Path to output timeseries file.
    tref: datetime.datetime, str
        Datetime of tref, string in "%Y%m%d %H%M%S" format.

    Returns
    -------
    df: pd.DataFrame
        Dataframe of timeseries with parsed time index.
    """
    tref = parse_datetime(tref)
    df = pd.read_csv(fn, delim_whitespace=True, index_col=0, header=None)
    df.index = pd.to_datetime(df.index.values, unit="s", origin=tref)
    df.columns = df.columns.values.astype(int)
    df.index.name = "time"
    df.columns.name = "index"
    return df


def write_timeseries(
    fn: Union[str, Path],
    df: pd.DataFrame,
    tref: Union[str, datetime],
    fmt: str = "%7.2f",
) -> None:
    """Write pandas.DataFrame to fixed width ascii timeseries files
    such as sfincs.bzs, sfincs.dis and sfincs.precip. The output time index is given in
    seconds from tref.

    Parameters
    ----------
    fn: str, Path
        Path to output timeseries file.
    df: pd.DataFrame
        Dataframe of timeseries.
    tref: datetime.datetime, str
        Datetime of tref, string in "%Y%m%d %H%M%S" format.
    fmt: str, optional
        Output value format, by default "%7.2f".
    """
    tref = parse_datetime(tref)
    if df.index.size == 0:
        raise ValueError("df does not contain data.")
    data = df.reset_index().values
    data[:, 0] = (df.index - tref).total_seconds()
    # calculate required width for time column; hard coded single decimal precision
    # format for other columns is based on fmt`argument
    w = int(np.floor(np.log10(data[-1, 0]))) + 3
    fmt_lst = [f"%{w}.1f"] + [fmt for _ in range(df.columns.size)]
    fmt_out = " ".join(fmt_lst)
    with open(fn, "w") as f:
        np.savetxt(f, data, fmt=fmt_out)


## MASK


def mask_bounds(
    da_mask: xr.DataArray,
    gdf_include: gpd.GeoDataFrame = None,
    gdf_exclude: gpd.GeoDataFrame = None,
    structure: np.ndarray = np.ones((3, 3)),
) -> xr.DataArray:
    """Returns the boundary cells based of values greater than zero in da_mask.
    If provided the bounds are limited to cells within gdf_include and outside gdf_exclude.

    Parameters
    ----------
    da_mask: xr.DataArray
        Model mask.
    gdf_include, gdf_exclude: geopandas.GeoDataFrame
        Geometries with areas to include/exclude from the model boundary.

    Returns
    -------
    bounds: xr.DataArray
        Boolean mask of model boundary cells.
    """
    bounds = np.logical_xor(
        da_mask != 0, ndimage.binary_erosion(da_mask, structure=structure)
    )
    if gdf_include is not None:
        da_include = da_mask.raster.geometry_mask(gdf_include)
        bounds = bounds.where(da_include, False)
    if gdf_exclude is not None:
        da_exclude = da_mask.raster.geometry_mask(gdf_exclude)
        bounds = bounds.where(~da_exclude, False)
    return bounds


## STRUCTURES: thd / weir ##


def gdf2structures(gdf: gpd.GeoDataFrame) -> List[Dict]:
    """Convert GeoDataFrame[LineString] to list of structure dictionaries

    The x,y are taken from the geometry.
    For weir structures to additional paramters are required, a "z" (elevation) and
    "par1" (Cd coefficient in weir formula) are required which should be supplied
    as columns (or z-coordinate) of the GeoDataFrame. These columns should either
    contain a float or 1D-array of floats with same length as the LineString.

    Parameters
    ----------
    gdf: geopandas.GeoDataFrame with LineStrings geometries
        GeoDataFrame structures.

    Returns
    -------
    feats: list of dict
        List of dictionaries describing structures.
    """
    feats = []
    for _, item in gdf.iterrows():
        feat = item.drop("geometry").dropna().to_dict()
        # check geom
        line = item.geometry
        if line.type == "MultiLineString" and len(line) == 1:
            line = line[0]
        if line.type != "LineString":
            raise ValueError("Invalid geometry type, only LineString is accepted.")
        xyz = tuple(zip(*line.coords[:]))
        feat["x"], feat["y"] = list(xyz[0]), list(xyz[1])
        if len(xyz) == 3:
            feat["z"] = list(xyz[2])
        feats.append(feat)
    return feats


def structures2gdf(feats: List[Dict], crs: Union[int, CRS] = None) -> gpd.GeoDataFrame:
    """Convert list of structure dictionaries to GeoDataFrame[LineString]

    Parameters
    ----------
    feats: list of dict
        List of dictionaries describing structures.
    crs: int, CRS
        Coordinate reference system

    Returns
    -------
    gdf: geopandas.GeoDataFrame
        GeoDataFrame structures
    """
    records = []
    for f in feats:
        feat = copy.deepcopy(f)
        xyz = [feat.pop("x"), feat.pop("y")]
        if "z" in feat and np.atleast_1d(feat["z"]).size == len(xyz[0]):
            xyz.append(feat.pop("z"))
        feat.update({"geometry": LineString(list(zip(*xyz)))})
        records.append(feat)
    gdf = gpd.GeoDataFrame.from_records(records)
    if crs is not None:
        gdf.set_crs(crs, inplace=True)
    return gdf


def write_structures(
    fn: Union[str, Path], feats: List[Dict], stype: str = "thd", fmt="%.1f"
) -> None:
    """Write list of structure dictionaries to file

    Parameters
    ----------
    fn: str, Path
        Path to output structure file.
    feats: list of dict
        List of dictionaries describing structures.
        For thd files "x" and "y" are required, "name" is optional.
        For weir files "x", "y" and "z" are required, "name" and "par1" are optional.
    stype: {'thd', 'weir'}
        Structure type thin dams (thd) or weirs (weir).
    fmt: str
        format for "z" and "par1" fields.

    Examples
    --------
    >>> feats = [
            {
                "name": 'WEIR01',
                "x": [0, 10, 20],
                "y": [100, 100, 100],
                "z": 5.0,
                "par1": 0.6,
            },
            {
                "name": 'WEIR02',
                "x": [100, 110, 120],
                "y": [100, 100, 100],
                "z": [5.0, 5.1, 5.0],
                "par1": 0.6,
            },
        ]
    >>> write_structures('sfincs.weir', feats, stype='weir')
    """
    cols = {"thd": 2, "weir": 4}[stype.lower()]
    fmt = ["%.0f", "%.0f"] + [fmt for _ in range(cols - 2)]
    if stype.lower() == "weir" and np.any(["z" not in f for f in feats]):
        raise ValueError('"z" value missing for weir files.')
    with open(fn, "w") as f:
        for i, feat in enumerate(feats):
            name = feat.get("name", i + 1)
            if isinstance(name, int):
                name = f"{stype:s}{name:02d}"
            rows = len(feat["x"])
            a = np.zeros((rows, cols), dtype=np.float32)
            a[:, 0] = np.asarray(feat["x"]).round(0)
            a[:, 1] = np.asarray(feat["y"]).round(0)
            if stype.lower() == "weir":
                a[:, 2] = feat["z"]
                a[:, 3] = feat.get("par1", 0.6)
            s = io.BytesIO()
            np.savetxt(s, a, fmt=fmt)
            f.write(f"{name}\n")
            f.write(f"{rows:d} {cols:d}\n")
            f.write(s.getvalue().decode())


def read_structures(fn: Union[str, Path]) -> List[Dict]:
    """Read structure files to list of dictionaries.

    Parameters
    ----------
    fn : str, Path
        Path to structure file.

    Returns
    -------
    feats: list of dict
        List of dictionaries describing structures.
    """
    feats = []
    col_names = ["x", "y", "z", "par1"]
    with open(fn, "r") as f:
        while True:
            name = f.readline().strip()
            if not name:  # EOF
                break
            feat = {"name": name}
            rows, cols = [int(v) for v in f.readline().strip().split(maxsplit=2)]
            for c in range(cols):
                feat[col_names[c]] = [0.0 for _ in range(rows)]
            for r in range(rows):
                for c, v in enumerate(f.readline().strip().split(maxsplit=cols)):
                    feat[col_names[c]][r] = float(v)
            if cols > 2:
                for c in col_names[2:]:
                    if np.unique(feat[c]).size == 1:
                        feat[c] = feat[c][0]
            feats.append(feat)
    return feats


## OUTPUT: sfincs_map.nc, sfincs_his.nc ##


def read_sfincs_map_results(
    fn_map: Union[str, Path],
    hmin: float = 0.0,
    crs: Union[int, CRS] = None,
    chunksize: int = 100,
    drop: List[str] = ["crs", "sfincsgrid"],
    logger=logger,
    **kwargs,
) -> Tuple[xr.Dataset]:
    """Read sfincs_map.nc staggered grid netcdf files and parse to two
    hydromt.RasterDataset objects: one with face and one with edge variables.

    Additionally, hmax is computed from zsmax and zb if present.

    Parameters
    ----------
    fn_map : str, Path
        Path to sfincs_map.nc file
    hmin: float, optional
        Minimum water depth to consider in hmax map, i.e. cells with lower depth
        get a nodata values assigned. By deafult 0.0
    crs: int, CRS
        Coordinate reference system
    chunksize: int, optional
        chunk size along time dimension, by default 100
    drop : List[str], optional
        Variables to drop from reading, by default ["crs", "sfincsgrid"]

    Returns
    -------
    ds_face, ds_edge: hydromt.RasterDataset
        Parsed SFINCS output map file
    """

    ds_map = xr.open_dataset(fn_map, chunks={"time": chunksize}, **kwargs)
    ds_map = ds_map.set_coords(("x", "y", "edge_x", "edge_y"))
    crs = ds_map["crs"].item() if ds_map["crs"].item() != 0 else crs

    if ds_map["inp"].attrs.get("rotation") != 0:
        logger.warning("Cannot parse rotated maps. Skip reading sfincs.map.nc")
        return xr.Dataset(), xr.Dataset()

    # split general+face and edge vars
    dvars = list(ds_map.data_vars.keys())
    face_vars = [v for v in dvars if "edge_m" not in ds_map[v].dims and v not in drop]
    edge_vars = [v for v in dvars if "edge_m" in ds_map[v].dims and v not in drop]

    # read face vars
    face_coords = {
        "x": xr.IndexVariable("x", ds_map["x"].isel(n=0).values),
        "y": xr.IndexVariable("y", ds_map["y"].isel(m=0).values),
    }
    ds_face = (
        ds_map[face_vars]
        .drop(["x", "y"])
        .rename({"n": "y", "m": "x"})
        .assign_coords(face_coords)
        .transpose(..., "y", "x")
    )
    # compute hmax
    if "zsmax" in ds_face:
        logger.info('Computing "hmax = max(zsmax) - zb"')
        hmax = ds_face["zsmax"].max("timemax") - ds_face["zb"]
        hmax = hmax.where(hmax > hmin, -9999)
        hmax.raster.set_nodata(-9999)
        ds_face["hmax"] = hmax
    # set spatial attrs
    ds_face.raster.set_spatial_dims(x_dim="x", y_dim="y")
    ds_face.raster.set_crs(crs)

    # get edge vars
    ds_edge = xr.Dataset()
    if len(edge_vars) > 0:
        edge_coords = {
            "edge_x": xr.IndexVariable(
                "edge_x", ds_map["edge_x"].isel(edge_n=0).values
            ),
            "edge_y": xr.IndexVariable(
                "edge_y", ds_map["edge_y"].isel(edge_m=0).values
            ),
        }
        ds_edge = (
            ds_map[edge_vars]
            .drop_vars(["edge_x", "edge_y"])
            .rename({"edge_n": "edge_y", "edge_m": "edge_x"})
            .assign_coords(edge_coords)
            .transpose(..., "edge_y", "edge_x")
        )
        ds_edge.raster.set_spatial_dims(x_dim="edge_x", y_dim="edge_y")
        ds_edge.raster.set_crs(crs)

    return ds_face, ds_edge


def read_sfincs_his_results(
    fn_his: Union[str, Path],
    crs: Union[int, CRS] = None,
    chunksize: int = 100,
    **kwargs,
) -> xr.Dataset:
    """Read sfincs_his.nc point timeseries netcdf file and parse to hydromt.GeoDataset object.

    Parameters
    ----------
    fn_his : str, Path
        Path to sfincs_his.nc file
    crs: int, CRS
        Coordinate reference system
    chunksize: int, optional
        chunk size along time dimension, by default 100

    Returns
    -------
    ds_his: xr.Dataset
        Parsed SFINCS output his file.
    """

    ds_his = xr.open_dataset(fn_his, chunks={"time": chunksize}, **kwargs)
    crs = ds_his["crs"].item() if ds_his["crs"].item() != 0 else crs
    dvars = list(ds_his.data_vars.keys())
    # set coordinates & spatial dims
    cvars = ["id", "name", "x", "y"]
    ds_his = ds_his.set_coords([v for v in dvars if v.split("_")[-1] in cvars])
    ds_his.vector.set_spatial_dims(
        x_dim="station_x", y_dim="station_y", index_dim="stations"
    )
    # set crs
    ds_his.vector.set_crs(crs)

    return ds_his
