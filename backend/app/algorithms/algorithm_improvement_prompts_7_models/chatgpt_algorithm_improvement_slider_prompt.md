# ChatGPT Prompt: Improve One Backend Image Processing Algorithm With Frontend Slider Parameters

## Model-Specific Instruction

You are ChatGPT acting as a senior Python + OpenCV backend engineer.
Provide a balanced improvement: readable code, correct algorithm behavior, safe defaults, boundary handling, local-test compatibility, and slider-ready parameter metadata.


## Project Context

Repository: `https://github.com/qiuyu168/Digital-image-processing-Design`

The project is an interactive digital image processing system based on anime image recognition.

Backend stack:

- Python >= 3.11
- FastAPI
- OpenCV complete package: `opencv-contrib-python`
- NumPy
- Pillow
- SciPy
- scikit-image
- Windows 11 local development
- No Docker
- No database
- No large deep learning model dependency

The backend algorithm layer is organized into 6 categories and 29 algorithm files.

---

## Required Image Upload and Processing Specification

All algorithms must assume that input images have already passed the upload validation rules below.

| Item | Required Rule |
|---|---|
| Supported formats | `jpg`, `jpeg`, `png`, `bmp`, `webp`, `tif`, `tiff` |
| Unsupported formats | `gif`, `mp4`, `avi`, `heic`, `raw`, `psd` |
| Minimum file size | 10 KB |
| Maximum file size | 5 MB |
| Minimum resolution | 128 x 128 |
| Maximum resolution | 4096 x 4096 |
| Backend internal image format | OpenCV BGR + `uint8` |
| Invalid image handling | Reject before algorithm processing |

Algorithm-level assumptions:

1. The algorithm receives a decoded OpenCV image as `numpy.ndarray`.
2. The image is usually BGR and `uint8`.
3. The algorithm must still validate `image is not None`.
4. The algorithm must handle both color and grayscale inputs safely when possible.
5. The algorithm must not read upload files directly.
6. The algorithm must not perform upload validation itself unless absolutely necessary.
7. The algorithm must not resize, reject, or alter image dimensions unless this is its actual algorithm purpose.

---

## Required Algorithm Directory and File List

The algorithm files are organized under `backend/app/algorithms/`.

```text
grayscale_image/
  grayscale.py
  binary_threshold.py
  histogram_equalization.py
  edge_detection_basic.py
  erode.py
  dilate.py
  open_operation.py
  close_operation.py

color_image/
  color_space_convert.py
  saturation_adjust.py
  anime_color_enhance.py
  dominant_color_extract.py

geometric_transform/
  resize.py
  rotate.py
  flip.py

spatial_filter/
  mean_filter.py
  gaussian_filter.py
  median_filter.py
  bilateral_filter.py
  laplacian_sharpen.py

frequency_analysis/
  dft_spectrum.py
  spectrum_shift.py
  magnitude_spectrum.py

frequency_filter/
  low_pass_filter.py
  high_pass_filter.py
  ideal_low_pass.py
  ideal_high_pass.py
  gaussian_low_pass.py
  gaussian_high_pass.py
```

Do not create extra algorithm files beyond this list.

---

## Required Algorithm File Standard

Every algorithm file must satisfy:

1. The first line must be a Chinese function description comment.
2. The file must define `ALGORITHM_META`.
3. The file must define `run(image, params)`.
4. `run(image, params)` must return a dictionary.
5. The return dictionary must contain `result`, `steps`, `metrics`, and `analysis`.
6. `result` must be a `numpy.ndarray`.
7. `steps` must be a list of dictionaries.
8. Each step must contain `name` and `image`.
9. `metrics` must be a dictionary.
10. `analysis` must be a Chinese string.
11. The algorithm must not use `cv2.imshow()`.
12. The algorithm must not use personal absolute paths.
13. The algorithm must not save files by itself.
14. The algorithm must not call FastAPI or frontend code.
15. The algorithm must not introduce a database, Docker, or model dependency.

Standard return format:

```python
return {
    "result": result_image,
    "steps": [
        {"name": "step name", "image": step_image}
    ],
    "metrics": {},
    "analysis": "Chinese analysis text."
}
```

---

## Frontend Slider Parameter Compatibility Requirement

The frontend will generate draggable numeric sliders and other parameter controls automatically from `ALGORITHM_META["params"]`.

Therefore, every adjustable parameter in every algorithm file must provide complete frontend-readable metadata.

### Required Parameter Metadata Format

Each parameter must follow this format:

```python
"parameter_name": {
    "type": "float",
    "default": 1.5,
    "min": 0.0,
    "max": 3.0,
    "step": 0.1,
    "label": "饱和度系数",
    "component": "slider"
}
```

### Required Fields

| Field | Required | Purpose |
|---|---|---|
| `type` | Yes | Tells frontend how to parse value. Allowed: `int`, `float`, `odd_int`, `select`, `bool`. |
| `default` | Yes | Initial value shown in frontend. Also used by local tests. |
| `min` | Required for numeric params | Minimum slider value. |
| `max` | Required for numeric params | Maximum slider value. |
| `step` | Required for numeric params | Slider step size. |
| `label` | Yes | Chinese display name in frontend parameter panel. |
| `component` | Yes | Frontend control type. Allowed: `slider`, `select`, `switch`, `input`. |

### Numeric Slider Rules

Use `component: "slider"` for numeric parameters.

Examples:

```python
"threshold": {
    "type": "int",
    "default": 127,
    "min": 0,
    "max": 255,
    "step": 1,
    "label": "阈值",
    "component": "slider"
}
```

```python
"kernel_size": {
    "type": "odd_int",
    "default": 5,
    "min": 1,
    "max": 31,
    "step": 2,
    "label": "滤波核大小",
    "component": "slider"
}
```

```python
"sigma": {
    "type": "float",
    "default": 1.0,
    "min": 0.0,
    "max": 10.0,
    "step": 0.1,
    "label": "高斯标准差",
    "component": "slider"
}
```

### Select Rules

Use `component: "select"` for categorical parameters.

Example:

```python
"mode": {
    "type": "select",
    "default": "horizontal",
    "options": [
        {"label": "水平翻转", "value": "horizontal"},
        {"label": "垂直翻转", "value": "vertical"},
        {"label": "中心翻转", "value": "both"}
    ],
    "label": "翻转方向",
    "component": "select"
}
```

### Switch Rules

Use `component: "switch"` for boolean parameters.

Example:

```python
"preserve_size": {
    "type": "bool",
    "default": True,
    "label": "保持原图尺寸",
    "component": "switch"
}
```

### Important Frontend Compatibility Rules

1. Do not omit `default`.
2. Do not omit `step` for numeric slider parameters.
3. Do not use raw Python-only objects in `ALGORITHM_META`.
4. `ALGORITHM_META` must be JSON-serializable.
5. Parameter names must match exactly what `run(image, params)` reads.
6. `run(image, params)` must use the same defaults as `ALGORITHM_META`.
7. Backend must still clamp and validate values even if frontend uses sliders.
8. Do not trust frontend input blindly.
9. If a parameter should not be adjusted by frontend, do not put it in `ALGORITHM_META["params"]`.
10. Avoid too many parameters. Prefer 1-4 core adjustable parameters per algorithm.

### Example: Saturation Adjustment

Correct metadata:

```python
ALGORITHM_META = {
    "module": "color_image",
    "name": "saturation_adjust",
    "display_name": "饱和度调整",
    "description": "调整动漫图像色彩鲜艳程度，使人物和场景颜色更突出。",
    "params": {
        "saturation_factor": {
            "type": "float",
            "default": 1.5,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "饱和度系数",
            "component": "slider"
        }
    }
}
```

The corresponding `run` function must read:

```python
factor = params.get("saturation_factor", 1.5)
```

Then validate and clamp it again on the backend.

### API Compatibility Requirement

The `/api/algorithms` endpoint must be able to return the full `ALGORITHM_META`, including all parameter metadata, so that the frontend can generate sliders dynamically.

The `/api/process/run` endpoint must accept the current frontend parameter values through:

```json
{
  "module": "color_image",
  "algorithm": "saturation_adjust",
  "params": {
    "saturation_factor": 2.0
  }
}
```

The backend must pass `params` directly into:

```python
run(image, params)
```

---

## Algorithm Generation Restrictions

When improving one algorithm file:

1. Modify only the target algorithm file unless a tiny shared helper import is already available and safe to use.
2. Do not refactor the whole backend.
3. Do not rename files.
4. Do not move files.
5. Do not change public interfaces.
6. Do not change `manual_test_algorithm.py` unless explicitly asked.
7. Do not change frontend files.
8. Do not add optional algorithms.
9. Do not add new packages to `requirements.txt` unless absolutely necessary.
10. Prefer OpenCV + NumPy implementations.
11. Keep implementation readable for undergraduate team members.
12. Keep algorithm parameters simple and configurable through `ALGORITHM_META`.
13. Add safe defaults for all parameters.
14. Clamp all numeric parameters to valid ranges.
15. Convert output image to display-safe `uint8` when needed.
16. Preserve image shape unless the algorithm is a geometric transform.
17. Keep step images meaningful and not excessive.
18. Include useful metrics for debugging and reports.
19. Write `analysis` as a clear Chinese explanation of the effect.
20. Ensure local testing works through `backend/tests/manual_test_algorithm.py`.

---

## Boundary Conditions Required for All Algorithms

Every algorithm must handle or clearly guard against:

1. `image is None`.
2. `params is None`.
3. Missing parameter keys.
4. Invalid numeric parameter values.
5. Parameters outside expected ranges.
6. Even kernel sizes where odd kernel sizes are required.
7. Grayscale input image.
8. BGR color input image.
9. Alpha channel input image if it appears.
10. Very dark images.
11. Very bright images.
12. Low-contrast images.
13. Small valid images, such as 128 x 128.
14. Large valid images, up to 4096 x 4096.
15. Non-contiguous NumPy arrays.
16. Float intermediate values.
17. Overflow or underflow after computation.
18. Division by zero.
19. Empty masks or all-zero masks when relevant.
20. Frequency-domain log operations with zero values.
21. Morphology kernels with invalid size.
22. Geometric transforms that create empty output dimensions.
23. Output dtype not equal to `uint8`.
24. Output values outside 0 to 255.
25. Step images that are not NumPy arrays.

---

## Category-Specific Boundary Notes

### Grayscale Image Algorithms

Applies to `grayscale.py`, `binary_threshold.py`, `histogram_equalization.py`, `edge_detection_basic.py`, `erode.py`, `dilate.py`, `open_operation.py`, and `close_operation.py`.

Requirements:

1. Convert BGR to grayscale when needed.
2. Do not assume input is already grayscale.
3. Threshold values must stay in `[0, 255]`.
4. Morphology kernel size must be positive and odd.
5. Morphology operations should create binary or grayscale-safe results.
6. Edge detection should include optional blur and threshold handling.
7. Histogram equalization should handle grayscale and color inputs safely.

### Color Image Algorithms

Applies to `color_space_convert.py`, `saturation_adjust.py`, `anime_color_enhance.py`, and `dominant_color_extract.py`.

Requirements:

1. Handle BGR input correctly.
2. Avoid RGB/BGR confusion.
3. HSV values must be clamped to OpenCV ranges.
4. Saturation and brightness factors must be bounded.
5. Dominant color extraction should avoid too many clusters.
6. Return a displayable color result or a clear visualization image.

### Geometric Transform Algorithms

Applies to `resize.py`, `rotate.py`, and `flip.py`.

Requirements:

1. Width and height must remain positive.
2. Scale factor must be greater than zero.
3. Rotation angle should be bounded, for example `[-360, 360]`.
4. Border handling must be explicit.
5. Preserve dtype and valid pixel range.
6. Flip mode must be limited to valid OpenCV values.

### Spatial Filter Algorithms

Applies to `mean_filter.py`, `gaussian_filter.py`, `median_filter.py`, `bilateral_filter.py`, and `laplacian_sharpen.py`.

Requirements:

1. Kernel size must be positive and odd.
2. Gaussian sigma must be non-negative.
3. Median filter kernel must be odd and greater than 1.
4. Bilateral parameters must be positive.
5. Sharpening must clip output to `[0, 255]`.
6. Avoid excessive blur by limiting kernel size.

### Frequency Analysis Algorithms

Applies to `dft_spectrum.py`, `spectrum_shift.py`, and `magnitude_spectrum.py`.

Requirements:

1. Convert to grayscale first.
2. Use float arrays for DFT calculations.
3. Use `log(1 + magnitude)` to avoid log zero.
4. Normalize spectrum image to `uint8`.
5. Provide meaningful steps such as grayscale, DFT, shifted spectrum, and magnitude spectrum.

### Frequency Filter Algorithms

Applies to `low_pass_filter.py`, `high_pass_filter.py`, `ideal_low_pass.py`, `ideal_high_pass.py`, `gaussian_low_pass.py`, and `gaussian_high_pass.py`.

Requirements:

1. Convert to grayscale first unless color processing is intentionally supported.
2. Radius must be greater than zero.
3. Radius must be smaller than half of the image minimum dimension.
4. Mask dimensions must match DFT dimensions.
5. Inverse transform output must be normalized and converted to `uint8`.
6. Avoid division by zero in Gaussian mask generation.
7. Return both filtered result and useful frequency-domain steps.

---

## Required Local Testing

The implementation must pass local testing with:

```bat
cd backend
python tests/manual_test_algorithm.py
```

The simplified test script requires users to modify only:

```python
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/result.png"
ALGORITHM_IMPORT_PATH = "app.algorithms.<category>.<algorithm_file>"
```

Do not require manual changes to `PARAMS`.

The algorithm must obtain default values from `ALGORITHM_META["params"]`.



## Task

Improve the following target algorithm file.

Fill in these placeholders before running the prompt:

```text
TARGET_ALGORITHM_FILE = "<paste target file path here>"
TARGET_ALGORITHM_NAME = "<paste algorithm display name here>"
TARGET_ALGORITHM_CATEGORY = "<paste category name here>"
```

Example:

```text
TARGET_ALGORITHM_FILE = "backend/app/algorithms/color_image/saturation_adjust.py"
TARGET_ALGORITHM_NAME = "Saturation Adjustment"
TARGET_ALGORITHM_CATEGORY = "color_image"
```

You must:

1. Open and inspect `TARGET_ALGORITHM_FILE`.
2. Preserve useful existing implementation.
3. Ensure the file follows the required algorithm standard.
4. Improve the `run(image, params)` implementation.
5. Add or improve `ALGORITHM_META`.
6. Ensure every adjustable parameter in `ALGORITHM_META["params"]` is frontend-slider-ready.
7. Add `component`, `step`, `min`, `max`, `default`, `type`, and `label` for numeric slider parameters.
8. Add robust backend parameter validation.
9. Ensure `run(image, params)` uses the same defaults defined in `ALGORITHM_META`.
10. Add meaningful `steps`.
11. Add useful `metrics`.
12. Add Chinese `analysis`.
13. Ensure output image is valid and saveable.
14. Ensure local manual test can run successfully.

## Final Response Required

After editing, output a short Chinese summary containing:

1. Modified file path.
2. Algorithm name.
3. Main improvements.
4. Parameter metadata added for frontend sliders.
5. Boundary conditions handled.
6. How to test locally.
7. Any remaining notes.

Do not output a vague response such as "done".
