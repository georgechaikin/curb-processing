"""
Module for points processing
"""

from plyfile import PlyData
import open3d as o3d
import argparse
import numpy as np
import os


def get_ground(pcd, angles, angle_threshold=20):
    r"""Extracts the ground plane from the point cloud

    Parameters
    ----------
    pcd : open3d.geometry.PointCloud
        Point cloud
    angles : array_like
        array with points angles
    angle_threshold : int
        Angle threshold to filter the point cloud

    Returns
    -------
    tuple
        the cloud with ground plane and new angles array
    """
    _, inliers = pcd.segment_plane(
        distance_threshold=0.25,
        ransac_n=3,
        num_iterations=1000)
    
    inlier_cloud = pcd.select_by_index(inliers)
    angles = angles[inliers]
    angles_condition = (angles > angle_threshold).nonzero()[0]
    inlier_cloud = inlier_cloud.select_by_index(angles_condition)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    return inlier_cloud, angles


def get_curbs(cloud, min_diff=0.05, max_diff=0.1, xy_max_diff=0.5):
    r"""Extracts the curbs from the points cloud

    Parameters
    ----------
    cloud : open3d.geometry.PointCloud
        Point cloud
    min_diff : float
        Min z difference threshold
    max_diff : float
        Max z difference threshold
    xy_max_diff : float
        Difference threshold along x and y axes
    Returns
    
    -------
    open3d.geometry.PointCloud
        The cloud with curbs
    """
    cloud_arr = np.asarray(cloud.points)
    xy = cloud_arr[:,:-1] 
    z = cloud_arr[:,-1]
    indices = np.arange(len(z))
    left, right = indices, np.roll(indices, 5)
    xy_diff = np.linalg.norm(xy[left] - xy[right], axis=1)
    height_diff = z[left] - z[right]
    inliers = (height_diff > min_diff) & (height_diff < max_diff) & (xy_diff < xy_max_diff)
    inliers = inliers.nonzero()[0]
    cloud = cloud.select_by_index(inliers)
    return cloud