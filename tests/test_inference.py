import os
import numpy as np

from PIL import Image
from src.util import get_model, get_pil_image_from_path, get_base_model_name, \
    resize_image, get_input_shape
from src.inference import make_inference_from_image, FOODS

INPUT_SIZE = None


def test_get_model():
    # path wrangling for CI/CD pipeline
    path = os.getcwd()

    model = get_model(path)
    # checks output shape
    assert model.layers[-1].output_shape[1] == len(FOODS)
    # checks if model is indeed frozen
    assert model.trainable is False
    print("test_get_model passed!")


def test_resize_image():
    path = os.getcwd()

    image = get_pil_image_from_path(path + "/tests/test_image.jpg")
    resized_image = resize_image(image, (224, 124))  # (width*height) input
    # (height*width) output
    assert (resized_image.shape[2], resized_image.shape[1]) == (224, 124)
    print("test_resize_image passed!")


def test_get_input_shape():
    path = os.getcwd()

    model = get_model(path)
    input_shape = get_input_shape(model)
    assert input_shape == (224, 224, 3)
    print("test_get_input_shape passed!")


def test_make_inference_from_image():
    path = os.getcwd()

    model = get_model(path)
    image = get_pil_image_from_path(path + "/tests/test_image.jpg")
    resized_image = resize_image(image, get_input_shape(model))
    inference, prob, food_probs = make_inference_from_image(model,
                                                            resized_image)
    # checks output type
    assert type(inference) == str
    assert inference == "chilli_crab"
    assert 0 <= prob <= 1
    assert type(food_probs) == dict
    print("test_make_inference_from_image passed!")


def test_get_base_model_name():
    path = os.getcwd()

    model = get_model(path)
    name = get_base_model_name(model)
    # checks output type
    assert type(name) == str
    assert name == "resnet50v2"
    print("test_get_base_model_name passed!")

