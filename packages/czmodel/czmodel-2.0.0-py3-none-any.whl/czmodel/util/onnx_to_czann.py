# Copyright 2020 Carl Zeiss Microscopy GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provides conversion utility functions."""
from io import BytesIO
from typing import Optional, TYPE_CHECKING
import onnx  # type: ignore

from czmodel.util.model_packing import create_model_zip
from czmodel.util.common import validate_metadata

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    from czmodel.model_metadata import ModelMetadata  # noqa: F401


def convert(model: str, model_metadata: "ModelMetadata", output_path: str, license_file: Optional[str] = None) -> None:
    """Wraps a given ONNX model into a czann container.

    Args:
        model: ONNX model to be converted.
        model_metadata: The metadata required to generate a czann model.
        output_path: Destination path to the .czmodel file that will be generated.
        license_file: Path to a license file.

    Raises:
        ValueError: If the input or output shapes of the model and the meta data do not match.
    """
    # Check if model input and output shape is consistent with provided metadata
    onnx_model = onnx.shape_inference.infer_shapes(onnx.load(model))
    input_shape = [
        dim.dim_value for dim in onnx_model.graph.input[0].type.tensor_type.shape.dim  # pylint: disable=no-member
    ][1:]
    output_shape = [
        dim.dim_value for dim in onnx_model.graph.output[0].type.tensor_type.shape.dim  # pylint: disable=no-member
    ][1:]
    validate_metadata(metadata=model_metadata, model_input_shape=input_shape, model_output_shape=output_shape)

    # Pack model into czann
    with open(model, "rb") as f:
        buffer = BytesIO(f.read())
        create_model_zip(
            model=buffer.getbuffer(),
            model_metadata=model_metadata,
            output_path=output_path,
            license_file=license_file
        )
