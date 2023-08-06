from ..core import MuDataSet
from ..utils import sizefmt


class Brain9kMultiome(MuDataSet):
    """
    Chromatin and gene-regulatory dynamics 
    of the developing human cerebral cortex 
    at single-cell resolution.

    Trevino, ..., Greenleaf, 2021
    DOI: 10.1016/j.cell.2021.07.039
    """

    def __init__(self):
        self.name = "brain9k_multiome"
        self.version = "1.0"
        self.files = [
            {
                "name": "GSE162170_multiome_rna_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Frna%5Fcounts%2Etsv%2Egz",
                "md5": "7283504077be065a86b4e4fb49fa07d0",
                "size": 24845803,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_spliced_rna_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fspliced%5Frna%5Fcounts%2Etsv%2Egz",
                "md5": "695ff462dc5049500f0f84cfd3ca99ef",
                "size": 11115238,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_unspliced_rna_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Funspliced%5Frna%5Fcounts%2Etsv%2Egz",
                "md5": "b0fd66acd2e98b56e024a2556f24a5de",
                "size": 15622285,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_atac_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fatac%5Fcounts%2Etsv%2Egz",
                "md5": "c0991a4766d8f5e0c93fe69378069bbf",
                "size": 149865144,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_atac_consensus_peaks.txt.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fatac%5Fconsensus%5Fpeaks%2Etxt%2Egz",
                "md5": "9481374ba303b098ed74286961fa561f",
                "size": 18315449,
                "format": "txt.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_cell_metadata.txt.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fcell%5Fmetadata%2Etxt%2Egz",
                "md5": "ab2687f9c01448d07bd0411d8d20b2f4",
                "size": 492098,
                "format": "txt.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_cluster_names.txt.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fcluster%5Fnames%2Etxt%2Egz",
                "md5": "07427984630409803b2ac568aaf248c3",
                "size": 278,
                "format": "txt.gz",
                "raw": False,
            },
            {
                "name": "GSE162170_multiome_atac_gene_activities.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fatac%5Fgene%5Factivities%2Etsv%2Egz",
                "md5": "4f967ec9929240503c5083c718e80142",
                "size": 831813316,
                "format": "tsv.gz",
                "raw": False,
            },
        ]

        self.total_size_int = sum([f["size"] for f in self.files])
        self.total_size = sizefmt(self.total_size_int)

        self.data = {
            "name": self.name,
            "version": self.version,
            "total_size": self.total_size,
            "files": self.files,
        }
        self.data_versions = [
            self.data,
        ]

        self.info = {
            **self.data,
            "data_versions": self.data_versions,
        }

    def load(self, data_dir="./"):
        from os import path
        import gzip
        from tqdm import tqdm

        import numpy as np
        from scipy.sparse import coo_matrix, csr_matrix
        import pandas as pd
        from mudata import AnnData, MuData

        def read_counts(fname, sep=",", header=True, index=True, obs_in_rows=True):
            data, row, col = [], [], []
            row_names, col_names = [], []
            with open(fname, 'rb') as f:
                if header:
                    col_names = f.readline().decode().split(sep)
                else:
                    ncol = len(f.readline().decode().split(sep))
                    col_names = [f"obs{i}" for i in range(ncol)]
                    f.seek(0)

                for i, line in tqdm(enumerate(f), postfix=f"Reading {fname}..."):
                    values = line.decode().split(sep)
                    if index:
                        row_name, values = values[0], np.array([int(v) for v in values[1:]])
                    else:
                        row_name = f"var{i}"
                        values = np.array([int(v) for v in values])
                    js = np.where(values != 0)[0]

                    row.append(np.repeat(i, len(js)))
                    col.append(js)
                    data.append(values[js])
                    row_names.append(row_name)
            data = [v for e in data for v in e]
            row = [v for e in row for v in e]
            col = [v for e in col for v in e]
            if not obs_in_rows:
                row, col = col, row
                row_names, col_names = col_names, row_names
            mx = coo_matrix((data, (row, col)), shape=(len(row_names), len(col_names)))
            adata = AnnData(X=csr_matrix(mx), obs=pd.DataFrame(index=row_names), var=pd.DataFrame(index=col_names))
            return adata

        modalities = dict()
        counts = {"rna": "GSE162170_multiome_rna_counts.tsv.gz", "atac": "GSE162170_multiome_atac_counts.tsv.gz"}
        for m, fname in counts.items():
            fpath = os.path.join(data_dir, fname)
            modalities[m] = read_counts(fpath, sep="\t", obs_in_rows=False)

        mdata = MuData(modalities)

        # TODO: [atac].var in GSE162170_multiome_atac_consensus_peaks.txt.gz
        # TODO: obs in GSE162170_multiome_cell_metadata.txt.gz

        return mdata


def dataset():
    return Brain9kMultiome()
