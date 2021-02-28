ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d

COPY requirements-dev.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt \
   && rm -rf /tmp/pip-tmp

COPY . /app
WORKDIR /app

CMD task test