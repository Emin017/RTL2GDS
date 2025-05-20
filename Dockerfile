ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE}
LABEL maintainer="harry0789@qq.com"

RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y python3-pip && \
    pip3 install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple pyyaml orjson klayout requests && \
    apt-get autoremove -y && apt-get clean -y

ARG R2G_REPO=.
ARG R2G_WORKSPACE=/opt/rtl2gds

ENV PYTHONPATH="${R2G_WORKSPACE}/src"

ADD ${R2G_REPO} ${R2G_WORKSPACE}

WORKDIR ${R2G_WORKSPACE}

CMD ["/usr/bin/env", "python3", "-m", "rtl2gds", "-h"]
