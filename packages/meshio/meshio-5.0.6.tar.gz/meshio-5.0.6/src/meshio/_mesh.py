from __future__ import annotations

import collections
import copy
import warnings

import numpy as np
from numpy.typing import ArrayLike

from ._common import num_nodes_per_cell


class CellBlock(collections.namedtuple("CellBlock", ["type", "data"])):
    def __repr__(self):
        return f"<meshio CellBlock, type: {self.type}, num cells: {len(self.data)}>"

    def __len__(self):
        return len(self.data)


class Mesh:
    def __init__(
        self,
        points: ArrayLike,
        cells: dict[str, ArrayLike] | list[tuple[str, ArrayLike] | CellBlock],
        point_data: dict[str, ArrayLike] | None = None,
        cell_data: dict[str, list[ArrayLike]] | None = None,
        field_data=None,
        point_sets: dict[str, ArrayLike] | None = None,
        cell_sets: dict[str, list[ArrayLike]] | None = None,
        gmsh_periodic=None,
        info=None,
    ):
        self.points = np.asarray(points)
        if isinstance(cells, dict):
            # Let's not deprecate this for now.
            # import warnings
            # warnings.warn(
            #     "cell dictionaries are deprecated, use list of tuples, e.g., "
            #     '[("triangle", [[0, 1, 2], ...])]',
            #     DeprecationWarning,
            # )
            # old dict, deprecated
            #
            # convert dict to list of tuples
            cells = list(cells.items())

        self.cells = []
        for cell_block in cells:
            if isinstance(cell_block, tuple):
                cell_type, data = cell_block
                self.cells.append(
                    CellBlock(
                        cell_type,
                        # polyhedron data cannot be converted to numpy
                        # arrays because the sublists don't all have the
                        # same length
                        data
                        if cell_type.startswith("polyhedron")
                        else np.asarray(data),
                    )
                )
            else:
                self.cells.append(cell_block)

        self.point_data = {} if point_data is None else point_data
        self.cell_data = {} if cell_data is None else cell_data
        self.field_data = {} if field_data is None else field_data
        self.point_sets = {} if point_sets is None else point_sets
        self.cell_sets = {} if cell_sets is None else cell_sets
        self.gmsh_periodic = gmsh_periodic
        self.info = info

        # assert point data consistency and convert to numpy arrays
        for key, item in self.point_data.items():
            self.point_data[key] = np.asarray(item)
            if len(self.point_data[key]) != len(self.points):
                raise ValueError(
                    f"len(points) = {len(self.points)}, "
                    f'but len(point_data["{key}"]) = {len(self.point_data[key])}'
                )

        # assert cell data consistency and convert to numpy arrays
        for key, data in self.cell_data.items():
            if len(data) != len(cells):
                raise ValueError(
                    "Incompatible cell data. "
                    f"{len(cells)} cell blocks, but '{key}' has {len(data)} blocks."
                )

            for k in range(len(data)):
                data[k] = np.asarray(data[k])
                if len(data[k]) != len(self.cells[k]):
                    raise ValueError(
                        "Incompatible cell data. "
                        f"Cell block {k} has length {len(self.cells[k])}, but "
                        f"corresponding cell data {key} item has length {len(data[k])}."
                    )

    def __repr__(self):
        lines = ["<meshio mesh object>", f"  Number of points: {len(self.points)}"]
        special_cells = [
            "polygon",
            "polyhedron",
            "VTK_LAGRANGE_CURVE",
            "VTK_LAGRANGE_TRIANGLE",
            "VTK_LAGRANGE_QUADRILATERAL",
            "VTK_LAGRANGE_TETRAHEDRON",
            "VTK_LAGRANGE_HEXAHEDRON",
            "VTK_LAGRANGE_WEDGE",
            "VTK_LAGRANGE_PYRAMID",
        ]
        if len(self.cells) > 0:
            lines.append("  Number of cells:")
            for cell_type, elems in self.cells:
                string = cell_type
                if cell_type in special_cells:
                    string += f"({elems.shape[1]})"
                lines.append(f"    {string}: {len(elems)}")
        else:
            lines.append("  No cells.")

        if self.point_sets:
            names = ", ".join(self.point_sets.keys())
            lines.append(f"  Point sets: {names}")

        if self.cell_sets:
            names = ", ".join(self.cell_sets.keys())
            lines.append(f"  Cell sets: {names}")

        if self.point_data:
            names = ", ".join(self.point_data.keys())
            lines.append(f"  Point data: {names}")

        if self.cell_data:
            names = ", ".join(self.cell_data.keys())
            lines.append(f"  Cell data: {names}")

        if self.field_data:
            names = ", ".join(self.field_data.keys())
            lines.append(f"  Field data: {names}")

        return "\n".join(lines)

    def copy(self):
        return copy.deepcopy(self)

    def write(self, path_or_buf, file_format: str | None = None, **kwargs):
        # avoid circular import
        from ._helpers import write

        write(path_or_buf, self, file_format, **kwargs)

    def get_cells_type(self, cell_type: str):
        if not any(c.type == cell_type for c in self.cells):
            return np.empty((0, num_nodes_per_cell[cell_type]), dtype=int)
        return np.concatenate([c.data for c in self.cells if c.type == cell_type])

    def get_cell_data(self, name: str, cell_type: str):
        return np.concatenate(
            [d for c, d in zip(self.cells, self.cell_data[name]) if c.type == cell_type]
        )

    @property
    def cells_dict(self):
        cells_dict = {}
        for cell_type, data in self.cells:
            if cell_type not in cells_dict:
                cells_dict[cell_type] = []
            cells_dict[cell_type].append(data)
        # concatenate
        for key, value in cells_dict.items():
            cells_dict[key] = np.concatenate(value)
        return cells_dict

    @property
    def cell_data_dict(self):
        cell_data_dict = {}
        for key, value_list in self.cell_data.items():
            cell_data_dict[key] = {}
            for value, (cell_type, _) in zip(value_list, self.cells):
                if cell_type not in cell_data_dict[key]:
                    cell_data_dict[key][cell_type] = []
                cell_data_dict[key][cell_type].append(value)

            for cell_type, val in cell_data_dict[key].items():
                cell_data_dict[key][cell_type] = np.concatenate(val)
        return cell_data_dict

    @property
    def cell_sets_dict(self):
        sets_dict = {}
        for key, member_list in self.cell_sets.items():
            sets_dict[key] = {}
            offsets = {}
            for members, cells in zip(member_list, self.cells):
                if members is None:
                    continue
                if cells.type in offsets:
                    offset = offsets[cells.type]
                    offsets[cells.type] += cells.data.shape[0]
                else:
                    offset = 0
                    offsets[cells.type] = cells.data.shape[0]
                if cells.type in sets_dict[key]:
                    sets_dict[key][cells.type].append(members + offset)
                else:
                    sets_dict[key][cells.type] = [members + offset]
        return {
            key: {
                cell_type: np.concatenate(members)
                for cell_type, members in sets.items()
                if sum(map(np.size, members))
            }
            for key, sets in sets_dict.items()
        }

    @classmethod
    def read(cls, path_or_buf, file_format=None):
        # avoid circular import
        from ._helpers import read

        # 2021-02-21
        warnings.warn(
            "meshio.Mesh.read is deprecated, use meshio.read instead",
            DeprecationWarning,
        )
        return read(path_or_buf, file_format)

    def sets_to_int_data(self):
        # If possible, convert cell sets to integer cell data. This is possible if all
        # cells appear exactly in one group.
        default_value = -1
        if len(self.cell_sets) > 0:
            intfun = []
            for k, c in enumerate(zip(*self.cell_sets.values())):
                # Go for -1 as the default value. (NaN is not int.)
                arr = np.full(len(self.cells[k]), default_value, dtype=int)
                for i, cc in enumerate(c):
                    if cc is None:
                        continue
                    arr[cc] = i
                intfun.append(arr)

            for item in intfun:
                if np.any(item == default_value):
                    warnings.warn(
                        "Not all cells are part of a cell set. "
                        f"Using default value {default_value}."
                    )
                    break

            data_name = "-".join(self.cell_sets.keys())
            self.cell_data = {data_name: intfun}
            self.cell_sets = {}

        # now for the point sets
        # Go for -1 as the default value. (NaN is not int.)
        if len(self.point_sets) > 0:
            intfun = np.full(len(self.points), default_value, dtype=int)
            for i, cc in enumerate(self.point_sets.values()):
                intfun[cc] = i

            if np.any(intfun == default_value):
                warnings.warn(
                    "Not all points are part of a point set. "
                    f"Using default value {default_value}."
                )

            data_name = "-".join(self.point_sets.keys())
            self.point_data = {data_name: intfun}
            self.point_sets = {}

    def int_data_to_sets(self):
        """Convert all int data to {point,cell}_sets, where possible."""
        keys = []
        for key, data in self.cell_data.items():
            # handle all int and uint data
            if not all(v.dtype.kind in ["i", "u"] for v in data):
                continue

            keys.append(key)

            # this call can be rather expensive
            tags = np.unique(np.concatenate(data))

            # try and get the names by splitting the key along "-" (this is how
            # sets_to_int_data() forms the key)
            names = key.split("-")
            # remove duplicates and preserve order
            # <https://stackoverflow.com/a/7961390/353337>:
            names = list(dict.fromkeys(names))
            if len(names) != len(tags):
                # alternative names
                names = [f"set{tag}" for tag in tags]

            # TODO there's probably a better way besides np.where, something from
            # np.unique or np.sort
            for name, tag in zip(names, tags):
                self.cell_sets[name] = [np.where(d == tag)[0] for d in data]

        # remove the cell data
        for key in keys:
            del self.cell_data[key]

        # now point data
        keys = []
        for key, data in self.point_data.items():
            # handle all int and uint data
            if not all(v.dtype.kind in ["i", "u"] for v in data):
                continue

            keys.append(key)

            # this call can be rather expensive
            tags = np.unique(data)

            # try and get the names by splitting the key along "-" (this is how
            # sets_to_int_data() forms the key
            names = key.split("-")
            # remove duplicates and preserve order
            # <https://stackoverflow.com/a/7961390/353337>:
            names = list(dict.fromkeys(names))
            if len(names) != len(tags):
                # alternative names
                names = [f"set{tag}" for tag in tags]

            # TODO there's probably a better way besides np.where, something from
            # np.unique or np.sort
            for name, tag in zip(names, tags):
                self.point_sets[name] = np.where(data == tag)[0]

        # remove the cell data
        for key in keys:
            del self.point_data[key]
