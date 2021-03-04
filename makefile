#!make
.DEFAULT_GOAL=start

local.build:
	@docker-compose build

local.start:
	@docker-compose up -d

local.down:
	@docker-compose down

local.check.credentials:
	@if ! [ -s ~/.credentials/ghcr.name ]; then \
    	python3 build/scripts/ghcr.py; \
    fi

local.docker.login: local.check.credentials
	@cat ~/.credentials/ghcr.token | docker login ghcr.io -u $(shell cat ~/.credentials/ghcr.name) --password-stdin

local.test:
	@docker exec ratatouille pytest --cov=ratatouille

ci.test:
	@docker exec ratatouille pytest --cov=ratatouille --junitxml=junit/test-results.xml --cov-report=xml --cov-report=html
	@docker cp $(shell docker-compose ps -q ratatouille):/app/junit ./junit
	@docker cp $(shell docker-compose ps -q ratatouille):/app/htmlcov ./htmlcov
	@docker cp $(shell docker-compose ps -q ratatouille):/app/coverage.xml ./coverage.xml

logs:
	@docker logs -f $(shell docker-compose ps -q ratatouille)

sh:
	@docker exec -it ratatouille /bin/bash

ci.docker.login:
	@echo $(GITHUB_TOKEN) | docker login ghcr.io -u $(GITHUB_USER) --password-stdin

docker_tag_and_push: ci.docker.login
	@export TAG=$(date +%d%m%Y-%H%M%S)
	@docker build -f build/docker/dockerfile.prod -t $(REGISTRY):latest -t $(REGISTRY):$(TAG) .
	@docker push $(REGISTRY):$(TAG)
	@docker push $(REGISTRY):latest

start: local.docker.login local.start

stop: local.down

renew: local.down local.build local.start

ci_check_tests:ci.docker.login local.start ci.test

.PHONY:  start stop renew sh logs docker_tag_and_push
