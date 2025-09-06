import os
import sys
from argparse import ArgumentParser


if __name__ == "__main__":

    frames_dict = {
        "longdress": list(range(1051, 1053)),
        # "longdress": list(range(1051, 1081)),
        "soldier": list(range(536, 566)),
        "loot": list(range(1000, 1030)),
        "redandblack": list(range(1450, 1480)),
    }

    # Set up command line argument parser
    parser = ArgumentParser(description="Training script parameters")
    parser.add_argument('--model_base', type=str, required=True, help="Path to the model root directory")
    parser.add_argument('--dataset_base', type=str, required=True, help="Path to the dataset root directory")
    parser.add_argument('--dataset_name', type=str, required=True, help="Name of the dataset")
    parser.add_argument('--scene', type=str, required=True, help="Name of the scene")
    parser.add_argument('--method', type=str, required=True, help="Name of the method", choices=["lapis", "freeze", "dynamic-lapis"])
    parser.add_argument('--lambda_dssim', type=float, default=0.8, help="Lambda for DSSIM loss")
    parser.add_argument('--iterations', type=int, default=30_000, help="Number of training iterations for each resolution")
    args = parser.parse_args(sys.argv[1:])


    model_base = args.model_base
    dataset_base = args.dataset_base
    dataset_name = args.dataset_name
    scene = args.scene
    method = args.method
    lambda_dssim = args.lambda_dssim
    iterations = args.iterations

    resolution_scales = [8, 4, 2, 1]
    train_bin = "dynamic-lapis-gs/train.py"

    train_command = ""

    if method == "dynamic-lapis":
        '''Dynamic-LapisGS
        Combine with the training strategy of "Dynamic 3D Gaussians: Tracking by Persistent Dynamic View Synthesis"
        Which is,
        Train the first frame, and only update the position and rotation for the subsequent frames, so that each splat has its correspondence across frames 
        '''
        first_frame = frames_dict[scene][0]
        subsequent_frames = frames_dict[scene][1:]

        # 1. train the first frame from scratch
        for idx, resolution in enumerate(resolution_scales):
            if not (os.path.isfile(f"{model_base}/{dataset_name}/{scene}/{method}/{scene}_res{resolution}/{first_frame:04}/point_cloud/iteration_30000/point_cloud.ply")): # TEMPORARY, skip the training if the model already exists

                print(f"Training model for {scene} frame {first_frame:04} at resolution {resolution}")

                model_dir = os.path.join(model_base, dataset_name, scene, method, f"{scene}_res{resolution}", f"{first_frame:04}")
                os.makedirs(model_dir, exist_ok=True) # mkdir model_dir if not exists
                source_dir = os.path.join(dataset_base, dataset_name, scene, f"{scene}_res{resolution}", f"{first_frame:04}")

                if resolution == 8: # train from scratch for the first resolution
                    train_command = f"python {train_bin} -s {source_dir} -m {model_dir} --data_device cuda --lambda_dssim {lambda_dssim} --iterations {iterations}"
                else: # for other resolutions, use the previous resolution's model as foundation GS
                    train_command = f"python {train_bin} -s {source_dir} -m {model_dir} --data_device cuda --lambda_dssim {lambda_dssim}  --iterations {iterations} --dynamic_opacity --foundation_gs_path {model_base}/{dataset_name}/{scene}/{method}/{scene}_res{resolution_scales[idx-1]}/{first_frame:04}/point_cloud/iteration_30000/point_cloud.ply"

                os.system(train_command) # run the command lines


        # 2. train the subsequent frames based on the previous frame, no densification, only update the position and rotation
        for frame in subsequent_frames:
            for idx, resolution in enumerate(resolution_scales):
                print(f"Training model for {scene} frame {frame:04} at resolution {resolution}")
                
                model_dir = os.path.join(model_base, dataset_name, scene, method, f"{scene}_res{resolution}", f"dynamic_{frame:04}")
                os.makedirs(model_dir, exist_ok=True) # mkdir model_dir if not exists
                source_dir = os.path.join(dataset_base, dataset_name, scene, f"{scene}_res{resolution}", f"{frame:04}")
                

                if frame == subsequent_frames[0]:
                    previous_gs_path = os.path.join(model_base, dataset_name, scene, method, f"{scene}_res{resolution}", f"{(frame-1):04}", "point_cloud", "iteration_30000", "point_cloud.ply")
                else:
                    previous_gs_path = os.path.join(model_base, dataset_name, scene, method, f"{scene}_res{resolution}", f"dynamic_{(frame-1):04}", "point_cloud", "iteration_30000", "point_cloud.ply")

                # disable densification and opacity reset by:
                # 1. setting --densify_from_iter and --opacity_reset_interval larger than number of iterations, 
                # 2. setting --densify_until_iter to 0
                train_command = f"python {train_bin} -s {source_dir} -m {model_dir} --eval --data_device cuda --lambda_dssim {lambda_dssim}  --iterations {iterations} --densify_from_iter {iterations+1} --densify_until_iter 0 --opacity_reset_interval {iterations+1}  --initial_gs_path {previous_gs_path}"


                # run the command lines
                os.system(train_command)