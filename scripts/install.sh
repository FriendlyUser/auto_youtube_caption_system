#!/bin/sh

# handles all installation for python + ffmpeg and package.json
if ! [ -x "$(command -v python)" ]; then
  echo 'Error: python is not installed.' >&2
  exit 1
fi

# check if node installed
if ! [ -x "$(command -v node)" ]; then
  echo 'Error: node is not installed.' >&2
  exit 1
fi


# error if python not installed
sudo apt update -y
sudo apt install ffmpeg -y

# install node modules
npm install


# install python requirements
pip install -r scripts/requirements.txt