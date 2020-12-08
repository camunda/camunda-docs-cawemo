#!/bin/bash

FILES="static/.env static/docker-compose.yml"

if [[ "$(git diff $FILES)" != "" ]]; then
		echo "There are differences for $FILES:"
		echo
		git --no-pager diff --no-color $FILES
		echo
		echo 'Please run'
		echo
		echo '  make merge-deployment-resources'
		echo
		echo "to create these differences for $FILES locally."
		echo 'Then commit and push those differences.'
		exit 1
fi