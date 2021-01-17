.PHONY: deploy build-dev run-dev start-dev

GCP_PROJECT = optimal-courage-279020
GCP_PROJECT_REGION = eu-west2
PROJECT_GCP_CREDENTIALS_FILENAME = ssl-gcloud-credentials


# GCP_PROJECT = colossal-squid
# GCP_PROJECT_REGION = eu-west2
# PROJECT_GCP_CREDENTIALS_FILENAME = prod-gcloud-credentials


NAME = example


set-active-account:
	$(eval EXCO=$(shell gcloud config configurations activate $(PROJECT_GCP_CREDENTIALS_FILENAME); echo $$?))
	if [ $(EXCO) -eq 1 ]; then gcloud config configurations create $(PROJECT_GCP_CREDENTIALS_FILENAME) ; fi;

	gcloud config set project $(GCP_PROJECT)
	gcloud config set functions/region $(GCP_PROJECT_REGION)

	gcloud auth activate-service-account \
	--key-file="/Users/brunomurino/.config/gcp/$(PROJECT_GCP_CREDENTIALS_FILENAME).json"

deploy: set-active-account
	gcloud functions \
	deploy $(NAME) \
	--entry-point entrypoint \
	--source ./$(NAME) \
	--runtime python38 \
	--trigger-http \
	--allow-unauthenticated \
	--update-env-vars ENV=prod \
	--update-env-vars JOB_NAME=$(NAME)

build-dev:
	docker build \
	--build-arg GCP_CREDENTIALS_FILENAME=$(PROJECT_GCP_CREDENTIALS_FILENAME) \
	--build-arg FUNCTIONS_JOB_NAME=$(NAME) \
	-f ./Dockerfile \
	-t $(NAME)_image \
	$(NAME)

run-dev:
	docker \
	run \
	-ti \
	--rm \
	--env ENV=dev \
	--env SLACK_WEBHOOK_URL=$(SLACK_WEBHOOK_URL) \
	-p 8080:8080 \
	--mount type=bind,source="$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))"/$(NAME)/,target=/root/function/ \
	--mount type=bind,source=/Users/brunomurino/.config/gcp/,target=/root/config/ \
	--name $(NAME)_container \
	--entrypoint functions-framework \
	$(NAME)_image \
	--target=entrypoint --debug

start-dev: build-dev run-dev
	