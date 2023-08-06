# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import datetime
import logging

import eccodes

from climetlab.core import Base

# from climetlab.decorators import dict_args
from climetlab.utils.bbox import BoundingBox

from . import Reader

LOG = logging.getLogger(__name__)

# return eccodes.codes_new_from_file(self.file, eccodes.CODES_PRODUCT_GRIB)

# See https://pymotw.com/2/weakref/


class CodesHandle:
    def __init__(self, handle, path, offset):
        self.handle = handle
        self.path = path
        self.offset = offset

    def __del__(self):
        eccodes.codes_release(self.handle)

    def get(self, name):
        try:
            if name == "values":
                return eccodes.codes_get_values(self.handle)
            if name in ("distinctLatitudes", "distinctLongitudes"):
                return eccodes.codes_get_double_array(self.handle, name)
            return eccodes.codes_get(self.handle, name)
        except eccodes.KeyValueNotFoundError:
            return None


class CodesReader:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path, "rb")

    def __del__(self):
        try:
            self.file.close()
        except Exception:
            pass

    def at_offset(self, offset):
        self.file.seek(offset, 0)
        return self.__next__()

    def __iter__(self):
        return self

    def __next__(self):
        offset = self.file.tell()
        handle = eccodes.codes_new_from_file(self.file, eccodes.CODES_PRODUCT_GRIB)
        if not handle:
            raise StopIteration()
        return CodesHandle(handle, self.path, offset)

    @property
    def offset(self):
        return self.file.tell()


def cb(r):
    print("Delete", r)


class GribField(Base):
    def __init__(self, *, handle=None, reader=None, offset=None):
        self._handle = handle
        self._reader = reader
        self._offset = offset

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def path(self):
        return self.handle.path

    @property
    def handle(self):
        if self._handle is None:
            assert self._offset is not None
            assert self._reader is not None
            self._handle = self._reader.at_offset(self._offset)
        return self._handle

    @property
    def values(self):
        return self.handle.get("values")

    @property
    def offset(self):
        if self._offset is None:
            self._offset = int(self.handle.get("offset"))
        return self._offset

    @property
    def shape(self):
        return self.handle.get("Nj"), self.handle.get("Ni")

    def plot_map(self, driver):
        driver.bounding_box(
            north=self.handle.get("latitudeOfFirstGridPointInDegrees"),
            south=self.handle.get("latitudeOfLastGridPointInDegrees"),
            west=self.handle.get("longitudeOfFirstGridPointInDegrees"),
            east=self.handle.get("longitudeOfLastGridPointInDegrees"),
        )
        driver.plot_grib(self.path, self.handle.get("offset"))

    def to_numpy(self):
        return self.values.reshape(self.shape)

    def __repr__(self):
        return "GribField(%s,%s,%s,%s,%s,%s)" % (
            self.handle.get("shortName"),
            self.handle.get("levelist"),
            self.handle.get("date"),
            self.handle.get("time"),
            self.handle.get("step"),
            self.handle.get("number"),
        )

    def _grid_definition(self):
        return dict(
            north=self.handle.get("latitudeOfFirstGridPointInDegrees"),
            south=self.handle.get("latitudeOfLastGridPointInDegrees"),
            west=self.handle.get("longitudeOfFirstGridPointInDegrees"),
            east=self.handle.get("longitudeOfLastGridPointInDegrees"),
            south_north_increment=self.handle.get("jDirectionIncrementInDegrees"),
            west_east_increment=self.handle.get("iDirectionIncrementInDegrees"),
        )

    def field_metadata(self):
        m = self._grid_definition()
        for n in ("shortName", "units", "paramId"):
            p = self.handle.get(n)
            if p is not None:
                m[n] = str(p)
        m["shape"] = self.shape
        return m

    def datetime(self):
        date = self.handle.get("date")
        time = self.handle.get("time")
        return datetime.datetime(
            date // 10000, date % 10000 // 100, date % 100, time // 100, time % 100
        )

    def valid_datetime(self):
        step = self.handle.get("endStep")
        return self.datetime() + datetime.timedelta(hours=step)

    def to_datetime_list(self):
        return [self.valid_datetime()]

    def to_bounding_box(self):
        return BoundingBox(
            north=self.handle.get("latitudeOfFirstGridPointInDegrees"),
            south=self.handle.get("latitudeOfLastGridPointInDegrees"),
            west=self.handle.get("longitudeOfFirstGridPointInDegrees"),
            east=self.handle.get("longitudeOfLastGridPointInDegrees"),
        )

    def _attributes(self, names):
        result = {}
        for name in names:
            result[name] = self.handle.get(name)
        return result


class GRIBIterator:
    def __init__(self, path):
        self.path = path
        self.reader = CodesReader(path)

    def __repr__(self):
        return "GRIBIterator(%s)" % (self.path,)

    def __next__(self):
        offset = self.reader.offset
        handle = next(self.reader)
        return GribField(handle=handle, reader=self.reader, offset=offset)

    def __iter__(self):
        return self


class GRIBFilter:
    def __init__(self, reader, filter):
        self._reader = reader
        self._filter = dict(**filter)

    def __repr__(self):
        return "GRIBFilter(%s, %s)" % (self._reader, self._filter)

    def __iter__(self):
        return GRIBIterator(self.path)


# class MultiGribReaders(GriddedMultiReaders):
#     engine = "cfgrib"
#     backend_kwargs = {"squeeze": False}


class GRIBReader(Reader):
    appendable = True  # GRIB messages can be added to the same file

    open_mfdataset_backend_kwargs = {"squeeze": False}
    open_mfdataset_engine = "cfgrib"

    def __init__(self, source, path):
        super().__init__(source, path)
        self._fields = None
        self._reader = None

    def __repr__(self):
        return "GRIBReader(%s)" % (self.path,)

    def __iter__(self):
        return GRIBIterator(self.path)

    def _items(self):
        if self._fields is None:
            self._fields = []
            for f in self:
                self._fields.append(f.offset)
        return self._fields

    def __getitem__(self, n):
        if self._reader is None:
            self._reader = CodesReader(self.path)
        return GribField(reader=self._reader, offset=self._items()[n])

    def __len__(self):
        return len(self._items())

    def to_xarray(self, **kwargs):
        return type(self).to_xarray_multi([self.path], **kwargs)

    @classmethod
    def to_xarray_multi(cls, paths, **kwargs):
        import xarray as xr

        options = dict(
            backend_kwargs={"squeeze": False},
        )
        options.update(kwargs)
        options["engine"] = "cfgrib"
        return xr.open_mfdataset(
            paths,
            **options,
        )


def reader(source, path, magic, deeper_check):
    if magic[:4] == b"GRIB":
        return GRIBReader(source, path)
