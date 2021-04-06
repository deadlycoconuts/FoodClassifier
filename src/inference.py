import os
import argparse
import numpy as np
import tensorflow as tf

from src.util import get_model, get_pil_image_from_path, get_input_shape, \
    resize_image


FOODS = ['chilli_crab',
         'curry_puff',
         'dim_sum',
         'ice_kacang',
         'kaya_toast',
         'nasi_ayam',
         'popiah',
         'roti_prata',
         'sambal_stingray',
         'satay',
         'tau_huay',
         'wanton_noodle']

parser = argparse.ArgumentParser()


def make_inference_from_image(model, image):
    """
    Uses the model provided to predict the image class of the image
    provided. Returns the image class, the probability of it being that
    class, as well as a dictionary containing all the other possible classes
    and their respective probabilities.

    Args:
        model (tf.keras.Model): a classification model
        image (np.ndarray): an ndarray containing an image

    Returns:
        image_class (str): the predicted image class
        prob (float): the probability that the image belongs to image_class
        food_probs (dict): key-value pairs of (image class, probability) for
        all classes
    """
    output = model.predict(image)
    probas = np.squeeze(tf.nn.softmax(output, axis=1), axis=0)

    image_class = FOODS[np.argmax(np.squeeze(output, axis=0))]
    prob = round(np.max(probas), 2)

    food_probs = dict()
    for i in range(len(FOODS)):
        food_probs[FOODS[i]] = str(round(probas[i], 4))
    return image_class, prob, food_probs


if __name__ == "__main__":
    # args = parser.parse_known_args()
    parser.add_argument('image_file_name', nargs='?', default=None)
    args = parser.parse_args()

    if args.image_file_name is None:
        raise Exception("No image specified!")

    # path wrangling for CI/CD pipeline
    path = os.getcwd()
    if path[-15:] == "all-assignments":
        path = path + "/assignment7"

    saved_model = get_model(path)
    saved_image = get_pil_image_from_path(args.image_file_name)
    saved_image = resize_image(saved_image, get_input_shape(saved_model))

    result = make_inference_from_image(saved_model, saved_image)
