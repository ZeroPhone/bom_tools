# Interactive BOM generation

We use
[InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) to
generate web-based interactive visualisation of our PCBs. The
`generate-html-bom.sh` script generates the HTML BOMs for each Zerophone
revision and outputs it in `/tmp/generate-html-bom`. It depends on
[Kicad](http://kicad-pcb.org/) 5.0.0 and
[kicad-python](https://github.com/KiCad/kicad-python). Since it is currently
a pain to setup on most distributions **[1]**, you can use the environment
defined in `Dockerfile`:

```
export IMAGE_NAME=zp-htmlbomgenerator
export CONTAINER_NAME=$IMAGE_NAME

# Using docker
docker build -t $IMAGE_NAME .
docker run -it $IMAGE_NAME
docker cp $CONTAINER_NAME:/tmp/generated-html-bom.tar.gz .

# Using podman/buildah
podman build -t $IMAGE_NAME .
podman run --name $CONTAINER_NAME -it $IMAGE_NAME
volume=$(podman mount $CONTAINER_NAME)
cp $volume/tmp/generated-html-bom.tar.gz .
podman unmount $CONTAINER_NAME
podman rm $CONTAINER_NAME
```

**[1]** As of writing (Sept. 2018), it works out-of-the-box on
[Archlinux](https://www.archlinux.org/packages/community/x86_64/kicad/) and
[Debian buster](https://packages.debian.org/buster/kicad).
