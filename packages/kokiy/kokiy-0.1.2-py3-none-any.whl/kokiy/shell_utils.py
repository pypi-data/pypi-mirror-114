"""
Module for cartesian or axi-cylindrical cut plane tools
"""

import numpy as np

from arnica.utils.vector_actions import yz_to_theta
from arnica.utils.cloud2cloud import cloud2cloud
#from cloud2cloud import cloud2cloud

from kokiy import AxiShell
from kokiy import CartShell


# TODO: do we really care with those that misuse import?
__all__ = ["infer_shell_from_xyz", "axishell_create_structured_base",
           "cartshell_create_structured_base",
           "interpolate_solutions_on_shell",
           "shell_geom_type", "shell_repr"]


def infer_shell_from_xyz(mesh_xyz, geom_type, shape, bnd_uv=None, bnd_angles=None):
    """ Build a shell from an AVBP Cut

    :param geom_type: str, either "cart" or "axicyl".
    :param shape: tuple (nu,nv), discretization of the shell
    :param bnd_angles: Boundary angles to keep a fraction of the cuts
    :type bnd_uv: list of 4 floats to limit sheel umin, umax, vmin, vmax
    """
    if bnd_angles is not None:
        raise DeprecationWarning("BNd_angle is not used anymore, Use bnd_uv")

    #mesh = find_mesh_for_sol(paths, prefix)
    # Build shell
    if geom_type == "axicyl":
        shell = axishell_create_structured_base(
            shape[0],
            shape[1],
            mesh_xyz,
            bnd_uv)
    elif geom_type == "cart":
        shell = cartshell_create_structured_base(
            shape[0],
            shape[1],
            mesh_xyz)
    return shell


def axishell_create_structured_base(n_longi, n_azi, mesh, bnd_uv=None):
    """
    *Obtain the base in structured mesh*

    Assumes the mesh is the x_axis rotated extrusion of an (x,r) curve.

    :param n_longi: int, Number of radial points of the shell
    :param n_azi: int, Number of azimuthal points of the shell
    :param mesh: Array of coordinates of the cut mesh of shape (n, 3)
    :type bnd_uv: list of 4 floats to limit shell umin, umax, vmin, vmax

    :returns:
        - **shell** -  An array representing axysymmetric computational shell
    """

    x_pos = mesh[:, 0].mean()
    r_vals = np.hypot(mesh[:, 1],mesh[:, 2])
    theta = np.rad2deg(yz_to_theta(mesh[:, :]))

    
    if bnd_uv is None:
        bnd_uv = [None, None, None, None]
    if bnd_uv[0] is None:
        bnd_uv[0] = r_vals.min()
    if bnd_uv[1] is None:
        bnd_uv[1] = r_vals.max()
    if bnd_uv[2] is None:
        bnd_uv[2] = theta.min()
    if bnd_uv[3] is None:
        bnd_uv[3] = theta.max()
    
    x_ctrl_pts = [x_pos, x_pos]
    r_ctrl_pts =  [bnd_uv[0], bnd_uv[1]]
    tmin = bnd_uv[2]
    tmax = bnd_uv[3]
    
    shell = AxiShell(
        n_azi,
        n_longi,
        tmax-tmin, #angle_range,
        x_ctrl_pts, #x_vals[corners_idx],
        r_ctrl_pts, #r_vals[corners_idx],
        tmin #angle_min,
    )

    return shell


def cartshell_create_structured_base(n_longi, n_trans, mesh):
    # pylint: disable=invalid-name
    """
    *Obtain the base in structured mesh*

    Assumes the path is square, aligned with y and z, with x = constant.

    :param n_longi: Number of longitudinal points of the shell
    :type n_longi: int
    :param n_trans: Number of transversal points of the shell
    :type n_trans: int
    :param mesh: Array of coordinates of the cut mesh of shape (n, 3)

    :returns:
        - **shell** -  An array representing cartesian computational shell
    """

    x_vals, y_vals, z_vals = mesh.T

    zero = (x_vals.mean(), y_vals.min(), z_vals.min())
    v_max = (x_vals.mean(), y_vals.max(), z_vals.min())
    u_max = (x_vals.mean(), y_vals.min(), z_vals.max())
    shell = CartShell(
        n_trans,
        n_longi,
        zero,
        u_max,
        v_max,
    )

    return shell

def _shell_interp_on_struct_base(shell, mesh, raw_data):
    """
    *Interpolate unstructured data on a structured grid*

    :param shell: AxiShell or CartShell object
    :param mesh: Array of shape (N,3) containing coordinates of raw_data
    :param raw_data: A numpy structured array gathering the unstructured data

    :returns: **struct_data** -  An array holding the intrepolated structured data
    """

    dim = shell.xyz.shape[-1]
    target_xyz = shell.xyz.reshape(-1, dim)

    # Arnica way
    raw_data_dict = {key: raw_data[key] for key in raw_data.dtype.names}  # Structured array to dict
    struct_dict = cloud2cloud(mesh, raw_data_dict, target_xyz, stencil=4, power=4)
    struct_data = np.empty(shell.shape, dtype=raw_data.dtype)
    for key in struct_dict:
        struct_data[key] = struct_dict[key].reshape(shell.shape)

    # Elois Cloud2Cloud way
    # val_names =  raw_data.dtype.names
    # source_array = np.empty( (mesh.shape[0], len(val_names) ))
    # for i, key in enumerate(val_names):
    #     source_array[:,i] = raw_data[key]
    # target_array = cloud2cloud(mesh, source_array, target_xyz, stencil=4)
    
    # struct_data = np.empty(shell.shape, dtype=raw_data.dtype)
    # for i, key in enumerate(val_names):
    #    struct_data[key] = target_array[:, i].reshape(shell.shape)


    return struct_data


def interpolate_solutions_on_shell(shell, mesh, raw_data):
    """
    *Loads AVBP solutions interpolated on structured mesh.*

    :param shell: A shell
    :param data_dict: | A dict( ) containing data on the format \
                      **data_dict** [*key*] = array(*n_steps*, *n_theta*, *n_r*)
                      with various names "rho", "rhou"...

    :returns:
        - **interpol_data** - A dict( ) containing interpolated data
    """

    # TODO : make this interpolation without the for on times
    # probably inside the cloud to cloud
    n_steps = raw_data.shape[0]
    interpol_data = np.zeros((n_steps, *shell.shape), dtype=raw_data.dtype)
    for step in range(n_steps):
        interpol_data[step] = _shell_interp_on_struct_base(
            shell,
            mesh,
            raw_data[step],
        )

    return interpol_data


def shell_geom_type(shell):
    """Return the shell geom_type"""
    # TODO: really required?
    if isinstance(shell, AxiShell):
        return "axicyl"
    elif isinstance(shell, CartShell):
        return "cart"
    else:
        msgerr = "Shell object must be an AxiShell or a CartShell"
        msgerr += "\n" + str(shell)
        raise RuntimeError(msgerr)


def shell_repr(shell):
    """return a shell description"""
    # TODO: why not to make it a method of shell?
    out = f"""
Shell
-----

shape :{shell.shape}
type : {shell_geom_type(shell)}

"""
    return out
