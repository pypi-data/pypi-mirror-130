from mbf_genomics.annotator import Annotator, FromFile
import pandas as pd


class Description(Annotator):
    """Add the description for the genes from genome.

    @genome may be None (default), then the ddf is queried for a '.genome'
    Requires a genome with df_genes_meta - e.g. EnsemblGenomes
    """

    columns = ["description"]

    def __init__(self, genome=None):
        self.genome = genome

    def calc_ddf(self, ddf):
        if self.genome is None:
            try:
                genome = ddf.genome
            except AttributeError:
                raise AttributeError(
                    "ddf had no .genome and no genome was passed to Description"
                )
        else:
            genome = self.genome
        lookup = dict(genome.df_genes_meta["description"].items())
        result = []
        for gene_stable_id in ddf.df["gene_stable_id"]:
            result.append(lookup.get(gene_stable_id, ""))
        return pd.Series(result, index=ddf.df.index)


def GeneStrandedSalmon(*args, **kwargs):
    """Deprecated. use anno_tag_counts.Salmon"""
    raise NotImplementedError("Deprecated. Use anno_tag_counts.Salmon")


# FromFile forwarded to mbf_genomics.annotator.FromFile
FromFile = FromFile
