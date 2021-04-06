# Note that this Dockerfile was intentionally left incomplete.
# Inherit from an appropriate docker image here.

WORKDIR $WORK_DIR

COPY static static
COPY templates templates
COPY src src
COPY model_weights.h5 README.md ./
COPY conda.yml .

# Update the base conda environment using the conda.yml.
RUN conda update -n base -c defaults conda && conda env update -f conda.yml -n base && rm conda.yml

RUN chown -R 1000450000:0 $WORK_DIR

USER $USER

EXPOSE 8000

# Add a line here to run your app
CMD ["python", "src/app.py"]