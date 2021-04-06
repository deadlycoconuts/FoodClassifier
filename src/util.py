import re
import base64
import numpy as np
import tensorflow as tf

from tensorflow import keras
from PIL import Image
from io import BytesIO


MODEL_NAME = "/model_weights.h5"


def get_model(model_file_path):
    """
    Returns a Keras model with its weights initialised when given a file path
    leading to a .h5 file.

    Args:
        model_file_path (str): string containing the file path of the model

    Returns:
        model (tf.keras.Model): a Keras model with its weights initialised
    """
    model_file_path = model_file_path + MODEL_NAME
    model = keras.models.load_model(filepath=model_file_path)
    model.trainable = False
    return model


def get_pil_image_from_path(image_file_path):
    """
    Returns a PIL image when given a file path leading to an image file.

    Args:
        image_file_path (str): string containing the file path of the image

    Returns:
        pil_image (PIL.Image): a PIL image
    """
    # note that input shape has been modified to not include the batch number
    # dimension
    pil_image = Image.open(image_file_path)
    return pil_image


def resize_image(image, input_shape):
    """
    Returns a resized image as a numpy ndarray given a PIL image and a desired
    input shape entered as a tuple (width, height).

    Args:
        image (PIL.Image): a PIL image to be resized
        input_shape (tuple): a tuple containing the desired image
        dimensions in the form (width, height)

    Returns:
        image (numpy.ndarray): a numpy tensor containing the resized image
        in the dimensions (1, height, width, channels)
    """
    image = image.resize((input_shape[0], input_shape[1]))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


def get_input_shape(model):
    """
    Returns the input shape of a model.

    Args:
        model (tf.keras.Model): the model whose input we would like to get

    Returns:
        input_shape (tuple): a tuple containing the input shape dimensions
        in the form (channels, width, height)
    """
    input_shape = model.layers[0].output_shape[0]
    input_shape = (input_shape[1], input_shape[2], input_shape[3])
    return input_shape


def get_base_model_name(model):
    """
    Returns the name of the base model of the model given in a string.

    Args:
        model (tf.keras.Model): the model whose base model name we would
        like to get

    Returns:
        name (str): a string containing the name of the base model
    """
    name = model.layers[3].name
    return name


def base64_to_pil(img_base64):
    """
    Returns a PIL image from a base64 radix representation of an image.

    Args:
        img_base64 (str): the base64 radix string representing an image

    Returns:
        pil_image (PIL.Image): a PIL image
    """
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data))).convert(
        'RGB')
    return pil_image


def capitalize_food_probs(food_probs):
    """
    Returns a dictionary of (food_name, prob) key-value pairs with the food
    names capitalised and their underscores removed.

    Used for the front end web application HTTP requests.

    Args:
        food_probs (dict): a dictionary containing key-value pairs of food
        name predictions and their corresponding prediction probabilities

    Returns:
        new_dict (dict): a dictionary containing key-value pairs of food
        name predictions capitalised and their prediction probabilities
    """
    new_dict = {}
    for key in food_probs.keys():
        new_word = " ".join(word.capitalize() for word in key.split("_"))
        new_dict[new_word] = food_probs[key]
    return new_dict
