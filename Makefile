MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.SUFFIXES:

## Demo

.PHONY: merge-deployment-resources
merge-deployment-resources:
	cat .env.cawemo .env.iam > static/.env \
	&& yq m \
		docker-compose.cawemo.yml \
       	docker-compose.iam.yml \
		> static/docker-compose.yml

.PHONY: check-unmerged-deployment-changes
check-unmerged-deployment-changes: merge-deployment-resources
	./checkUnmergedChanges.sh