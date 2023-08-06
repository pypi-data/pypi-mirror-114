FROM continuumio/miniconda3:latest

RUN apt-get update && apt-get install -yqq curl \
 && rm -rf /var/lib/apt/lists/*

ARG USER=dnadna

# Environment for using CUDA capabilities, though this also requires
# that the Docker engine is using the NVIDIA container runtime:
# https://github.com/NVIDIA/nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES="all"
ENV NVIDIA_DRIVER_CAPABILITIES="compute,utility"

# The container runs by default as the "dnadna" user instead of root
RUN adduser --uid 1001 --disabled-password --gecos '' ${USER}

# Install fixuid so that we can more easily fix up the UID of the dnadna
# user if the container is run with --uid <uid!=1001>
RUN curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.5/fixuid-0.5-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - \
 && chown root:root /usr/local/bin/fixuid \
 && chmod 4755 /usr/local/bin/fixuid \
 && mkdir -p /etc/fixuid \
 && printf "user: ${USER}\ngroup: ${USER}\npaths:\n  - /home/${USER}\n" > /etc/fixuid/config.yml

USER ${USER}

# Make the directory before setting it as the WORKDIR; see
# https://github.com/moby/moby/issues/36677#issuecomment-375607267
RUN mkdir -p /home/${USER}/dnadna
WORKDIR /home/${USER}/dnadna

# Copy over just the environment.yml
# NOTE: This used to be spelled "COPY --chown=${USER}" but this isn't
# supported on some older Docker versions
COPY --chown=1001:1001 environment-cuda.yml /home/${USER}/dnadna/

# Create the environment
# We create the full environment as root.
# file ownership doesn't need to be changed later (this takes a very long time
# otherwise).  
# If users need to add additional packages to the environment they can do so
# by creating a new environment later.
USER root
RUN conda env update -n base -f environment-cuda.yml \
 && conda clean --all --yes

# Now copy over the full source tree (which changes more frequently)
COPY --chown=1001:1001 . /home/${USER}/dnadna/

COPY ./docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]

# Install the local copy of dnadna (run this through the entrypoint so that
# it runs in the conda environment; there are other ways we could do this
# but since it's already available to us might as well
# The git repository is intentionally included in the build context so
# that setuptools_scm can work; but after installation we can get rid
# of it to save space
RUN /usr/local/bin/docker-entrypoint.sh pip --no-cache-dir install . \
 && rm -rf .git

USER ${USER}

# There is apparently an issue in conda where the user's local
# pkgs_dir does not get set as the default, so we need to change that
# https://github.com/ContinuumIO/docker-images/issues/151#issuecomment-642603686
RUN conda config --prepend pkgs_dirs /opt/conda/pkgs \
 && conda config --prepend pkgs_dirs /home/${USER}/.conda/pkgs \
 && conda init bash

# Just start a bash shell as the default command
CMD [ "/bin/bash" ]
