# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional

import torch
from torch import Tensor

from torchmetrics.functional.pairwise.euclidean import (
    _pairwise_euclidean_distance_compute, 
    _check_input,
)


def _pairwise_cosine_similarity_update(
    X: Tensor, Y: Optional[Tensor] = None, zero_diagonal: Optional[bool] = None
) -> Tensor:
    """ 
    Calculates the pairwise cosine similarity matrix
    
    Args:
        X: tensor of shape ``[N,d]``
        Y: if provided, a tensor of shape ``[M,d]``
        zero_diagonal: determines if the diagonal should be set to zero
    """
    X, Y, zero_diagonal = _check_input(X, Y, zero_diagonal)

    norm = torch.norm(X, p=2, dim=1)
    X = X / norm.unsqueeze(1)
    norm = torch.norm(Y, p=2, dim=1)
    Y = Y / norm.unsqueeze(1)

    distance = X @ Y.T
    if zero_diagonal:
        distance.fill_diagonal_(0)
    return distance


def pairwise_cosine_similarity(
    X: Tensor, Y: Optional[Tensor] = None, reduction: Optional[str] = None, zero_diagonal: Optional[bool] = None
) -> Tensor:
    r""" 
    Calculates pairwise cosine similarity:
    
    .. math::
        s_{cos}(x,y) = \frac{<x,y>}{||x|| \cdot ||y||} = \frac{\sum_{d=1}^D x_d \cdot y_d }{\sqrt{\sum_{d=1}^D x_i^2} \cdot \sqrt{\sum_{d=1}^D x_i^2}}
    
    If two tensors are passed in, the calculation will be performed
    pairwise between the rows of the tensors. If a single tensor is passed in, the calculation will
    be performed between the rows of that tensor.
    
    Args:
        X: Tensor with shape ``[N, d]``
        Y: Tensor with shape ``[M, d]``, optional
        reduction: reduction to apply along the last dimension. Choose between `'mean'`, `'sum'` 
            (applied along column dimension) or  `'none'`, `None` for no reduction
        zero_diagonal: if the diagonal of the distance matrix should be set to 0. If only `X` is given
            this defaults to `True` else if `Y` is also given it defaults to `False`

    Returns:
        A ``[N,N]`` matrix of distances if only ``X`` is given, else a ``[N,M]`` matrix

    Example:
        >>> import torch
        >>> from torchmetrics.functional import pairwise_cosine_similarity
        >>> x = torch.tensor([[2, 3], [3, 5], [5, 8]], dtype=torch.float32)
        >>> y = torch.tensor([[1, 0], [2, 1]], dtype=torch.float32)
        >>> pairwise_cosine_similarity(x, y)
        tensor([[0.5547, 0.8682],
                [0.5145, 0.8437],
                [0.5300, 0.8533]])
        >>> pairwise_cosine_similarity(x)
        tensor([[0.0000, 0.9989, 0.9996],
                [0.9989, 0.0000, 0.9998],
                [0.9996, 0.9998, 0.0000]])

    """
    distance = _pairwise_cosine_similarity_update(X, Y, zero_diagonal)
    return _pairwise_euclidean_distance_compute(distance, reduction)
