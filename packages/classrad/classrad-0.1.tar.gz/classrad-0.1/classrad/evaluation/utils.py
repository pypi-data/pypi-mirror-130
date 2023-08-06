import numpy as np
import pandas as pd
from sklearn.metrics import auc, confusion_matrix, roc_curve


def get_youden_threshold(y_test, y_score):
    """
    Returns optimal threshold, as well as TPR and FPR, that maximize the
    difference between TPR and FPR
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    youden_index = [tpr[i] - fpr[i] for i in range(len(tpr))]
    youden_argmax = np.argmax(youden_index)
    you_tpr = tpr[youden_argmax]
    you_fpr = fpr[youden_argmax]
    you_thr = thresholds[youden_argmax]
    print(
        f"Optimal threshold at {you_thr} gives TPR = {you_tpr}, \
          FPR = {you_fpr}"
    )
    return you_fpr, you_tpr, you_thr


def get_optimal_threshold(y_test, y_score):
    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    i = np.arange(len(tpr))
    roc = pd.DataFrame(
        {
            "tf": pd.Series(tpr - (1 - fpr), index=i),
            "threshold": pd.Series(thresholds, index=i),
        }
    )
    roc_t = roc.ix[(roc.tf - 0).abs().argsort()[:1]]
    return list(roc_t["threshold"])


def get_sensitivity_specificity(y_test, y_pred_proba, threshold):
    y_pred = np.where(y_pred_proba > threshold, 1, 0)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    sensitivity = np.round(sensitivity, 3)
    specificity = np.round(specificity, 3)
    return sensitivity, specificity


def common_roc_settings(ax):
    ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="black", alpha=0.8)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend(loc="lower right", fontsize="x-small")


def get_fpr_tpr_auc(y_true, y_pred):
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = np.round(auc(fpr, tpr), 3)
    return fpr, tpr, roc_auc
