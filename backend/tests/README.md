# 本文件用于说明后端本地算法测试工具的使用方法。

## 1. 工具用途

`manual_test_algorithm.py` 用于让小组成员在本地单独测试一个图像处理算法文件。它会读取一张本地图片，动态导入指定算法，调用 `run(image, params)`，再把结果图和步骤图保存到本地目录。

这个脚本只用于本地手动测试，不是复杂的 pytest 集成测试。

## 2. 适用对象

后端算法成员、组长和负责接口联调的成员都可以使用它。每个成员在提交自己的算法文件前，应先运行一次本地测试。

## 3. 测试图片位置

建议把测试图片放到：

```bat
backend\data\test_images\
```

例如：

```bat
backend\data\test_images\anime_test.png
```

支持常见格式：`jpg`、`jpeg`、`png`、`bmp`、`tif`、`tiff`、`webp`。

## 4. 算法文件位置

算法文件必须放在规范目录下，例如：

```text
backend/app/algorithms/grayscale_image/grayscale.py
backend/app/algorithms/color_image/saturation_adjust.py
backend/app/algorithms/grayscale_image/edge_detection_basic.py
backend/app/algorithms/grayscale_image/sobel_edge_detection.py
```

不要使用旧版灰度、彩色或频域分析目录，统一使用当前规范分类目录。

## 5. 修改导入路径

打开：

```bat
backend\tests\manual_test_algorithm.py
```

修改：

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.color_image.saturation_adjust"
```

导入路径是 Python 模块路径，不是文件路径。比如文件在：

```text
backend/app/algorithms/grayscale_image/grayscale.py
```

导入路径应写成：

```python
ALGORITHM_IMPORT_PATH = "app.algorithms.grayscale_image.grayscale"
```

## 6. 修改输入和输出路径

输入图片：

```python
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
```

输出图片：

```python
OUTPUT_IMAGE_PATH = "data/test_outputs/result.png"
```

路径建议写相对于 `backend/` 的相对路径，不要写个人电脑绝对路径。

## 7. 参数来源

简化版 `manual_test_algorithm.py` 会根据算法文件中的 `ALGORITHM_META["params"]` 自动读取默认参数，不需要手动修改 `PARAMS`。

需要自定义参数时，使用高级脚本 `manual_test_algorithm_advanced.py`。例如 Sobel：

```python
PARAMS = {
    "direction": "both",
    "kernel_size": 3,
    "scale": 1.0,
    "delta": 0
}
```

不同算法参数不同，例如 Canny：

```python
PARAMS = {
    "threshold1": 80,
    "threshold2": 160,
    "blur_size": 3
}
```

## 8. 运行脚本

在项目根目录进入后端目录：

```bat
cd backend
python tests/manual_test_algorithm.py
```

也可以使用示例配置：

```bat
python tests/manual_test_algorithm_advanced.py --config tests/sample_test_configs/canny_example.json
```

也可以临时传入参数：

```bat
python tests/manual_test_algorithm_advanced.py --algorithm app.algorithms.grayscale_image.sobel_edge_detection --input data/test_images/anime_test.png --output data/test_outputs/sobel_result.png --params "{\"direction\":\"both\",\"kernel_size\":3,\"scale\":1.0,\"delta\":0}"
```

## 9. 查看结果

结果图默认保存在：

```bat
backend\data\test_outputs\
```

如果算法返回了 `steps`，脚本还会生成步骤图目录，例如：

```text
backend/data/test_outputs/result_steps/
```

## 10. 常见错误

`No module named 'app'`：请确认是在 `backend` 目录下运行脚本。

`输入图片不存在`：请确认图片已经放入 `backend/data/test_images/`，并检查文件名和后缀。

`算法模块缺少 ALGORITHM_META`：算法文件没有按统一框架填写元信息。

`算法模块缺少 run(image, params)`：算法文件没有统一入口函数。

`result 字段必须是 numpy.ndarray`：算法不能直接返回路径、字符串或 `None`，必须返回图像数组。

## 11. 提交前检查

提交算法前确认：

```text
□ 算法文件在规范目录下
□ 文件第一行是中文功能说明
□ 文件包含 ALGORITHM_META
□ 文件包含 run(image, params)
□ run 返回 result、steps、metrics、analysis
□ 不使用 cv2.imshow()
□ 不写个人电脑绝对路径
□ 已运行 python tests/manual_test_algorithm.py
□ data/test_outputs/ 中已经生成结果图
□ steps 步骤图可以正常保存
```
