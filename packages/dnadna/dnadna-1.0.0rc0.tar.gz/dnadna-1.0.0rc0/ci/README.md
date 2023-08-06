Continuous Integration for DNADNA
=================================

This directory contains documentation and config files related to the
continuous integration (CI) infrastructure for DNADNA.  As DNADNA's source
code is hosted on a GitLab server, we use [GitLab
CI/CD](https://docs.gitlab.com/ee/ci/) to continuously run DNANDA's test
suit and build and deploy the documentation.

The main configuration for DNADNA's CI pipeline is in the
[`.gitlab-ci.yml`](../.gitlab-ci.yml) file at the root of the repository.
However, in order to make use of it, we must also configuration and maintain
a [GitLab Runner](https://docs.gitlab.com/runner/) to orchestrate and run CI
jobs.  Although some GitLab instances provide *shared* runners which can run
CI jobs for any project hosted on that site, many local GitLab instances
(including https://gitlab.inria.fr where DNADNA is currently hosted) do not
have shared runners available.  Furthermore, to fully test DNADNA it is
necessary to run the builds on machines with CUDA-compatible GPUs which
won't typically be available to shared runners.  Hence we need to run our
own GitLab Runner which has access to GPU devices.

This file documents, at a high level, how to set up a GitLab Runner in
general, as well as how the runner currently used for DNADNA's CI is
configured.


CI pipeline
-----------

A pipeline is a sequence of *jobs* that are executed each time a new change
is pushed to a git branch.  Some jobs run regardless of the branch, and some
jobs (such as *deploy*) can be configured to run only when certain branches
change (such as "master").  Jobs can be organized into *stages*, such that
jobs in the same stage can be executed in parallel, but only after all jobs
in the previous stage complete successfully.  The exact graph of job
dependencies is highly configurable, but this is the usual use case.  See
the [official documentation for GitLab CI
Pipelines](https://docs.gitlab.com/ee/ci/pipelines/index.html) for full
detail.

DNADNA's pipeline is configured in the [`.gitlab-ci.yml`](../.gitlab-ci.yml)
file.  The most recently executed pipeline can always be seen
[here](https://gitlab.inria.fr/ml_genetics/private/dnadna/pipelines/master/latest).
It currently consists of four stages:

- setup
- test
- docs
- deploy

### workflow

The [workflow](https://docs.gitlab.com/ee/ci/yaml/#workflowrules) section of
the `.gitlab-ci.yml` determines when pipelines should be run for a given
commit.  The current setup runs a pipeline only for:

- tags
- merge requests
- the `master` branch *or* any branch whose name begins with `ci/` or `ci-`

the latter rule is so that pipelines aren't created for *all* branches (this
leads to duplicate pipelines, such as when a branch is created for a merge
request.  However, if one has an experimental branch on which they would
like to run build pipelines, the branch name can be prefixed with `ci/` or
`ci-`.

### setup stage

DNADNA uses a [conda environment](https://docs.conda.io/en/latest/) to
install all of its runtime and test dependencies.  Some of its dependencies
(such as `cuda-toolkit`) are quite large so it can take some time to build
the environments.  This stage runs one or both of two jobs: `setup:cuda` and
`setup:cpu` which set up two different runtime environments described in
[`environment-cuda.yml`](../environment-cuda.yml) and
[`environment-cpu.yml`](../environment-cpu.yml) respectively.

The setup jobs merely build the conda environments, and the resulting
environments are *cached* using GitLab CI's [dependency
caching](https://docs.gitlab.com/ee/ci/caching/) feature.  This way
subsequent jobs in the same, or subsequent pipelines can re-use the cached
conda environments without having to re-build them for every job.  This
saves significant time and resources for most CI jobs.

Because of the use of caching, the "setup" stage can be skipped entirely by
most pipelines, and they can use the cached conda environments built and
cached by a previous pipeline.  The "setup" stage only needs to be run when
there have been changes to either `environment-cuda.yml` or
`environment-cpu.yml`, hence requiring the environments to be re-built and
re-cached.

### test stage

The "test" stage simply activates the conda environment from the previous
successful "setup" stage, and runs DNADNA's test suite using
[pytest](https://docs.pytest.org/en/latest/), as well as produces test
coverage reports.  If any of the tests fail, the job fails, and subsequent
pipeline stages are not run.

### docs stage

The "docs" stage builds DNADNA's documentation (currently just in HTML
format) using the [Sphinx](https://www.sphinx-doc.org/) documentation
generator, and fails if there are errors building the docs.

### deploy stage

The "deploy" stage is only run for pipelines on the "master" branch.  It
takes the HTML documentation built by a successful run of a the "docs"
stage, and pushes it to our [GitLab
Pages](https://docs.gitlab.com/ee/user/project/pages/) so that it can be
read at https://ml_genetics.gitlabpages.inria.fr/private/dnadna/ .

It also deploys an HTML [coverage
report](https://ml_genetics.gitlabpages.inria.fr/private/dnadna/coverage/cuda/)
so that the test coverage reported from the previous "test" stage can be
perused.  In the future this will be removed and replaced with GitLab's
[built-in support for coverage
reports](https://docs.gitlab.com/ee/ci/yaml/README.html#artifactsreportscobertura),
but this feature is very new and our local GitLab instance is not yet on a
version that supports it.


Configuring a GitLab Runner
---------------------------

Full documentation can be found at [Configuring GitLab
Runners](https://docs.gitlab.com/ee/ci/runners/README.html).  Here we
provide just a brief overview.

### Starting a gitlab-runner service

To run a GitLab runner it is good to have access to an always-on machine
with Docker installed (though it is also possible to provide a runner that
is only on part-time, such as running it on your personal computer at
night).  The easiest way to run the `gitlab-runner` orchestrator is by
running it in a [Docker
container](https://docs.gitlab.com/runner/install/docker.html).  For
example, like:

```bash
$ docker run --detach --volume /var/run/docker.sock:/var/run/docker.sock \
             --restart always --name dnadna-gitlab-runner gitlab/gitlab-runner
```

Here we create a container for gitlab-runner named "dnadna-gitlab-runner".
We mount `/var/run/docker.sock` as a volume, so that the gitlab-runner
container can also use the local system's Docker Engine to run build jobs.

TODO: This needs to be confirmed precisely, but my full notes on this are
on the TitanV server which I cannot currently access.

### gitlab-runner as an orchestrator

It should be clarified that the `gitlab-runner` command itself does not
directly execute build jobs.  Rather, it acts as an orchestrator that takes
requests from the project's pipeline to run jobs, and then spins up
additional runners, each of which handle a single job.  gitlab-runner can be
configured to specify how many jobs it can run concurrently.

Individual jobs can be run on a number of different executors, including
launching VMs, or using cloud compute services such as AWS.  Here we simply
use the [Docker
executor](https://docs.gitlab.com/runner/executors/docker.html), which runs
each job in its own Docker container, using (in this case) the same
DockerEngine that gitlab-runner itself is running on.

### Configuring gitlab-runner

At the moment, our dnadna-gitlab-runner does not know how to contact our
GitLab instance to begin accepting jobs, nor does it know how to execute
jobs.  We must provide it a config file, including a registration token,
then restart the container with the new configuration.

A template based on the actual (fairly minimal) configuration being used for
our current runner is at [`config.example.toml`](config.example.toml).
Lines commented with `# replace` contain variables that should be replaced
with actual values.  The `runners.url` option does not need to be changed
unless running pipelines on a different GitLab instance.  Lines commented `#
CUDA` are specific to configuring a runner which supports CUDA-enhanced
jobs.

A partial config file is also provided in
[`config.template.toml`](config.template.toml).  We will use this when
running `gitlab-runner register` below.

To obtain a runner token, the easiest way is through the web UI, if you have
sufficient permissions on the GitLab project.  Go to
https://gitlab.inria.fr/ml_genetics/private/dnadna/-/settings/ci_cd
and expand the "Runners" tab.  In the box labeled "Set up a specific runner
manually" you will find the URL (e.g. `https://gitlab.inria.fr` and a unique
token to use for registering the new runner).

#### Registering the runner

First, we can provide a partial configuration "template" from
[`config.template.toml`](config.template.toml).  This file needs to be
copied into the container so that it can use it:

```bash
$ docker cp config.template.toml dnadna-gitlab-runner:/etc/gitlab-runner/
```

To register the runner, on the Docker host on which you started it, run

```bash
$ docker exec -ti dnadna-gitlab-runner \
         gitlab-runner register \
             --template-config /etc/gitlab-runner/config.template.toml \
             --run-untagged
```

This will take you through an *interactive* registration process, an example
of which you can see here:

```text
Runtime platform                                    arch=amd64 os=linux pid=20 revision=1b659122 version=12.8.0
Running in system-mode.

Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
https://gitlab.inria.fr/
Please enter the gitlab-ci token for this runner:
xxxxxxxxxxxxxxxxxxxx
Please enter the gitlab-ci description for this runner:
[8e352418abf9]: My GitLab Runner for DNADNA, administered by Your Name <your@email>
Please enter the gitlab-ci tags for this runner (comma separated):
cuda
Registering runner... succeeded                     runner=XXXXXXXX
Please enter the executor: docker+machine, kubernetes, custom, docker-ssh, parallels, shell, ssh, virtualbox, docker, docker-ssh+machine:
docker
Please enter the default Docker image (e.g. ruby:2.6):
debian:latest
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
```

Refresh the CI settings page from which you obtained the registration token,
and you should see the new runner listed (with an automatically generated 8
character name) and a green circle next to its name.

All of these settings can also be provided non-interactively at the
command-line, like:

```bash
$ docker exec -ti dnadna-gitlab-runner \
         gitlab-runner register \
             --non-interactive \
             --template-config /etc/gitlab-runner/config.template.toml \
             --run-untagged \
             --url https://gitlab.inria.fr/ \
             --registration-token <token> \
             --description 'My GitLab Runner for DNADNA, administered by Your Name <your@email>' \
             --tag-list cuda \
             --executor docker --docker-image debian:latest
```

NOTE: As of writing there is a minor bug that `--executor docker` and
`--docker-image <image>` still need to be given at the command-line even if
they are already specified in the config template.

The value of the `--docker-image` setting isn't terribly important for now,
as it only specifies the default image to use for pipelines that don't
otherwise specify one.  Our pipeline specifies a different image to use.

#### Note on Docker configuration

In the [`config.template.toml`](config.template.toml) file we have under
`[runners.docker]` the setting:

```
volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock"]
```

The `"/cache"` is a default--it's where gitlab-runner mounts access to any
caches configured for the job.  However, the `"/var/run/docker.sock"` mount
is so that build jobs can directly access the Docker daemon on the same host
running gitlab-runner.  This is [one of the documented
methods](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-socket-binding)
for using Docker in a GitLab CI build.  However, it comes with some danger
because it means build jobs can take full control over the Docker daemon,
which may be being used by other users.  This is a potential security risk,
so please make use of this ethically.

Another possibility would be to configure gitlab-runner to start containers
in privileged mode, which allows using the
[docker-in-docker](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker-workflow-with-docker-executor)
method.  But this has its own, perhaps even more severe security trade-offs.


Configuring Docker+CUDA
-----------------------

TODO: How we configure Docker and gitlab-runner so that they can access
the GPUs.
