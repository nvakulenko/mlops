# mlops
# HW-1
- Model Generated in Colab is here /model/cats+dogs/export.pkl
- DVC repository for the project can be viewed https://studio.iterative.ai/user/nvakulenko/views/mlops-ipnrhig5ui
- Data set is extended with rabbits 200 images and added to existing data set with rabbit_ prefix
- Model regenerated with 'rabbits' class can be found here: /model/+rabbits/export.pkl
- REST API Wrapper for model is in /app folder
- Model wrapped with rest API and deployed in Docker is in Docker.file
- AutoML:
  - model generated with help of lobe.ai can be found in /lobeio directory  
  - code for generating auto-keras can be found in /autokeras directory

# HW-2
- ML pipeline: /airflow/dags/1_machine_learning.py: train and export model to 'export.pkl'
- Manual: Build docker image with wrapped model 'export.pkl' in flask REST service: docker build . -t cats_dogs_rabbits_fastai_model_image 
- Verification pipeline: /airflow/dags/3_verification_pipeline.py
  - mually prepare images for verification and put them into /data/to_predict directory
  - from DAG: 
    - start docker image 'cats_dogs_rabbits_fastai_model_image' 
    - interare over .jpg images in /data/to_predict
    - put into /predicted/recognized/ folder images with prediction >= 90%
    - put into /predicted/unrecognized/ folder images with prediction < 90%
- Manually: label unrecognized images and put them into /data/training folder
- retrain model with /airflow/dags/1_machine_learning.py


# HW-3
- Manual deploying with Seldon
  - use tensorflow model generated with lobe.io from /lobeai/model_TensorFlow can be found in /seldon/tensorflow folder
  - a try to wrap fastai model generated in HW-1 is in /seldon/fastai folder
  - more details in /seldon/README.md