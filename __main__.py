"""
The script for the curb processing
"""

from datetime import datetime
import os
import argparse
import numpy as np
import open3d as o3d

from points_processing import get_curbs, get_ground
from files_processing import get_ply_data, save_as_las

DEFAULT_FILENAME = 'borders'
DEFAULT_SAVETYPE = '.las'
UTC_OFFSET = np.array([627285, 4841948, 0.])
DT_FORMAT = "%Y-%m-%d %H:%M:%S"

if __name__ == '__main__':
    # 0. Args processing
    desktop_dir = os.path.join(
        os.path.join(
            os.path.expanduser('~')), 'Desktop') 
    parser = argparse.ArgumentParser(
        "Curb processing module"
        )
    parser.add_argument("--input_path",
                        help="path to input file (.ply format)")
    parser.add_argument("--output_dir",
                        default=desktop_dir,
                        help="path to output dir (file is .las)")
    parser.add_argument("--show_points",
                        action='store_true',
                        help="whether to show cloud points or not")

    args = parser.parse_args()
    # 1. Get the cloud with angles from the ply file
    pcd, angles = get_ply_data(args.input_path, UTC_OFFSET)
    # 2. Preprocess points cloud to extract the ground plane
    inlier_cloud, angles = get_ground(pcd, angles)
    # 3. Extract curb points from the predefined ground plane
    cloud = get_curbs(inlier_cloud)
    # 4. Define current date for the filename
    dt = datetime.now().isoformat()
    filepath = os.path.join(
        args.output_dir,
        DEFAULT_FILENAME + '_' + dt + '.las'
        )
    # 5. Show point clouds (if necessary)
    if args.show_points:
        pcd.voxel_down_sample(0.1)
        o3d.visualization.draw_geometries([pcd])
        o3d.visualization.draw_geometries([inlier_cloud])
        o3d.visualization.draw_geometries([cloud])
    # 6. Save the files (.las format)
    print(filepath)
    save_as_las(filepath, cloud)
