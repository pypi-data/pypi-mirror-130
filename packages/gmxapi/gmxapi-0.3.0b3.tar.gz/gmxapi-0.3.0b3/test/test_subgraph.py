#
# This file is part of the GROMACS molecular simulation package.
#
# Copyright (c) 2019,2021, by the GROMACS development team, led by
# Mark Abraham, David van der Spoel, Berk Hess, and Erik Lindahl,
# and including many others, as listed in the AUTHORS file in the
# top-level source directory and at http://www.gromacs.org.
#
# GROMACS is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# GROMACS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with GROMACS; if not, see
# http://www.gnu.org/licenses, or write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#
# If you want to redistribute modifications to GROMACS, please
# consider that scientific software is very special. Version
# control is crucial - bugs must be traceable. We will be happy to
# consider code for inclusion in the official distribution, but
# derived work must not be called official GROMACS. Details are found
# in the README & COPYING files - if they are missing, get the
# official version at http://www.gromacs.org.
#
# To help us fund GROMACS development, we humbly ask that you cite
# the research papers on the package. Check out http://www.gromacs.org.

import gmxapi as gmx

try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank_number = comm.Get_rank()
    comm_size = comm.Get_size()
except ImportError:
    comm = None
    rank_number = 0
    comm_size = 1
    rank_tag = ''
    MPI = None
else:
    rank_tag = 'rank{}:'.format(rank_number)

#
# if rank_number == 1:
#     import pydevd_pycharm
#     pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)


@gmx.function_wrapper(output={'data': float})
def add_float(a: float, b: float) -> float:
    return a + b


@gmx.function_wrapper(output={'data': bool})
def less_than(lhs: float, rhs: float, output=None):
    output.data = lhs < rhs


def test_subgraph_function():
    subgraph = gmx.subgraph(variables={'float_with_default': 1.0, 'bool_data': True})
    with subgraph:
        # Define the update for float_with_default to come from an add_float operation.
        subgraph.float_with_default = add_float(subgraph.float_with_default, 1.).output.data
        subgraph.bool_data = less_than(lhs=subgraph.float_with_default, rhs=6.).output.data
    operation_instance = subgraph()
    operation_instance.run()
    assert operation_instance.values['float_with_default'] == 2.

    loop = gmx.while_loop(operation=subgraph, condition=subgraph.bool_data)
    handle = loop()
    handle.run()
    assert handle.output.float_with_default.result() == 6


# def test_subgraph_cli(cleandir):
#     # Make a tool whose invocation always looks the same, but which has different
#     # output on each iteration.
#     scriptname = os.path.join(cleandir, 'clicommand.sh')
#     with open(scriptname, 'w') as fh:
#         fh.write('\n'.join(['#!/usr/bin/env bash',
#                             '# Concatenate an input file and a string argument to an output file.',
#                             '# Mock a utility with the tested syntax.',
#                             '#     clicommand.sh "some words" -i inputfile -o outputfile',
#                             'exit 1\n']))
#     os.chmod(scriptname, stat.S_IRWXU)
#
#     @gmx.function_wrapper()
#     def condition(line: str) -> bool:
#         if line.startswith('hello hello world'):
#             return True
#         return False
#
#     subgraph = gmx.subgraph(
#         variables={
#             'is_done': False,
#             'not_done': True,
#             'line': 'world'})
#     with subgraph:
#
#     loop = gmx.while_loop(operation=subgraph, condition=subgraph.not_done)
#     loop().run()


def test_local_tools_and_assumptions():
    const = gmx.make_constant(1.)
    assert add_float(const, const).output.data.result() == 2
    assert gmx.logical_not(less_than(const, const).output.data).result()
    # Note: It may not be safe to assume that keyword argument order (lhs, rhs) is preserved.
    assert less_than(const, add_float(const, const).output.data).output.data.result()
