r"""Root package info."""
import logging as __logging
import os

from torchmetrics.__about__ import *  # noqa: F401, F403

_logger = __logging.getLogger("torchmetrics")
_logger.addHandler(__logging.StreamHandler())
_logger.setLevel(__logging.INFO)

_PACKAGE_ROOT = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.dirname(_PACKAGE_ROOT)

from torchmetrics.average import AverageMeter  # noqa: E402
from torchmetrics.collections import MetricCollection  # noqa: E402
from torchmetrics.metric import Metric  # noqa: E402


__all__ = [
    "AverageMeter",
    "Metric",
    "MetricCollection",
]
