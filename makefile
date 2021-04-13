#!make
.DEFAULT_GOAL=start

check_missing_migrations:
	@$(eval TMP := $(shell docker exec -it ratatouille aerich migrate | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g"))
	@if [ "$(TMP)" != "No changes detected" ]; then \
    	echo "You have missing migrations!"; \
		exit 1; \
    fi

migrate:
	@docker exec ratatouille aerich upgrade

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
	@docker-compose run -v $(PWD):/app ratatouille coverage run --source=ratatouille -m pytest
	@mv .coverage .coverage-docker
	@coverage combine -a .coverage-docker
	@coverage report

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
