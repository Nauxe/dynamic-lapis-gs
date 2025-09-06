# Dynamic-LapisGS

The extension of LapisGS to Dynamic 3DGS. 

The Dynamic-LapisGS serves as the foundation of our dynamic 3DGS streaming system, "LTS: A DASH Streaming System for Dynamic Multi-Layer 3D Gaussian Splatting Scenes", which won the 🏆**Best Paper Award**🏆 at ACM MMSys'25 in April. See the [paper](https://drive.google.com/file/d/1iDz1ExOd1LrPhA7fv4DbLUbzn-Jioihn/view?usp=share_link). 

As for the code of LTS system, however, we have received notice from a company asserting that portions of our work may overlap with their patents related to viewport-dependent streaming. We are currently addressing this issue. At this moment, **we cannot make the system code or scripts openly available**. 

We apologize for any inconvenience this may cause and appreciate your understanding. We remain actively open to technical discussions and are strongly willing to provide clarifications regarding the implementation through academic or professional exchange.

Luckily, the core code for Dynamic-LapisGS is still available. You can use it to train and render your own dynamic 3DGS models.

## Setup

The code is built on the codebase of [LapisGS](https://github.com/nus-vv-streams/lapis-gs?tab=readme-ov-file), which essentially only modifies a few lines of code to support dynamic 3DGS. Please refer to the LapisGS repository for detailed requirements and elaboration.

## Pre-processing

To be released soon.

### Dataset Preparation


### Dataset Structure


## Running

```bash
python train_full_pipeline.py --model_base <path to the output model root directory> --dataset_base <path to the source root directory> --dataset_name <name of the dataset> --scene <name of the scene> --method <name of the method>  --frame_list <two numbers separated by space, indicating the start and end frame index, e.g., 0 30>
```

<details>
<summary><span style="font-weight: bold;">Please click here to see the arguments for the `train_full_pipeline.py` script.</span></summary>

| Parameter | Type | Description |
| :-------: | :--: | :---------: |
| `--model_base`   | `str` | Path to the output model root directory.|
| `--dataset_base` | `str` | Path to the source root directory. |
| `--dataset_name` | `str` | Name of the dataset of scenes. |
| `--scene`        | `str` | Name of the scene. |
| `--method`       | `str` | Name of the method we build the LOD 3DGS. Can be `"dynamic-lapis"` (the proposed method). |
| `--frame_list`   | `str` | Two numbers separated by space, indicating the start and end frame index, e.g., `0 30`. |

</details>
<br>

For example, we train the model for the scene *longdress* from dataset *8i* with the proposed method *dynamic-lapis*, using the command:
```bash
python train_full_pipeline.py --model_base ./model --dataset_base ./source --dataset_name 8i --scene longdress --method dynamic-lapis --frame_list 1051 1080
```

The file structure after training should be as follows:
```
project
└── source # dataset_base
    ├── 8i # dataset_name
    │   └── longdress # scene
    │       └── longdress_res1
    │           ├── 1051
    │           ├── 1052
    │           ├── 1053
    │           ...
    │       ├── longdress_res2
    │       ├── longdress_res4
    │       └── longdress_res8
└── model # model_base
    ├── 8i # dataset_name
    │   └── longdress # scene
    │       └── dynamic-lapis # method
    │           └── longdress_res1
    |               ├── 1051
    │               ├── dynamic_1052
    │               ├── dynamic_1053
    │               ...
    │               └── dynamic_1080
    │           ├── longdress_res2
    │           ├── longdress_res4
    │           └── longdress_res8
```


### Evaluation

We use the following command to evaluate the model:
```bash
python render.py -m <path to trained model> # Generate renderings
python metrics.py -m <path to trained model> # Compute error metrics on renderings
```

## Citation

If you find our code or paper useful, please cite:

```
@inproceedings{sun2025lts,
  author       = {Yuan{-}Chun Sun and
                  Yuang Shi and
                  Cheng{-}Tse Lee and
                  Mufeng Zhu and
                  Wei Tsang Ooi and
                  Yao Liu and
                  Chun{-}Ying Huang and
                  Cheng{-}Hsin Hsu},
  title        = {{LTS:} {A} {DASH} Streaming System for Dynamic Multi-Layer {3D} {Gaussian}
                  Splatting Scenes},
  booktitle    = {Proceedings of the 16th {ACM} Multimedia Systems Conference, MMSys
                  2025, Stellenbosch, South Africa, 31 March 2025 - 4 April 2025},
  pages        = {136--147},
  publisher    = {{ACM}},
  year         = {2025},
  url          = {https://doi.org/10.1145/3712676.3714445},
  doi          = {10.1145/3712676.3714445},
}
```