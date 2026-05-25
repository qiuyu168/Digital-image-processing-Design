# 本文件用于将 geometry 目录初始化为 Python 包，并导出所有几何变换算法

from .resize import run as resize_run, ALGORITHM_META as resize_meta
from .rotate import run as rotate_run, ALGORITHM_META as rotate_meta
from .translate import run as translate_run, ALGORITHM_META as translate_meta
from .affine import run as affine_run, ALGORITHM_META as affine_meta
from .perspective import run as perspective_run, ALGORITHM_META as perspective_meta

# 算法注册表：供后端统一调用
ALGORITHMS = {
    "resize": {
        "run": resize_run,
        "meta": resize_meta
    },
    "rotate": {
        "run": rotate_run,
        "meta": rotate_meta
    },
    "translate": {
        "run": translate_run,
        "meta": translate_meta
    },
    "affine": {
        "run": affine_run,
        "meta": affine_meta
    },
    "perspective": {
        "run": perspective_run,
        "meta": perspective_meta
    }
}

def get_algorithm(name: str):
    """根据算法名称获取对应的 run 函数和元数据"""
    return ALGORITHMS.get(name)

def list_algorithms():
    """返回所有算法名称列表"""
    return list(ALGORITHMS.keys())