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
"""Provides conversion functions to generate a CZANN from exported TensorFlow models."""
import os
import sys
from typing import Tuple, Union, Sequence, Optional, TYPE_CHECKING, List, Any

from tensorflow.keras import Model
from tensorflow.keras.models import load_model  # pylint: disable=no-name-in-module # Caused by TensorFlow

from czmodel.model_metadata import ModelSpec
from czmodel.util import keras_to_czann
from czmodel.util.argument_parsing import dir_file

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    # no-name-in-module is caused by issues in the TensorFlow code base
    from tensorflow.keras.layers import Layer  # noqa: F401  # pylint: disable=no-name-in-module,ungrouped-imports


def convert_from_model_spec(
    model_spec: ModelSpec,
    output_path: str,
    output_name: str = "DNNModel",
    spatial_dims: Optional[Tuple[int, int]] = None,
    preprocessing: Union["Layer", Sequence["Layer"]] = None,
    postprocessing: Union["Layer", Sequence["Layer"]] = None,
) -> None:
    """Convert a TensorFlow Keras model to a czann model usable in ZEN Intellesis.

    Args:
        model_spec: A ModelSpec object describing the specification of the CZANN to be generated.
        output_path: A folder to store the generated CZANN file.
        output_name: The name of the generated .czann file.
        spatial_dims: New spatial dimensions for the input node (see final usage for more details)
        preprocessing: A sequence of layers to be prepended to the model. (see final usage for more details)
        postprocessing: A sequence of layers to be appended to the model. (see final usage for more details)
    """
    # Create output directory
    os.makedirs(output_path, exist_ok=True)

    # Load model if necessary
    model = (
        model_spec.model
        if isinstance(model_spec.model, Model)
        else load_model(model_spec.model)
    )

    # Convert model
    keras_to_czann.convert(
        model=model,
        model_metadata=model_spec.model_metadata,
        license_file=model_spec.license_file,
        output_path=os.path.join(output_path, output_name),
        spatial_dims=spatial_dims,
        preprocessing=preprocessing,
        postprocessing=postprocessing,
    )


def convert_from_json_spec(
    model_spec_path: str,
    output_path: str,
    output_name: str = "DNNModel",
    spatial_dims: Optional[Tuple[int, int]] = None,
    preprocessing: Union["Layer", Sequence["Layer"]] = None,
    postprocessing: Union["Layer", Sequence["Layer"]] = None,
) -> None:
    """Converts a TensorFlow Keras model specified in a JSON metadata file to a czann model.

    Args:
        model_spec_path: The path to the JSON specification file.
        output_path: A folder to store the generated CZANN file.
        output_name: The name of the generated .czann file.
        spatial_dims: New spatial dimensions for the input node (see final usage for more details)
        preprocessing: A sequence of layers to be prepended to the model. (see final usage for more details)
        postprocessing: A sequence of layers to be appended to the model. (see final usage for more details)
    """
    # Parse the specification JSON file
    parsed_spec = ModelSpec.from_json(model_spec_path)

    # Write czann model to disk
    convert_from_model_spec(
        parsed_spec,
        output_path,
        output_name,
        spatial_dims=spatial_dims,
        preprocessing=preprocessing,
        postprocessing=postprocessing,
    )


def parse_args(args: List[str]) -> Any:
    """Parses all arguments from a given collection of system arguments.

    Arguments:
        args: The system arguments to be parsed.

    Returns:
        The parsed system arguments.
    """
    # Import argument parser
    import argparse  # pylint: disable=import-outside-toplevel

    # Define expected arguments
    parser = argparse.ArgumentParser(
        description="Convert a TensorFlow saved_model or ONNX model to a CZANN that can be executed inside ZEN."
    )
    parser.add_argument(
        "model_spec",
        type=dir_file,
        help="A JSON file containing the model specification.",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="The path where the generated czann model will be created.",
    )
    parser.add_argument(
        "output_name", type=str, help="The name of the generated czann model."
    )
    parser.add_argument(
        "--license_file", type=str, help="An optional license file to be included in the generated czann model."
    )

    # Parse arguments
    return parser.parse_args(args)


def main() -> None:
    """Console script to convert a TensorFlow Keras model to a CZANN."""
    args = parse_args(sys.argv[1:])

    # Run conversion
    convert_from_json_spec(args.model_spec, args.output_path, args.output_name)


if __name__ == "__main__":
    main()
