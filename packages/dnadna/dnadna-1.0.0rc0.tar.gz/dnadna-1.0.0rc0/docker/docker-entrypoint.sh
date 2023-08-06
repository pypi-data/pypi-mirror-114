#!/bin/bash

user=$(whoami 2>/dev/null)

if [ $UID -ne 0 -a $UID -ne 1001 ]; then
    # The default UID for the dnadna user is 1001; if running under a different
    # (non-root) UID change its UID.
    eval $(fixuid -q)
    # If the user with $UID did not exist before fixuid, then whoami returned
    # empty before so we need to do this again:
    user=$(whoami 2>/dev/null)
fi

# Set up the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
PS1="\h:\w\$ "
conda activate

if [ -n "$DEV" -a "$DEV" != "0" ]; then
    # Create the user's conda environment, activate it
    if [ ! -d /home/${user}/.conda/envs/dnadna ]; then
        conda create -n dnadna --clone base
        conda activate dnadna
        pip install -e .
    fi

    # Ensure that the dnadna environment is auto-activated when starting a new
    # shell:
    echo "conda activate dnadna" >> /home/${user}/.bashrc
fi

exec env PS1="$PS1" "$@"
