"""
Module to process files 
"""
import os

from plyfile import PlyData
import open3d as o3d
import numpy as np
import argparse
import pylas


def get_ply_data(ply_path, utc_offset=None):
    r"""Reads data from the ply file

    Parameters
    ----------
    ply_path : str
        Path to ply file
    utc_offset: array_like
        Offset for points subtraction

    Returns
    -------
    open3d.geometry.PointCloud
        The points cloud
    """
    plydata = PlyData.read(ply_path)
    angles = np.array(plydata['vertex']['scalar_ScanAngleRank'])
    pcd = o3d.io.read_point_cloud(ply_path)
    if utc_offset is not None:
        pcd = pcd.translate(-utc_offset)
    return pcd, angles


def save_as_las(save_path, cloud):
    r"""Reads data from the ply file

    Parameters
    ----------
    save_path : str
        Path where to store las file
    cloud: open3d.geometry.PointCloud
        Points cloud which should be saved
    """
    las = pylas.create()
    x, y, z = np.asarray(cloud.points).T
    las.x, las.y, las.z = x, y, z
    las.write(save_path)
