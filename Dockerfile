FROM docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.10.4

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="sphere_mesh ChRIS plugin wrapper"

WORKDIR /usr/local/src/ep-sphere_mesh

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["sphere_mesh_wrapper", "--help"]
