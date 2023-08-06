import os
import pathlib
from typing import Sequence, Union

import dataframe_image as dfi
import pandas as pd
import structlog
from sklearn.metrics import classification_report

logger = structlog.get_logger()


def classification_report_mlflow(
    y_true: Sequence,
    y_pred: Sequence,
    path: Union[str, pathlib.Path] = None,
    file_name: str = "classification_report.png",
):
    """Get an image output for sklearn classification_report.

    Arguments:
        y_true: True labels for a classification task.
        y_pred: Predicted labels for a classification task.
        path: Location for output image e.g. /Users/<your_name>/Downloads/
        file_name: Name of the output iamge
    """
    if not path:
        path = str(os.getcwd()) + "/" + file_name
    else:
        path = str(path) + file_name
    logger.info("The plot is saved at ", location=path)
    report = classification_report(y_true, y_pred, output_dict=True)
    report = pd.DataFrame(report).T
    report_styled = report.style.background_gradient()
    dfi.export(report_styled, path)
