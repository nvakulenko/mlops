import os

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from fastai.vision import *
from fastai.metrics import error_rate


def _train_and_export_model():
    path_img = '/data/training'
    fnames = get_image_files(path_img)
    data = ImageDataBunch.from_name_re(path_img, fnames, pat, ds_tfms=get_transforms(), size=224, bs=64).normalize(imagenet_stats)
    learn = cnn_learner(data, models.resnet34, metrics=error_rate)
    learn.fit_one_cycle(4)
    learn.export(os.path.abspath('/model/export.pkl'))


with DAG("training", schedule_interval="@daily", start_date=days_ago(1)) as dag:

    # here can be any data preparation operations
    preprocess_data = DummyOperator(task_id="preprocess_data")

    train_and_export_model = PythonOperator(
        task_id="train_model",
        python_callable=_train_and_export_model
    )

    preprocess_data >> train_and_export_model