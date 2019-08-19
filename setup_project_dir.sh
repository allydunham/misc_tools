#!/usr/bin/env bash
# Setup a new/existing folder ($1) for a data science style project, in my standard dir layout

# Directory to create project in
dir=$1

# Check dir exists, will create necessary parent dirs
if [ ! -d "$dir" ]
then
    printf "%s\n" "$dir does not exist, will be created"
    mkdir -p "$dir"
fi

cd "$dir" || exit

# Check if dir is empty - ask to continue if not
# script should be safe for existing content in any case
if [ "$(ls -A)" ]
then
    read -p "$dir is not empty. Continue (y/N)? " -n 1 -r
    echo

    [[ "$REPLY" =~ ^[Nn]$ ]] && exit 0
fi

# Make expected files
touch README

# Make directory structure
mkdir -p bin
mkdir -p src
mkdir -p docs
mkdir -p data
mkdir -p data/raw

