# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Common uniform samplers.
"""

# Imports
import collections
from torch.utils.data.sampler import Sampler


class UniformLabelSampler(Sampler):
    """ Samples elements uniformely accross pseudo labels.
    """
    def __init__(self, data_array):
        """ Init class.

        Parameters
        ----------
        data_array: ArrayDataset
            the train data array that contains the pseudo labels.
        """
        self.n_samples = len(data_array)
        self.data_array = data_array
        self.indexes = self.generate_indexes_epoch()

    def generate_indexes_epoch(self):
        """ Generate sampling indexes.
        """
        labels = self.data_array.labels
        clusters_to_images = self.get_clusters(labels)
        n_non_empty_clusters = len(clusters_to_images)
        size_per_pseudolabel = int(self.n_samples / n_non_empty_clusters) + 1
        res = np.array([])
        for name, cluster_indexes in clusters_to_images.items():
            indexes = np.random.choice(
                cluster_indexes, size_per_pseudolabel,
                replace=(len(cluster_indexes) <= size_per_pseudolabel))
            res = np.concatenate((res, indexes))
        np.random.shuffle(res)
        res = list(res.astype("int"))
        if len(res) >= self.n_samples:
            return res[:self.n_samples]
        res += res[: (self.n_samples - len(res))]
        return res

    def get_clusters(self, labels):
        """ Get indexes associated to each cluster.
        """
        tally = collections.defaultdict(list)
        for idx, item in enumerate(labels):
            tally[item].append(idx)
        return tally

    def __iter__(self):
        return iter(self.indexes)

    def __len__(self):
        return len(self.indexes)
