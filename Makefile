MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.SUFFIXES:

## Demo

.PHONY: merge-deployment-resources
merge-deployment-resources:
	cat input/.env.cawemo input/.env.iam > static/.env \
	&& yq m \
		input/docker-compose.cawemo.yml \
       	input/docker-compose.iam.yml \
		> static/docker-compose.yml

.PHONY: check-unmerged-deployment-changes
check-unmerged-deployment-changes: merge-deployment-resources
	./checkUnmergedChanges.sh