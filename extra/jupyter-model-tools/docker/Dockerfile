# jupyter-model-tools: JupyterLab on top of model-tools, with a bash kernel and
# language servers for Jsonnet, YAML, JSON and shell. Notebooks under
# /opt/notebooks are seeded into the user-writable /source/notebooks on first start.
ARG MODEL_TOOLS_VERSION=latest
FROM ghcr.io/cznewt/model-tools:${MODEL_TOOLS_VERSION}

USER root
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends -y nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN npm i -g bash-language-server yaml-language-server vscode-json-languageserver-bin

ARG JSONNET_LSP_VERSION=0.17.0
RUN case "$(uname -m)" in x86_64) A=amd64 ;; aarch64) A=arm64 ;; *) echo "unsupported $(uname -m)" && exit 1 ;; esac \
    && curl -fSL -o /usr/local/bin/jsonnet-language-server \
       "https://github.com/grafana/jsonnet-language-server/releases/download/v${JSONNET_LSP_VERSION}/jsonnet-language-server_${JSONNET_LSP_VERSION}_linux_${A}" \
    && chmod +x /usr/local/bin/jsonnet-language-server

COPY ./files/requirements.txt /requirements-notebook.txt
RUN pip3 install --no-cache-dir -r /requirements-notebook.txt \
    && python3 -m bash_kernel.install --sys-prefix \
    && (jupyter labextension disable "@jupyterlab/apputils-extension:announcements" || true)

COPY ./files/jupyter /home/ubuntu/.jupyter
COPY ./files/notebooks /opt/notebooks
COPY ./files/seed-notebooks /usr/local/bin/seed-notebooks

# JupyterLab serves /source; a persistent volume goes to /source/work (also ~/work).
RUN chmod +x /usr/local/bin/seed-notebooks \
    && mkdir -p /source/work \
    && chown -R ubuntu:ubuntu /home/ubuntu /opt/notebooks /source \
    && ln -sfn /source/work /home/ubuntu/work && chown -h ubuntu:ubuntu /home/ubuntu/work

USER ubuntu
WORKDIR /source
EXPOSE 8888

ENTRYPOINT ["/usr/local/bin/seed-notebooks"]
CMD ["jupyter", "lab", "--no-browser", "--config=/home/ubuntu/.jupyter/jupyter_notebook_config.py"]
