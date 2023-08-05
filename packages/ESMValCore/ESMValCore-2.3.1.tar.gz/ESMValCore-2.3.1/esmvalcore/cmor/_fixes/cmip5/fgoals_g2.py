"""Fixes for FGOALS-g2 model."""
import iris
from cf_units import Unit

from ..fix import Fix
from ..shared import add_sigma_factory, round_coordinates


class AllVars(Fix):
    """Fixes for all variables."""

    def fix_metadata(self, cubes):
        """Fix metadata.

        Fix time coordinate and round other coordinates to fix issue with
        modulus in longitude coordinate.

        Parameters
        ----------
        cubes : iris.cube.CubeList
            Input cubes.

        Returns
        -------
        iris.cube.CubeList

        """
        for cube in cubes:
            try:
                time = cube.coord('time')
            except iris.exceptions.CoordinateNotFoundError:
                pass
            else:
                time.units = Unit(time.units.name, time.units.calendar)

        round_coordinates(cubes, 4, coord_names=['longitude'])

        return cubes


class Cl(Fix):
    """Fixes for ``cl``."""

    def fix_metadata(self, cubes):
        """Fix metadata.

        Add pressure level coordinate.

        Parameters
        ----------
        cubes : iris.cube.CubeList
            Input cubes.

        Returns
        -------
        iris.cube.CubeList

        """
        cube = self.get_cube_from_list(cubes)
        add_sigma_factory(cube)
        return iris.cube.CubeList([cube])
