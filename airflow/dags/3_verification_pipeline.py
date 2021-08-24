from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

import os
import cv2
import json
import requests


# data/
#   - to_predict/
#   - predicted/
#       -- recognized/
#          --- cats/
#          --- dogs/
#       -- unrecognized/


def _predict_dir(ds, **kwargs):
    to_predict_dir = r'/data/to_predict/'
    predicted_dir = r'/data/predicted/'
    unrecognized_dir = predicted_dir + "unrecognized/"
    recognized_dir = predicted_dir + "recognized/"

    _make_dir(unrecognized_dir)
    _make_dir(recognized_dir)

    for file_name in os.listdir(to_predict_dir):
        prediction = _predict(to_predict_dir + file_name)

        category = prediction[0]
        rank = prediction[1]

        if rank < 0.9:
            os.replace(to_predict_dir + file_name,
                       unrecognized_dir + file_name)
        else:
            _make_dir(recognized_dir + category + "/")
            os.replace(to_predict_dir + file_name,
                       recognized_dir + category + "/" + file_name)


def _make_dir(unrecognized_dir):
    if not os.path.exists(unrecognized_dir):
        os.makedirs(unrecognized_dir)


def _predict(file_path):
    url = 'http://localhost:80/classify-url'
    headers = {'content-type': 'image/png'}

    img = cv2.imread(file_path)
    # encode image as png
    _, img_encoded = cv2.imencode('.png', img)
    # send http request with image and receive response
    response = requests.post(url, data=img_encoded.tostring(), headers=headers)
    # decode response
    response_values = json.loads(response.text)
    print(response_values)
    prediction = response_values['predictions'][0]
    print(prediction)
    return prediction


with DAG("verification", schedule_interval="@daily", start_date=days_ago(1)) as dag:

    start_docker_image = DockerOperator(
        task_id='docker_command_start',
        image='cats_dogs_rabbits_fastai_model_image',
        container_name='cats_dogs_rabbits_fastai_model_container',
        api_version='auto',
        auto_remove=True,
        network_mode="bridge"
    )

    verify = PythonOperator(
        task_id="predict_images_in_dir",
        python_callable=_predict_dir
    )

    start_docker_image >> verify
