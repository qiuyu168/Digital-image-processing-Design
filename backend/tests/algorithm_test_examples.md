# 本文件用于提供常见后端算法的本地测试配置示例。

以下示例都使用规范导入路径。运行前请先准备测试图片：

```bat
backend\data\test_images\anime_test.png
```

运行方式：

```bat
cd backend
python tests/manual_test_algorithm.py
```

也可以使用 JSON 配置：

```bat
python tests/manual_test_algorithm.py --config tests/sample_test_configs/grayscale_example.json
```

## 1. 灰度化

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.gray_transform.grayscale"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/grayscale_result.png"
PARAMS = {}
```

## 2. 二值阈值

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.gray_transform.binary_threshold"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/binary_threshold_result.png"
PARAMS = {
    "threshold": 127
}
```

## 3. 饱和度调整

规范算法文件是 `hsv_adjust.py`，测试导入路径统一使用 `app.algorithms.color_processing.hsv_adjust`。

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.color_processing.hsv_adjust"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/hsv_adjust_result.png"
PARAMS = {
    "saturation_factor": 1.5,
    "value_factor": 1.0,
    "hue_shift": 0
}
```

## 4. 高斯滤波

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.spatial_filter.gaussian_filter"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/gaussian_filter_result.png"
PARAMS = {
    "kernel_size": 5,
    "sigma": 1.0
}
```

## 5. Canny 边缘检测

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.edge_detection.canny"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/canny_result.png"
PARAMS = {
    "threshold1": 80,
    "threshold2": 160,
    "blur_size": 3
}
```

## 6. 傅里叶频谱显示

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.frequency_filter.dft_spectrum"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/dft_spectrum_result.png"
PARAMS = {}
```

## 7. 理想低通滤波

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.frequency_filter.ideal_low_pass"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/ideal_low_pass_result.png"
PARAMS = {
    "radius": 30
}
```

## 8. 理想高通滤波

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.frequency_filter.ideal_high_pass"
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/ideal_high_pass_result.png"
PARAMS = {
    "radius": 30
}
```

## 9. ??????

???????????????????????????????????

```python
app.algorithms.gray_transform.grayscale
app.algorithms.color_processing.hsv_adjust
app.algorithms.frequency_filter.dft_spectrum
```
