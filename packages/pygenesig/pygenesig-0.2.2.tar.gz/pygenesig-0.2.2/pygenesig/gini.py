"""
The Gini-coefficient (gini index) measures the inequality among values of
a frequency distribution. Originally applied to measure income inequality
we can also use it on gene expression data to find genes that are
over-represented in certain samples.
"""

import numpy as np
import pandas as pd
from pygenesig.validation import SignatureGenerator
from pygenesig.tools import collapse_matrix


def gini(array):
    """
    Calculate the Gini coefficient of a numpy array.

    Based on: https://github.com/oliviaguest/gini

    Args:
        array (array-like): input array

    Returns:
        float: gini-index of ``array``

    >>> a = np.zeros((10000))
    >>> a[0] = 1.0
    >>> '%.3f' % gini(a)
    '1.000'
    >>> a = np.ones(100)
    >>> '%.3f' % gini(a)
    '0.000'
    >>> a = np.random.uniform(-1,0,1000000)
    >>> '%.2f' % gini(a)
    '0.33'
    """
    # based on bottom eq: http://www.statsdirect.com/help/content/image/stat0206_wmf.gif
    # from: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    if np.amin(array) < 0:
        array -= np.amin(array)  # values cannot be negative
    array += 1e-12  # values cannot be 0
    array = np.sort(array)  # values must be sorted
    index = np.arange(1, array.shape[0] + 1)  # index per array element
    n = array.shape[0]  # number of array elements
    return (np.sum((2 * index - n - 1) * array)) / (
        n * np.sum(array)
    )  # Gini coefficient


def get_rogini_format(df_aggr, min_gini=0.7, max_rk=None, min_expr=1):
    """
    Imitate the *rogini* output format.

    Args:
        df_aggr (pd.DataFrame): m x n pandas DataFrame with m Genes and n tissues
        min_gini (float): gini cutoff, genes need to have a gini index larger than this value.
        max_rk (int): rank cutoff, include genes if they rank <= max_rank among all tissues.
        min_expr (float): minimal expression

    Returns:
        pd.DataFrame: equal to *rogini* output.

        Example::

            GENEID  CATEGORY        VALUE   RANKING GINI_IDX
            54165   Whole blood (ribopure)  491.359000      1       0.441296
            54165   CD34 cells differentiated to erythrocyte lineage        148.124000      2       0.441296
            54165   Mast cell - stimulated  68.973000       3       0.441296
            101927596       CD4+CD25-CD45RA+ naive conventional T cells     15.505000       1       0.948804
            101927596       CD8+ T Cells (pluriselect)      15.376000       2       0.948804
            101927596       CD4+CD25-CD45RA- memory conventional T cells    10.769000       3       0.948804

    """
    if max_rk is None:
        max_rk = float("inf")
    if min_gini is None:
        min_gini = 0
    if min_expr is None:
        min_expr = float("-inf")

    rogini_rows = []
    expr_gini = df_aggr.apply(gini, axis=1)
    expr_rank = df_aggr.rank(axis=1, ascending=False)
    for i in range(df_aggr.shape[0]):
        geneid = df_aggr.index[i]
        expr_row = df_aggr.iloc[i]
        gini_row = expr_gini.iloc[i]
        rk_row = expr_rank.iloc[i]
        which_cols = np.flatnonzero(
            (rk_row <= max_rk) & (gini_row >= min_gini) & (expr_row >= min_expr)
        )
        for j in which_cols:
            rogini_rows.append(
                [geneid, df_aggr.columns[j], expr_row[j], rk_row[j], gini_row]
            )
    columns = ["GENEID", "CATEGORY", "VALUE", "RANKING", "GINI_IDX"]
    df = pd.DataFrame(rogini_rows)
    df.columns = columns
    df.sort_values(["GENEID", "RANKING"], inplace=True)

    # the index does not have any meaning, we therefore want a consecutive index in the final data frame
    df.reset_index(drop=True, inplace=True)
    return df


def get_gini_signatures(
    df_aggr, min_gini=0.7, max_rk=3, max_rel_rk=None, min_expr=None
):
    """
    Generate gene signatures using gini index.

    Finds over-represented genes for each sample group, given the specified thresholds.

    Args:
        df_aggr (pd.DataFrame): m x n pandas DataFrame with m Genes and n tissues
        min_gini (float): gini cutoff, genes need to have a gini index larger than this value.
        max_rk (int): rank cutoff, include genes if they rank <= max_rank among all tissues.
        max_rel_rk (float): rank cutoff, include genes if they rank <= mal_rel_rk * m among all genes
            in the current sample.
        min_expr (float): minimal expression

    Returns:
        dict of list: A signature dictionary.

        Example::

            {
                "tissue1" : [list, of, gene, ids],
                "tissue2" : [list, of, other, genes],
                ...
            }

    """
    if max_rk is None:
        max_rk = float("inf")
    if min_gini is None:
        min_gini = 0
    if min_expr is None:
        min_expr = float("-inf")
    if max_rel_rk is None:
        max_rel_rk = 1

    # convert relative rank to absolute rank
    max_gene_rk = max_rel_rk * df_aggr.shape[0]

    expr_gini = df_aggr.apply(gini, axis=1)
    expr_rank_sample = df_aggr.rank(
        axis=1, ascending=False
    )  # rank across samples (along row)
    expr_rank_gene = df_aggr.rank(
        axis=0, ascending=False
    )  # rank across genes (along column)
    sig_mask = (
        (expr_rank_sample <= max_rk)
        & (df_aggr >= min_expr)
        & (expr_rank_gene <= max_gene_rk)
    )
    sig_mask.loc[
        expr_gini < min_gini,
    ] = False

    signatures = {}
    for tissue, sig_series in sig_mask.iteritems():
        signatures[tissue] = set(np.flatnonzero(sig_series))
    return signatures


class GiniSignatureGenerator(SignatureGenerator):
    """
    Use gini index to generate gene signatures.

    Genes, which are specific for a tissue result in a high gini index,
    whereas genes equally present in all tissues have a gini index close to zero.

    The idea is, that genes with a high gini index will reliably identify
    their tissue of origin.

    Args:
        expr (np.ndarray): m x n matrix with m samples and n genes
        target (array-like): m-vector with true tissue for each sample
        min_gini (float): gini cutoff, genes need to have a gini index larger than this value.
        max_rk (int): rank cutoff, include genes if they rank ``<= max_rank`` among all tissues.
        max_rel_rk (float): rank cutoff, include genes if they rank <= max_rel_rk * m among all genes
            in the current sample. Default: .33, i.e. genes need to appear in the first third of the sample.
        min_expr (float): genes need to have at least an expression ``>= min_expr`` to be included.
        aggregate_fun (function): function used to aggregate samples of the same tissue.
    """

    def __init__(
        self,
        expr,
        target,
        min_gini=0.7,
        max_rk=3,
        min_expr=1,
        max_rel_rk=0.33,
        aggregate_fun=np.median,
    ):
        super().__init__(expr, target)
        self.min_gini = min_gini
        self.max_rk = max_rk
        self.min_expr = min_expr
        self.aggregate_fun = aggregate_fun
        self.max_rel_rk = max_rel_rk

    def _mk_signatures(self, expr, target):
        df_aggr = collapse_matrix(
            expr, target, axis=1, aggregate_fun=self.aggregate_fun
        )
        return get_gini_signatures(
            df_aggr,
            min_gini=self.min_gini,
            max_rk=self.max_rk,
            min_expr=self.min_expr,
            max_rel_rk=self.max_rel_rk,
        )

    def get_rogini_format(self):
        df_aggr = collapse_matrix(
            self.expr, self.target, axis=1, aggregate_fun=self.aggregate_fun
        )
        return get_rogini_format(
            df_aggr, min_gini=self.min_gini, max_rk=self.max_rk, min_expr=self.min_expr
        )
