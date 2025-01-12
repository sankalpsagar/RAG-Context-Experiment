# To run
download dataset from:
https://drive.google.com/drive/folders/1qIZcNcU2wtiJNr3BUyX2GIUtnHEfbQDi?usp=sharing
and put the files in a folder called dataset in the root

download teh corpus:
https://drive.google.com/drive/folders/1aQAfNLq6HB0w4_fVnKMBvKA6cXJGRTpH?usp=sharing
and put the file in a folder called dataset in the root

change config.ini if necessary to update paths


# What I had to do to get it working on Ubuntu 24.04.1
use anaconda env with python 3.11
``pip install dexter-cqa``

conda update -n base -c defaults conda
conda install -c anaconda libstdcxx-ng
I copied [libstdc++.so.6.0.29](../../anaconda3/lib/libstdc%2B%2B.so.6.0.29)
to [libstdc++.so.6.0.29](../../anaconda3/envs/NLP-project/lib/libstdc%2B%2B.so.6.0.29)
To get it working for me

# link for the pickle files:
https://tud365-my.sharepoint.com/:f:/g/personal/sankalpsagar_tudelft_nl/EmV-kwrk-rdPn4JqoWWHIgsBzC8Un2gaxbpbGTvkEDLapA?e=0sEwVh

# some links:
https://pypi.org/project/dexter-cqa/
https://anonymous.4open.science/r/BCQA-05F9/README.md


