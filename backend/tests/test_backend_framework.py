# 本文件用于验证后端框架接口、服务层和图像处理主流程
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def make_png_bytes(width: int = 160, height: int = 160) -> bytes:
    rng = np.random.default_rng(20260526)
    image = rng.integers(0, 256, size=(height, width, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".png", image)
    assert ok
    payload = encoded.tobytes()
    assert len(payload) > 10 * 1024
    return payload


def make_solid_png_bytes(width: int, height: int) -> bytes:
    image = np.zeros((height, width, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".png", image)
    assert ok
    return encoded.tobytes()


def test_upload_validator_rejects_invalid_files_and_decodes_valid_image() -> None:
    from app.core.upload_validator import (
        decode_image_from_bytes,
        validate_upload_content_type,
        validate_upload_extension,
        validate_upload_file_size,
        validate_uploaded_image,
    )

    payload = make_png_bytes()

    with pytest.raises(ValueError):
        validate_upload_extension("anime.gif")
    with pytest.raises(ValueError):
        validate_upload_content_type("image/gif")
    with pytest.raises(ValueError):
        validate_upload_file_size(1024)

    decoded = decode_image_from_bytes(payload)
    assert decoded.dtype == np.uint8
    assert decoded.shape == (160, 160, 3)

    validated = validate_uploaded_image("anime.png", payload)
    assert validated.shape == decoded.shape


def test_upload_api_validates_rules_and_blocks_path_traversal() -> None:
    from main import app

    with TestClient(app) as client:
        tiny_file = client.post(
            "/api/upload/image",
            files={"file": ("tiny.png", make_solid_png_bytes(160, 160), "image/png")},
        )
        bad_extension = client.post(
            "/api/upload/image",
            files={"file": ("anime.gif", make_png_bytes(), "image/png")},
        )
        oversized = client.post(
            "/api/upload/image",
            files={"file": ("huge.png", b"0" * (5 * 1024 * 1024 + 1), "image/png")},
        )
        low_resolution = client.post(
            "/api/upload/image",
            files={"file": ("small.png", make_png_bytes(64, 64), "image/png")},
        )
        traversal = client.get("/api/upload/preview/%2E%2E/secret.png")

    for response in [tiny_file, bad_extension, oversized, low_resolution, traversal]:
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"]


def test_algorithm_registry_returns_nine_modules_and_preserves_slider_metadata() -> None:
    from app.services.algorithm_registry import get_all_algorithms

    data = get_all_algorithms()
    modules = data["modules"]

    assert [module["module"] for module in modules] == [
        "basic_operation",
        "grayscale_image",
        "color_image",
        "geometric_transform",
        "spatial_filter",
        "frequency_analysis",
        "frequency_filter",
        "image_restoration",
        "edge_shape_detection",
    ]

    color_module = next(module for module in modules if module["module"] == "color_image")
    saturation = next(
        algorithm
        for algorithm in color_module["algorithms"]
        if algorithm["name"] == "saturation_adjust"
    )
    param = saturation["params"]["saturation_factor"]
    assert param["component"] == "slider"
    assert param["min"] == 0.0
    assert param["max"] == 3.0
    assert param["step"] == 0.1

    grayscale_module = next(module for module in modules if module["module"] == "grayscale_image")
    grayscale_names = {algorithm["name"] for algorithm in grayscale_module["algorithms"]}
    assert "edge_detection_basic" not in grayscale_names
    assert "sobel_edge_detection" not in grayscale_names

    edge_module = next(module for module in modules if module["module"] == "edge_shape_detection")
    sobel = next(
        algorithm
        for algorithm in edge_module["algorithms"]
        if algorithm["name"] == "sobel_edge_detection"
    )
    assert sobel["display_name"] == "Sobel边缘检测"
    assert sobel["params"]["kernel_size"]["component"] == "slider"
    assert sobel["params"]["direction"]["component"] == "select"


def test_fastapi_framework_endpoints_upload_and_run_saturation_adjust() -> None:
    from app.core.config import UPLOAD_DIR
    from main import app

    payload = make_png_bytes()
    uploaded_path: Path | None = None

    with TestClient(app) as client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["success"] is True

        algorithms = client.get("/api/algorithms")
        assert algorithms.status_code == 200
        algorithm_payload = algorithms.json()
        assert algorithm_payload["success"] is True
        assert len(algorithm_payload["modules"]) == 9

        category = client.get("/api/algorithms/color-image")
        assert category.status_code == 200
        assert any(
            item["name"] == "saturation_adjust"
            for item in category.json()["algorithms"]
        )

        upload = client.post(
            "/api/upload/image",
            files={"file": ("anime.png", payload, "image/png")},
        )
        assert upload.status_code == 200
        upload_payload = upload.json()
        assert upload_payload["success"] is True
        assert "image_id" not in upload_payload
        image_path = upload_payload["image_path"]
        uploaded_path = UPLOAD_DIR / image_path

        preview = client.get(f"/api/upload/preview/{image_path}")
        assert preview.status_code == 200
        assert preview.headers["content-type"].startswith("image/")

        request_body = {
            "source_type": "upload",
            "image_path": image_path,
            "module": "color_image",
            "algorithm": "saturation_adjust",
            "params": {"saturation_factor": 1.2},
            "return_steps": True,
        }
        processed = client.post("/api/process/run", json=request_body)
        assert processed.status_code == 200
        process_payload = processed.json()
        assert process_payload["success"] is True
        assert process_payload["result_image"].startswith("data:image/png;base64,")
        assert process_payload["steps"]

        category_processed = client.post(
            "/api/algorithms/color-image/run",
            json={
                "source_type": "upload",
                "image_path": image_path,
                "algorithm": "saturation_adjust",
                "params": {"saturation_factor": 1.1},
                "return_steps": False,
            },
        )
        assert category_processed.status_code == 200
        assert category_processed.json()["result_image"].startswith(
            "data:image/png;base64,"
        )
        assert category_processed.json()["steps"] == []

    if uploaded_path and uploaded_path.exists():
        uploaded_path.unlink()


def test_api_errors_are_json_friendly_and_reject_unsupported_mime() -> None:
    from main import app

    with TestClient(app) as client:
        response = client.post(
            "/api/upload/image",
            files={"file": ("anime.png", make_png_bytes(), "image/gif")},
        )

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert "message" in response.json()


def test_category_api_can_run_grayscale_algorithm_after_upload() -> None:
    from app.core.config import UPLOAD_DIR
    from main import app

    uploaded_path: Path | None = None
    with TestClient(app) as client:
        upload = client.post(
            "/api/upload/image",
            files={"file": ("anime.png", make_png_bytes(), "image/png")},
        )
        assert upload.status_code == 200
        image_path = upload.json()["image_path"]
        uploaded_path = UPLOAD_DIR / image_path

        response = client.post(
            "/api/algorithms/grayscale-image/run",
            json={
                "source_type": "upload",
                "image_path": image_path,
                "algorithm": "grayscale",
                "params": {},
                "return_steps": False,
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["module"] == "grayscale_image"
    assert payload["result_image"].startswith("data:image/png;base64,")
    assert payload["steps"] == []

    if uploaded_path and uploaded_path.exists():
        uploaded_path.unlink()


def test_category_api_can_run_sobel_edge_detection_after_upload() -> None:
    from app.core.config import UPLOAD_DIR
    from main import app

    uploaded_path: Path | None = None
    with TestClient(app) as client:
        upload = client.post(
            "/api/upload/image",
            files={"file": ("anime.png", make_png_bytes(), "image/png")},
        )
        assert upload.status_code == 200
        image_path = upload.json()["image_path"]
        uploaded_path = UPLOAD_DIR / image_path

        response = client.post(
            "/api/algorithms/edge-shape-detection/run",
            json={
                "source_type": "upload",
                "image_path": image_path,
                "algorithm": "sobel_edge_detection",
                "params": {
                    "kernel_size": 3,
                    "scale": 1.0,
                    "delta": 0,
                    "direction": "both",
                },
                "return_steps": True,
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["module"] == "edge_shape_detection"
    assert payload["algorithm"] == "sobel_edge_detection"
    assert payload["algorithm_display_name"] == "Sobel边缘检测"
    assert payload["result_image"].startswith("data:image/png;base64,")
    assert payload["steps"]
    assert "edge_ratio" in payload["metrics"]

    if uploaded_path and uploaded_path.exists():
        uploaded_path.unlink()


def test_new_category_routes_and_two_image_processing_work_after_upload() -> None:
    from app.core.config import UPLOAD_DIR
    from main import app

    uploaded_paths: list[Path] = []
    with TestClient(app) as client:
        first_upload = client.post(
            "/api/upload/image",
            files={"file": ("first.png", make_png_bytes(160, 160), "image/png")},
        )
        second_upload = client.post(
            "/api/upload/image",
            files={"file": ("second.png", make_png_bytes(180, 160), "image/png")},
        )
        assert first_upload.status_code == 200
        assert second_upload.status_code == 200
        first_path = first_upload.json()["image_path"]
        second_path = second_upload.json()["image_path"]
        uploaded_paths.extend([UPLOAD_DIR / first_path, UPLOAD_DIR / second_path])

        for route in [
            "/api/algorithms/basic-operation",
            "/api/algorithms/grayscale-image",
            "/api/algorithms/image-restoration",
            "/api/algorithms/edge-shape-detection",
        ]:
            response = client.get(route)
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["algorithms"]

        missing_second = client.post(
            "/api/process/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "module": "basic_operation",
                "algorithm": "add_operation",
                "params": {"alpha": 1.0, "beta": 1.0, "gamma": 0},
                "return_steps": False,
            },
        )
        assert missing_second.status_code == 400
        assert "second" in missing_second.json()["message"].lower()

        two_image = client.post(
            "/api/algorithms/basic-operation/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "second_image_path": second_path,
                "algorithm": "add_operation",
                "params": {"alpha": 1.0, "beta": 1.0, "gamma": 0},
                "return_steps": False,
            },
        )
        assert two_image.status_code == 200
        assert two_image.json()["success"] is True
        assert two_image.json()["module"] == "basic_operation"
        assert two_image.json()["result_image"].startswith("data:image/png;base64,")
        assert two_image.json()["steps"] == []

        not_operation = client.post(
            "/api/algorithms/basic-operation/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "algorithm": "not_operation",
                "params": {},
                "return_steps": False,
            },
        )
        assert not_operation.status_code == 200
        assert not_operation.json()["algorithm"] == "not_operation"

        gamma = client.post(
            "/api/algorithms/grayscale-image/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "algorithm": "gamma_correction",
                "params": {"gamma": 1.2},
                "return_steps": False,
            },
        )
        assert gamma.status_code == 200
        assert gamma.json()["module"] == "grayscale_image"

        motion_blur = client.post(
            "/api/algorithms/image-restoration/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "algorithm": "motion_blur_simulation",
                "params": {"length": 15, "angle": 30},
                "return_steps": False,
            },
        )
        assert motion_blur.status_code == 200
        assert motion_blur.json()["module"] == "image_restoration"

        histogram_matching = client.post(
            "/api/algorithms/grayscale-image/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "second_image_path": second_path,
                "algorithm": "histogram_matching",
                "params": {},
                "return_steps": False,
            },
        )
        assert histogram_matching.status_code == 200
        assert histogram_matching.json()["module"] == "grayscale_image"

        canny = client.post(
            "/api/algorithms/edge-shape-detection/run",
            json={
                "source_type": "upload",
                "image_path": first_path,
                "algorithm": "canny_edge_detection",
                "params": {"threshold1": 80, "threshold2": 160, "blur_size": 5},
                "return_steps": False,
            },
        )
        assert canny.status_code == 200
        assert canny.json()["module"] == "edge_shape_detection"

    for uploaded_path in uploaded_paths:
        if uploaded_path.exists():
            uploaded_path.unlink()


def test_process_request_rejects_legacy_image_id_field() -> None:
    from main import app

    with TestClient(app) as client:
        response = client.post(
            "/api/process/run",
            json={
                "source_type": "upload",
                "image_id": "upload_legacy.png",
                "module": "color_image",
                "algorithm": "saturation_adjust",
                "params": {},
                "return_steps": False,
            },
        )

    assert response.status_code == 422
    assert response.json()["success"] is False


def test_analysis_metrics_can_include_channel_histogram() -> None:
    from app.core.config import UPLOAD_DIR
    from main import app

    uploaded_path: Path | None = None
    with TestClient(app) as client:
        upload = client.post(
            "/api/upload/image",
            files={"file": ("anime.png", make_png_bytes(), "image/png")},
        )
        assert upload.status_code == 200
        image_path = upload.json()["image_path"]
        uploaded_path = UPLOAD_DIR / image_path

        response = client.post(
            "/api/analysis/metrics",
            json={
                "source_type": "upload",
                "image_path": image_path,
                "include_histogram": True,
            },
        )

    assert response.status_code == 200
    metrics = response.json()["metrics"]
    assert metrics["width"] == 160
    assert metrics["height"] == 160
    assert metrics["histogram"]["bins"] == 256
    assert [channel["name"] for channel in metrics["histogram"]["channels"]] == [
        "blue",
        "green",
        "red",
    ]
    assert all(len(channel["values"]) == 256 for channel in metrics["histogram"]["channels"])
    assert all(channel["pixel_count"] == 160 * 160 for channel in metrics["histogram"]["channels"])

    if uploaded_path and uploaded_path.exists():
        uploaded_path.unlink()


def test_bilateral_filter_handles_bgra_float_non_contiguous_image() -> None:
    from app.algorithms.spatial_filter.bilateral_filter import run

    image = np.zeros((160, 180, 4), dtype=np.float32)
    image[:, :, 0] = np.linspace(0.0, 1.0, 180, dtype=np.float32)[None, :]
    image[:, :, 1] = np.linspace(1.0, 0.0, 160, dtype=np.float32)[:, None]
    image[:, :, 2] = 0.5
    image[:, :, 3] = 1.0

    response = run(image[:, ::-1, :], {"diameter": 7, "sigma_color": 50, "sigma_space": 50})

    assert response["result"].dtype == np.uint8
    assert response["result"].shape == (160, 180, 3)
    assert response["steps"][0]["image"].shape == (160, 180, 3)


def test_process_schemas_accept_frontend_display_names_and_reject_image_id() -> None:
    from app.schemas.process_schema import CategoryProcessRequest, ProcessRequest

    request = ProcessRequest(
        source_type="upload",
        image_path="upload_xxx.png",
        second_image_path="upload_yyy.png",
        module="color_image",
        module_display_name="彩色图像类",
        algorithm="saturation_adjust",
        algorithm_display_name="饱和度调整",
        params={"saturation_factor": 1.2},
    )
    assert request.module == "color_image"
    assert request.second_image_path == "upload_yyy.png"
    assert request.module_display_name == "彩色图像类"
    assert request.algorithm_display_name == "饱和度调整"

    category_request = CategoryProcessRequest(
        source_type="upload",
        image_path="upload_xxx.png",
        second_image_path="upload_yyy.png",
        algorithm="saturation_adjust",
        algorithm_display_name="饱和度调整",
    )
    assert category_request.algorithm_display_name == "饱和度调整"

    assert category_request.second_image_path == "upload_yyy.png"

    with pytest.raises(ValidationError):
        ProcessRequest(
            source_type="upload",
            image_id="upload_legacy.png",
            module="color_image",
            algorithm="saturation_adjust",
        )

    with pytest.raises(ValidationError):
        CategoryProcessRequest(
            source_type="upload",
            image_path="upload_xxx.png",
            image_id="upload_legacy.png",
            algorithm="saturation_adjust",
        )


def test_manual_test_script_is_beginner_three_path_version() -> None:
    script = BACKEND_ROOT / "tests" / "manual_test_algorithm.py"
    content = script.read_text(encoding="utf-8")

    assert 'INPUT_IMAGE_PATH = "data/test_images/anime_test.png"' in content
    assert 'OUTPUT_IMAGE_PATH = "data/test_outputs/result.png"' in content
    assert 'ALGORITHM_IMPORT_PATH = "app.algorithms.color_image.saturation_adjust"' in content
    assert "PARAMS =" not in content
    assert "argparse" not in content
    assert "--input" not in content
    assert "--output" not in content
    assert "--params" not in content
    assert "--config" not in content


def test_p0_p1_repository_hygiene_files_are_in_place() -> None:
    project_root = BACKEND_ROOT.parent
    gitignore = (project_root / ".gitignore").read_text(encoding="utf-8")

    assert not (BACKEND_ROOT / "app" / "core" / "algorithm_framework.py").exists()
    assert not (
        BACKEND_ROOT / "app" / "algorithms" / "algorithm_improvement_prompts_7_models"
    ).exists()
    assert (project_root / "docs" / "prompts" / "algorithm_improvement_prompts_7_models").is_dir()
    assert (BACKEND_ROOT / "data" / "uploads" / ".gitkeep").exists()
    assert not list((BACKEND_ROOT / "data" / "uploads").glob("upload_*.png"))

    for required_rule in [
        "__pycache__/",
        "*.py[cod]",
        ".pytest_cache/",
        "backend/data/uploads/*",
        "!backend/data/uploads/.gitkeep",
        "backend/data/outputs/*",
        "!backend/data/outputs/.gitkeep",
        "backend/data/test_outputs/*",
        "!backend/data/test_outputs/.gitkeep",
    ]:
        assert required_rule in gitignore
