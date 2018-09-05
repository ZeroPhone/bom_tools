#!/bin/sh

set -e
set -x

HTMLBOM_REPOSITORY="https://github.com/openscopeproject/InteractiveHtmlBom"
HTMLBOM_RELEASE="v1"
HTMLBOM_ARCHIVE="InteractiveHtmlBom-$HTMLBOM_RELEASE.tar.gz"
HTMLBOM_SCRIPT="./InteractiveHtmlBom-1/InteractiveHtmlBom/generate_interactive_bom.py"

PCB_REPOSITORY="https://github.com/ZeroPhone/ZeroPhone-PCBs"
PCB_REVISIONS="gamma delta delta-b"

# Work in /tmp to keep current directory clean
cd /tmp

# Fetch InteractiveHtmlBom generator
wget -O $HTMLBOM_ARCHIVE $HTMLBOM_REPOSITORY/archive/$HTMLBOM_RELEASE.tar.gz
tar xf $HTMLBOM_ARCHIVE

# Fetch PCB revisions and generate HTML files
for revision in $PCB_REVISIONS; do
    revision_dir=generated-html-bom/$revision

    wget -O $revision.tar.gz $PCB_REPOSITORY/archive/$revision.tar.gz
    tar xf $revision.tar.gz

    for pcb_file in $(find "ZeroPhone-PCBs-$revision" -name "*.kicad_pcb") ; do
        python2 $HTMLBOM_SCRIPT --nobrowser $pcb_file

        pcb_dir=$(dirname $pcb_file)
        pcb_name=$(basename $pcb_dir)
        mkdir -p $revision_dir/$pcb_name
        cp $pcb_dir/bom/ibom.html $revision_dir/$pcb_name/index.html
    done
done

# Archive output for easier handling
tar cvzf generated-html-bom.tar.gz generated-html-bom
