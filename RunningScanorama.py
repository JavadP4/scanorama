import os

import numpy as np
from scanorama import *
from scipy.sparse import vstack
from sklearn.preprocessing import normalize, LabelEncoder
import sys
from time import time
from bin.process import load_names, process

data_names = [
    'bin/data/mouse_brain/dropviz/Cerebellum_ALT',
    'bin/data/mouse_brain/dropviz/Cortex_noRep5_FRONTALonly',
    'bin/data/mouse_brain/dropviz/Cortex_noRep5_POSTERIORonly',
    'bin/data/mouse_brain/dropviz/EntoPeduncular'
]

# process(data_names, min_trans=100)
# it saves files in npz format if they are "mtx", "h5", or "txt"|"tsv"|"txt.gz"|"tsv.gz"
# if data_names are folders then it assumes that each folder contains a mtx file named "matrix.mtx", and a tsv file for gene names "genes.tsv"; if it is a file name then it checks different file types ("h5", or "txt"|"tsv"|"txt.gz"|"tsv.gz")


# "load_names" (which calls "load_data" which uses scipy.sparse.load_npz for loading data) assumes that datasets are npz files (any full path of a ".npz" file or a folder containing "tab.npz" and "tab.genes.txt" files; these files are created by "process" function from other data types). It loads datasets and normalize them based on "norm" flag. If you are going to do the run "integrate" it does the normalization by calling the "process_data" so you can set "norm" to False.
# signature: load_names(data_names, norm=True, log1p=False, verbose=True).
t0 = time()
datasets, genes_list, n_cells = load_names(data_names)
print('Load time: {:.3f}s'.format(time() - t0))

t0 = time()
datasets_dimred, datasets, genes = correct(
    datasets, genes_list, ds_names=data_names,
    return_dimred=True, batch_size=BATCH_SIZE,
)
print('Batch corrected panoramas: {:.3f}s'.format(time() - t0))
t0 = time()
integrated, corrected, genes = scanorama.correct(datasets, genes_list, return_dimred=True)
print('Batch corrected and integration in: {:.3f}s'
      .format(time() - t0))