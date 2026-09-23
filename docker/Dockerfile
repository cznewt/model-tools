# model-tools: one image with every "desired state" renderer plus its helpers.
#   kapitan, go-jsonnet (jsonnet, jsonnetfmt, jsonnet-lint), jb, jrsonnet, tanka,
#   helm, kustomize, kubectl, kubeconform, cue, timoni, kluctl, ytt, kcl,
#   sops, age, vals, yq, jq, just, fish
#
# Multi-arch through buildx: TARGETARCH is amd64 or arm64; the two release
# asset namings that differ (jrsonnet, just) are derived from it below.
ARG UBUNTU_VERSION=24.04
FROM ubuntu:${UBUNTU_VERSION} AS downloader

ARG TARGETARCH
ENV PKG_ARCH=${TARGETARCH}

WORKDIR /root

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague
ENV PATH="/opt/venv/bin:${PATH}"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3 python3-pip python3-venv python3-dev \
    curl build-essential unzip wget git libffi-dev ca-certificates golang-go \
    && rm -rf /var/lib/apt/lists/*

# golang-go: gojsonnet has no arm64 wheel, pip builds it from source under QEMU

# kapitan (python) with the go-jsonnet binding; pyyaml + markdown for the doc action
ARG KAPITAN_VERSION
RUN python3 -m venv /opt/venv && \
    pip3 install --upgrade pip wheel && \
    pip3 install "kapitan[gojsonnet]==${KAPITAN_VERSION}" pyyaml markdown

ARG JSONNET_VERSION
RUN wget -q https://github.com/google/go-jsonnet/releases/download/v${JSONNET_VERSION}/go-jsonnet_${JSONNET_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar xzf go-jsonnet_${JSONNET_VERSION}_linux_${PKG_ARCH}.tar.gz

ARG JB_VERSION
RUN wget -q -O jb https://github.com/jsonnet-bundler/jsonnet-bundler/releases/download/v${JB_VERSION}/jb-linux-${PKG_ARCH} && chmod +x jb

ARG JRSONNET_VERSION
RUN case "${PKG_ARCH}" in amd64) A=amd64 ;; arm64) A=aarch64 ;; *) echo "unsupported arch ${PKG_ARCH}" && exit 1 ;; esac \
    && wget -q -O jrsonnet https://github.com/deltarocks/jrsonnet/releases/download/v${JRSONNET_VERSION}/jrsonnet-linux-gnu-${A} && chmod +x jrsonnet

ARG HELM_VERSION
RUN wget -q https://get.helm.sh/helm-v${HELM_VERSION}-linux-${PKG_ARCH}.tar.gz \
    && tar -zxf helm-v${HELM_VERSION}-linux-${PKG_ARCH}.tar.gz && mv linux-${PKG_ARCH}/helm helm && chmod +x helm

ARG TANKA_VERSION
RUN wget -q -O tk https://github.com/grafana/tanka/releases/download/v${TANKA_VERSION}/tk-linux-${PKG_ARCH} && chmod +x tk

ARG YTT_VERSION
RUN wget -q -O ytt https://github.com/carvel-dev/ytt/releases/download/v${YTT_VERSION}/ytt-linux-${PKG_ARCH} && chmod +x ytt

ARG KLUCTL_VERSION
RUN wget -q https://github.com/kluctl/kluctl/releases/download/v${KLUCTL_VERSION}/kluctl_v${KLUCTL_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar -zxf kluctl_v${KLUCTL_VERSION}_linux_${PKG_ARCH}.tar.gz && chmod +x kluctl

ARG KCL_VERSION
RUN wget -q https://github.com/kcl-lang/cli/releases/download/v${KCL_VERSION}/kcl-v${KCL_VERSION}-linux-${PKG_ARCH}.tar.gz \
    && tar -zxf kcl-v${KCL_VERSION}-linux-${PKG_ARCH}.tar.gz && chmod +x kcl

ARG JQ_VERSION
RUN wget -q -O jq https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}/jq-linux-${PKG_ARCH} && chmod +x jq

ARG YQ_VERSION
RUN wget -q -O yq https://github.com/mikefarah/yq/releases/download/v${YQ_VERSION}/yq_linux_${PKG_ARCH} && chmod +x yq

ARG VALS_VERSION
RUN wget -q https://github.com/helmfile/vals/releases/download/v${VALS_VERSION}/vals_${VALS_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar -zxf vals_${VALS_VERSION}_linux_${PKG_ARCH}.tar.gz && chmod +x vals

ARG CUE_VERSION
RUN wget -q https://github.com/cue-lang/cue/releases/download/v${CUE_VERSION}/cue_v${CUE_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar -zxf cue_v${CUE_VERSION}_linux_${PKG_ARCH}.tar.gz && chmod +x cue

ARG SOPS_VERSION
RUN wget -q -O sops https://github.com/getsops/sops/releases/download/v${SOPS_VERSION}/sops-v${SOPS_VERSION}.linux.${PKG_ARCH} && chmod +x sops

ARG AGE_VERSION
RUN wget -q https://github.com/FiloSottile/age/releases/download/v${AGE_VERSION}/age-v${AGE_VERSION}-linux-${PKG_ARCH}.tar.gz \
    && tar -zxf age-v${AGE_VERSION}-linux-${PKG_ARCH}.tar.gz

ARG KUSTOMIZE_VERSION
RUN wget -q https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/v${KUSTOMIZE_VERSION}/kustomize_v${KUSTOMIZE_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar -zxf kustomize_v${KUSTOMIZE_VERSION}_linux_${PKG_ARCH}.tar.gz && chmod +x kustomize

ARG KUBECTL_VERSION
RUN wget -q -O kubectl https://dl.k8s.io/release/v${KUBECTL_VERSION}/bin/linux/${PKG_ARCH}/kubectl && chmod +x kubectl

ARG KUBECONFORM_VERSION
RUN wget -q https://github.com/yannh/kubeconform/releases/download/v${KUBECONFORM_VERSION}/kubeconform-linux-${PKG_ARCH}.tar.gz \
    && tar -zxf kubeconform-linux-${PKG_ARCH}.tar.gz && chmod +x kubeconform

ARG TIMONI_VERSION
RUN wget -q https://github.com/stefanprodan/timoni/releases/download/v${TIMONI_VERSION}/timoni_${TIMONI_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar -zxf timoni_${TIMONI_VERSION}_linux_${PKG_ARCH}.tar.gz && chmod +x timoni

ARG JUST_VERSION
RUN case "${PKG_ARCH}" in amd64) A=x86_64 ;; arm64) A=aarch64 ;; esac \
    && wget -q https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-${A}-unknown-linux-musl.tar.gz \
    && tar -zxf just-${JUST_VERSION}-${A}-unknown-linux-musl.tar.gz just && chmod +x just

# GitOps engine clients: reconcile, diff and inspect what the renderers produced
ARG FLUX_VERSION
RUN wget -q https://github.com/fluxcd/flux2/releases/download/v${FLUX_VERSION}/flux_${FLUX_VERSION}_linux_${PKG_ARCH}.tar.gz \
    && tar -zxf flux_${FLUX_VERSION}_linux_${PKG_ARCH}.tar.gz flux && chmod +x flux

ARG ARGOCD_VERSION
RUN wget -q -O argocd https://github.com/argoproj/argo-cd/releases/download/v${ARGOCD_VERSION}/argocd-linux-${PKG_ARCH} && chmod +x argocd

ARG ARGO_WORKFLOWS_VERSION
RUN wget -q -O argo.gz https://github.com/argoproj/argo-workflows/releases/download/v${ARGO_WORKFLOWS_VERSION}/argo-linux-${PKG_ARCH}.gz \
    && gunzip -f argo.gz && chmod +x argo

FROM ubuntu:${UBUNTU_VERSION}

COPY --from=downloader /opt/venv /opt/venv
COPY --from=downloader /root/jsonnet /root/jsonnetfmt /root/jsonnet-lint /root/jsonnet-deps /usr/local/bin/
COPY --from=downloader /root/jb /root/jrsonnet /root/tk /root/ytt /root/yq /root/jq /root/kluctl /root/kcl /root/cue /root/sops /root/vals /root/kustomize /root/kubectl /root/kubeconform /root/timoni /root/just /root/helm /root/flux /root/argocd /root/argo /usr/local/bin/
COPY --from=downloader /root/age/age /root/age/age-keygen /usr/local/bin/

ENV PATH="/opt/venv/bin:${PATH}"
WORKDIR /root

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3 git ssh-client wget curl gnupg libmagic1 ca-certificates fish \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./files/actions /actions

ENV PATH="${PATH}:/actions"
