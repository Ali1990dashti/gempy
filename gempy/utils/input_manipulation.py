"""
    This file is part of gempy.

    gempy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    gempy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with gempy.  If not, see <http://www.gnu.org/licenses/>.

Tested on Ubuntu 16

Created on 23/06/2018

@author: Miguel de la Varga
"""
import numpy as np
import pandas as pn


def find_interfaces_from_block(block, value):
    """
    Find the voxel at an interface. We shift left since gempy is based on bottoms

    Args:
        block (ndarray):
        value:

    Returns:

    """
    A = block > value
    # Matrix shifting along axis
    B = A  #
    x_shift = B[:-1, :, :] ^ B[1:, :, :]

    # Matrix shifting along axis
    y_shift = B[:, :-1, :] ^ B[:, 1:, :]

    # Matrix shifting along axis
    z_shift = B[:, :, :-1] ^ B[:, :, 1:]

    final_bool = np.zeros_like(block, dtype=bool)
    final_bool[:-1, :-1, :-1] = x_shift[:, :-1, :-1] ^ y_shift[:-1, :, :-1] ^ z_shift[-1:, -1:, :]

    return final_bool


def interfaces_from_interfaces_block(block_bool, grid, formation='default_formation', series='Default_series',
                                     formation_number=1, order_series=1, n_points=20):

    coord_select = grid[np.ravel(block_bool)]

    loc_points = np.linspace(0, coord_select.shape[0]-1, n_points, dtype=int)

    # Init dataframe
    p = pn.DataFrame(columns=['X', 'Y', 'Z', 'formation', 'series', 'formation_number',
                              'order_series', 'isFault'])

    p[['X', 'Y', 'Z']] = pn.DataFrame(coord_select[loc_points])
    p['formation'] = formation
    p['series'] = series
    p['formation_number'] = formation_number
    p['order_series'] = order_series

    return p


def set_interfaces_from_block(geo_data, block):
    values = np.unique(np.round(block))
    values.sort()
    values = values[:-1]
    interfaces_df = pn.DataFrame(columns=['X', 'Y', 'Z', 'formation', 'series', 'formation_number',
                                          'order_series'])
    for e, value in enumerate(values):
        block_bool = find_interfaces_from_block(block, value)
        #interfaces_df.append(interfaces_from_interfaces_block(block_bool, geo_data.grid.values,
        #                                                      formation='formation_'+str(e), series='Default_series',
        #                                                     formation_number=e, order_series=1))
        geo_data.set_interfaces(interfaces_from_interfaces_block(block_bool, geo_data.grid.values,
                                                              formation='formation_'+str(e), series='Default_series',
                                                              formation_number=e, order_series=1), append=True)

    return geo_data
