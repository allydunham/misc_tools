#!/usr/bin/env bash
# TODO: Convert to python script with more convenient behaviour
# Script to sync between a local and remote directory(s)
#
# Setup for a given project folder using the config beow
#
# Will look for global and local .rsync_exclude/rsync_include files
# .rsync_exclude in $HOME is assumed to be global prefs
# Manual include overrides all excludes
#
# Sync only desired folders based on args

## Config ##
project_name="Project"
local=$HOME/test
remotes=(/remote/dir/1 remote/dir/2)
folders=( "data" "meta" "figures" "test" )

## Colours for printf ##
green=$(tput setaf 2)
magenta=$(tput setaf 5)
bold=$(tput bold)
normal=$(tput sgr0)

## Check for presence of include/exclude files ##
if [ -e "$HOME/.rsync_exclude" ]; then
   global_exclude="--exclude-from $HOME/.rsync_exclude"
else
   global_exclude=""
fi

if [ -e "$local/.rsync_exclude" ]; then
   local_exclude="--exclude-from $local/.rsync_exclude"
else
   local_exclude=""
fi

if [ -e "$local/.rsync_include" ]; then
   local_include="--include-from $local/.rsync_include --exclude='*'"
   local_exclude=""
else
   local_include=""
fi

## Sync function ##
syncr () {
   rsync -vauh "$global_exclude" "$local_exclude" "$local_include" --dry-run "$1" "$2"

   read -p "Transfer? " -n 1 -r
   echo
   if [[ $REPLY =~ ^[Yy]$ ]]
   then
      sync -auh "$global_exclude" "$local_exclude" "$local_include" "$1" "$2"
   fi
}

## Override folders if argument passed ##
if [ $# -ne 0 ]; then
   folders=( "$@" )
fi

## Perform sync ##
printf "%s\n" "${magenta}${bold}Rsyncing $project_name${normal}"
for r in "${remotes[@]}"; do
   read -p "Sync to remote: $r? " -n 1 -r
   echo
   if [[ $REPLY =~ ^[Yy]$ ]]; then
      for f in "${folders[@]}"; do
         printf "\n%s\n%s\n" "${green}${bold}Folder: $f${normal}" "${green}Local -> Remote${normal}"
         syncr "$local/$f/" "$r/$f"
         printf "\n%s\n" "${green}Local <- Remote${normal}"
         syncr "$r/$f/" "$local/$f"
      done
   fi
done


