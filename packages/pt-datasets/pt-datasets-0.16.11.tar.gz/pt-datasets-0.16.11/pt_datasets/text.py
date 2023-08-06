# PyTorch Datasets utility repository
# Copyright (C) 2020  Abien Fred Agarap
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Text datasets module"""
from typing import Tuple

import torch

from pt_datasets.datasets.AGNews import AGNews
from pt_datasets.datasets.IMDB import IMDB
from pt_datasets.datasets.TwentyNewsgroups import TwentyNewsgroups
from pt_datasets.datasets.Yelp import Yelp


def load_dataset(
    name: str, vectorizer: str, return_vectorizer: bool, ngram_range: Tuple
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads a text benchmark classification dataset.

    Parameters
    ----------
    name: str
        The name of the dataset to load.
        The following are the supported datasets:
            1. ag_news
            2. 20newsgroups
            3. imdb
            4. yelp
    vectorizer: str
        The vectorizer to use, options: [ngrams | tfidf (default)]
    return_vectorizer: bool
        Whether to return the vectorizer object or not.
    ngram_range: Tuple
        The n-gram range to use.

    Returns
    -------
    Tuple
        train_dataset: torch.utils.data.Dataset
            The training dataset object.
        test_dataset: torch.utils.data.Dataset
            The test dataset object
    """
    if name == "ag_news":
        train_dataset, test_dataset = load_agnews(
            vectorizer=vectorizer,
            return_vectorizer=return_vectorizer,
            ngram_range=ngram_range,
        )
    elif name == "20newsgroups":
        train_dataset, test_dataset = load_20newsgroups(
            vectorizer=vectorizer,
            return_vectorizer=return_vectorizer,
            ngram_range=ngram_range,
        )
    elif name == "yelp":
        train_dataset, test_dataset = load_yelp(
            vectorizer=vectorizer,
            return_vectorizer=return_vectorizer,
            ngram_range=ngram_range,
        )
    elif name == "imdb":
        train_dataset, test_dataset = load_imdb(
            vectorizer=vectorizer,
            return_vectorizer=return_vectorizer,
            ngram_range=ngram_range,
        )
    if return_vectorizer:
        vectorizer = train_dataset.vectorizer
        return train_dataset, test_dataset, vectorizer
    else:
        return train_dataset, test_dataset


def load_agnews(
    vectorizer: str = "tfidf",
    return_vectorizer: bool = False,
    ngram_range: Tuple = (3, 3),
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the AG News dataset.

    Parameters
    ----------
    vectorizer: str
        The vectorizer to use, options: [ngrams | tfidf (default)]
    return_vectorizer: bool
        Whether to return the vectorizer object or not.
    ngram_range: Tuple
        The n-gram range to use.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set
    """
    train_dataset = AGNews(
        train=True,
        vectorizer=vectorizer,
        return_vectorizer=True,
        ngram_range=ngram_range,
    )
    vectorizer = train_dataset.vectorizer
    test_dataset = AGNews(train=False, vectorizer=vectorizer, ngram_range=ngram_range)
    return (train_dataset, test_dataset)


def load_20newsgroups(
    vectorizer: str = "tfidf",
    return_vectorizer: bool = False,
    ngram_range: Tuple = (3, 3),
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the 20newsgroups dataset.

    Parameters
    ----------
    vectorizer: str
        The vectorizer to use, options: [ngrams | tfidf (default)]
    return_vectorizer: bool
        Whether to return the vectorizer object or not.
    ngram_range: Tuple
        The n-gram range to use.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set
    """
    train_dataset = TwentyNewsgroups(
        train=True,
        vectorizer=vectorizer,
        return_vectorizer=True,
        ngram_range=ngram_range,
    )
    vectorizer = train_dataset.vectorizer
    test_dataset = TwentyNewsgroups(
        train=False, vectorizer=vectorizer, ngram_range=ngram_range
    )
    return (train_dataset, test_dataset)


def load_imdb(
    vectorizer: str = "tfidf",
    return_vectorizer: bool = False,
    ngram_range: Tuple = (3, 3),
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the IMDB dataset.

    Parameters
    ----------
    vectorizer: str
        The vectorizer to use, options: [ngrams | tfidf (default)]
    return_vectorizer: bool
        Whether to return the vectorizer object or not.
    ngram_range: Tuple
        The n-gram range to use.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set
    """
    train_dataset = IMDB(
        train=True,
        vectorizer=vectorizer,
        return_vectorizer=True,
        ngram_range=ngram_range,
    )
    vectorizer = train_dataset.vectorizer
    test_dataset = IMDB(vectorizer=vectorizer, train=False, ngram_range=ngram_range)
    return (train_dataset, test_dataset)


def load_yelp(
    vectorizer: str = "tfidf",
    return_vectorizer: bool = False,
    ngram_range: Tuple = (3, 3),
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the Yelp dataset.

    Parameters
    ----------
    vectorizer: str
        The vectorizer to use, options: [ngrams | tfidf (default)]
    return_vectorizer: bool
        Whether to return the vectorizer object or not.
    ngram_range: Tuple
        The n-gram range to use.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set
    """
    train_dataset = Yelp(
        train=True,
        vectorizer=vectorizer,
        return_vectorizer=True,
        ngram_range=ngram_range,
    )
    vectorizer = train_dataset.vectorizer
    test_dataset = Yelp(vectorizer=vectorizer, train=False, ngram_range=ngram_range)
    return (train_dataset, test_dataset)
