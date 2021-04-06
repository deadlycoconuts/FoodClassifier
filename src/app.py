import os
import sys

sys.path.append(os.getcwd())
from flask import Flask, jsonify, request, render_template
#from waitress import serve

from src.inference import make_inference_from_image, FOODS
from src.util import get_model, get_pil_image_from_path, get_input_shape, \
    get_base_model_name, base64_to_pil, resize_image, capitalize_food_probs


app = Flask(__name__,
            template_folder="../templates",
            static_folder="../static")
model = get_model(os.getcwd())


@app.route('/')
def index():
    """
    Renders the template of the one and only page of the web application.

    Returns:
        A call to the render_template method from Flask to display the home
        page of the application
    """
    return render_template("index.html")
    #return "I'm too lazy to find anything interesting for now so I'm leaving \
    #        this blank. Appreciate minimalism."


@app.route('/info', methods=['GET'])  # what's the point of this
def short_description():
    """
    Returns a JSON object containing some simple information of the
    classification model.

    Not used for the web browser interface.

    Returns:
        A JSON object containing information about the model if the GET type
        was correctly specified in the HTTP request, else None
    """
    if request.method == 'GET':
        return jsonify({"model": get_base_model_name(model),
                        "input-size": str(get_input_shape(model)),
                        "num-classes": str(len(FOODS)),
                        "pretrained-on": "ImageNet"})
        # I can only hardcode this
    return None


@app.route('/predict', methods=['POST'])
def predict():
    """
    Takes as input a POST request that contains the image path specified as an
    upload directory.

    Returns the predicted class and probability given the image file path of an
     image containing food in it.

    Not used for the web browser interface.
    Returns:
        A JSON object containing the predicted food class and well as the
        probability that this prediction is believed to be true.

        If the HTTP request method is not POST, return None.
    """
    if request.method == 'POST':
        image = base64_to_pil(request.json)
        image = resize_image(image, get_input_shape(model))

        inference, prob, _ = make_inference_from_image(model, image)
        return jsonify({'food': inference, 'probability': str(prob)})
    return None


@app.route('/gui_predict', methods=['POST'])
def gui_predict():
    """
    Takes as input a jsonified image that has been rendered in its base64
    radix representation.

    Returns a dictionary with key-value pairs of food classes and their
    corresponding prediction values. Capitalises and removes the underscores
    from the names of the food classes for aesthetic purposes.

    Used primarily with the web browser interface.

    Returns:
        A JSON object containing key-value pairs of food classes and their
        probabilities.

        If the HTTP request method is not POST, return None.
    """
    if request.method == 'POST':
        image = base64_to_pil(request.json)
        image = resize_image(image, get_input_shape(model))

        _, _, food_probs = make_inference_from_image(model, image)
        food_probs = capitalize_food_probs(food_probs)
        print(food_probs)
        return jsonify(food_probs)
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
    # For production mode, comment the line above and uncomment below
    #serve(app, host="0.0.0.0", port=8000)
