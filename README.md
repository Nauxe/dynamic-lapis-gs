# Dynamic-LapisGS

The extension of LapisGS to Dynamic 3DGS. 

The Dynamic-LapisGS serves as the foundation of our dynamic 3DGS streaming system, "LTS: A DASH Streaming System for Dynamic Multi-Layer 3D Gaussian Splatting Scenes", which won the **Best Paper Award** at MMSys'25 in April. See the [paper](https://drive.google.com/file/d/1iDz1ExOd1LrPhA7fv4DbLUbzn-Jioihn/view?usp=share_link). 

As for the code of LTS system, however, we have received notice from a company asserting that portions of our work may overlap with their patents related to viewport-dependent streaming. Because of this potential legal issue, **we cannot make the code or scripts openly available at this moment**. 

We apologize for any inconvenience this may cause and appreciate your understanding. We remain open to technical discussions and are willing to provide clarifications regarding the implementation through academic or professional exchange.

Luckily, the core code for Dynamic-LapisGS is still available. You can use it to train and render your own dynamic 3DGS models.

# Setup

The code is built on the codebase of [LapisGS](https://github.com/nus-vv-streams/lapis-gs?tab=readme-ov-file), which essentially only modifies a few lines of code to support dynamic 3DGS. Please refer to the LapisGS repository for detailed requirements and elaboration.

# Pre-processing

## Dataset Preparation


## Dataset Structure


# Running


# Citation

If you find our code or paper useful, please cite:

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