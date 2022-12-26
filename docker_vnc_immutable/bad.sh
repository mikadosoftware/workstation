#!/bin/bash

catch_err() {
    echo "An error occured. Commonly this needs a podman container prune to remove container image with same name."
}

trap 'catch_err' ERR

echo BEFORE
fjfjhfhfjfjfjfjfjf
echo AFTER