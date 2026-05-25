# 本文件用于将 gray_transform 目录初始化为 Python 包，并导出所有灰度变换算法

from .grayscale import run as grayscale_run, ALGORITHM_META as grayscale_meta
from .binary_threshold import run as binary_threshold_run, ALGORITHM_META as binary_threshold_meta
from .linear_transform import run as linear_transform_run, ALGORITHM_META as linear_transform_meta
from .gamma_transform import run as gamma_transform_run, ALGORITHM_META as gamma_transform_meta
from .log_transform import run as log_transform_run, ALGORITHM_META as log_transform_meta
from .histogram_equalization import run as histogram_equalization_run, ALGORITHM_META as histogram_equalization_meta
from .clahe import run as clahe_run, ALGORITHM_META as clahe_meta

# 算法注册表：供后端统一调用
ALGORITHMS = {
    "grayscale": {
        "run": grayscale_run,
        "meta": grayscale_meta
    },
    "binary_threshold": {
        "run": binary_threshold_run,
        "meta": binary_threshold_meta
    },
    "linear_transform": {
        "run": linear_transform_run,
        "meta": linear_transform_meta
    },
    "gamma_transform": {
        "run": gamma_transform_run,
        "meta": gamma_transform_meta
    },
    "log_transform": {
        "run": log_transform_run,
        "meta": log_transform_meta
    },
    "histogram_equalization": {
        "run": histogram_equalization_run,
        "meta": histogram_equalization_meta
    },
    "clahe": {
        "run": clahe_run,
        "meta": clahe_meta
    }
}

def get_algorithm(name: str):
    """根据算法名称获取对应的 run 函数和元数据"""
    return ALGORITHMS.get(name)

def list_algorithms():
    """返回所有算法名称列表"""
    return list(ALGORITHMS.keys())