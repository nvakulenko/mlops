#!/usr/bin/env python3
import io
import logging
import numpy as np
from PIL import Image
from fastai.vision import *
import fastai

logger = logging.getLogger('__mymodel__')

class MyModel(object):
  def __init__(self):
    logger.info("initializing...")
    logger.info("load model here...")
    self._model = load_learner(Path("/model"))
    logger.info("model has been loaded and initialized...")
  def predict(self, X, features_names):
    """ Seldon Core Prediction API """
 
    logger.info("predict called...")
    # Use Pillow to convert to an RGB image then reverse channels.
    logger.info('converting tensor to image')
    img = Image.open(io.BytesIO(X))
    if self._model:
      logger.info("perform inference here...")
      _, _, losses = self._model.predict(img)
      logger.info("Prediction: {}".format(losses))
      logger.info(losses)

    img = img.convert('RGB')
    img = np.array(img)
    img = img[:, :, ::-1]
    logger.info("image size = {}".format(img.shape))
    # This will serialize the image into a JSON tensor
    logger.info("returning prediction...")
    # Return the original image sent in RGB

    return img[:,:,::-1]

    #return SeldonResponse(data=X, metrics=runtime_metrics, tags=runtime_tags)


  #https://github.com/SeldonIO/seldon-core/blob/3aebcac308243324f2ae39dea10b48872836d4eb/python/tests/test_model_microservice.py#L163