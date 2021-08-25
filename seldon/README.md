## Setup for custom wrapper for model from /fastai directory

In order to deploy custom model with seldon one needs to:
- write custom seldon server
- build Docker image with all needed Seldon dependencies
- create kubernetis pod with SeldonDeployment wrapper

Steps to build project from /fastai directory:

- build docker image

   `eval $(minikube -p minikube docker-env)`

   `minikube docker-env`

   `docker build --no-cache -t nvakulenko/my-model:0.1 .`

- start from .yaml

   `kubectl create -f seldon-deploy.yaml`

- forward port (just to not use istio)

   `kubectl port-forward service/seldon-model-example 8000:8000`

- logs

   `kubectl logs deployment.apps/seldon-model-example-0-my-model -c seldon-container-engine`

   `kubectl logs deployment.apps/seldon-model-example-0-my-model -c my-model`

- delete

   `kubectl delete -f seldon-deploy.yaml`

- test prediction
   
   `python3 my-model-client.py http://localhost:8000/api/v0.1/predictions Abissinian_1.jpg`


# seldon-container-engine:

The service orchestrator is a component that is added to your inference graph to:
- Correctly manage the request/response paths described by your inference graph
- Expose Prometheus metrics
- Provide Tracing via Open Tracing
- Add CloudEvent based payload logging


Seldon Core provides an example Helm analytics chart that displays the above Prometheus metrics in Grafana. You can install it with:

`helm install seldon-core-analytics seldon-core-analytics \
   --repo https://storage.googleapis.com/seldon-charts \
   --namespace seldon-system`

Metrics doc:
https://docs.seldon.io/projects/seldon-core/en/v1.1.0/analytics/analytics.html

#### set python home
export PATH="$(pyenv root)/shims:$PATH"