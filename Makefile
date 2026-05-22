include .env

DOCKER_REGISTRY=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com


# Docker
auth:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(DOCKER_REGISTRY)

create-repo:
	aws ecr create-repository --repository-name $(FLASK_IMAGE) --region $(AWS_REGION) || true

docker:
	docker build --build-arg PORT=$(PORT) -t $(DOCKER_REGISTRY)/$(FLASK_IMAGE):$(FLASK_VERSION) -f Dockerfile .
	docker push $(DOCKER_REGISTRY)/$(FLASK_IMAGE):$(FLASK_VERSION)
	kubectl rollout restart deployment $(DEPLOYMENT) --namespace=$(NAMESPACE) || true


# Kubernetes and Helm
k8s-init:
	kubectl create namespace $(NAMESPACE) || true

# TODO: Delete original secret first...
# TODO: cron job...
k8s-auth:
	kubectl create secret docker-registry ecr-secret --docker-server=$(DOCKER_REGISTRY) --docker-username=AWS --docker-password=$(DOCKER_PASSWORD) --namespace=$(NAMESPACE)
