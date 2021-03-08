FROM nvidia/cuda:9.0-cudnn7-devel

LABEL maintainer &amp;quot;thatta&amp;quot;

# Set environment
ENV TERM xterm
ENV LC_ALL=C.UTF-8
ENV LANG C.UTF-8

# Install apt package.
RUN DEBIAN_FRONTEND=noninteractive \
   apt-get update -y \
 &&  apt-get install -y --no-install-recommends \
   apt-utils \
   less \
   wget \
   curl \
   git \
   graphviz \
   unzip \
   bzip2 \
   build-essential \
   vim \
   libncursesw5-dev \
   libgdbm-dev \
   libc6-dev \
   zlib1g-dev \
   libsqlite3-dev \
   tk-dev \
   libssl-dev \
   openssl \
   libbz2-dev \
   libreadline-dev

# Install pyenv.
RUN git clone https://github.com/pyenv/pyenv.git /opt/pyenv \
 && echo 'eval &amp;quot;$(pyenv init -)&amp;quot;' >> ~/.bashrc
ENV PYENV_ROOT /opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN $PYENV_ROOT/plugins/python-build/install.sh

# Create Anaconda environment
RUN pyenv install anaconda3-4.4.0 && \ 
	pyenv global anaconda3-4.4.0 && \  
	pyenv rehash

# Create python 3.7 environment and install pipenv.
RUN pyenv install 3.6.5 &&  \
   pyenv global 3.6.5 && \
   eval "$(pyenv init -)"

# ENV PATH $PYENV_ROOT/versions/anaconda3-4.4.0/bin:$PATH


# Upgrade pip.
RUN pip install --upgrade pip

# Install python library.
RUN pip install --ignore-installed \
   matplotlib\
   networkx\
   notebook\
   numpy\
   pandas\
   pillow\
   torch==1.1.0 \
   scikit-image==0.14.1 \
   scikit-learn==0.20.1 \
   scipy==1.1.0 \
   torchvision==0.3.0 \
   tqdm \
   Django \
   django-bootstrap4 \
   requests
   # io \
   # base64
# COPY requirements.txt /tmp/
# RUN conda create --name myenv --file /tmp/requirements.txt
# COPY . /tmp/

# RUN source activate myenv
# Enable nbextension.
# RUN jupyter contrib nbextension install --user

# Downgrade cuDNN library.
# TensorFlows issue: https://github.com/tensorflow/tensorflow/issues/17566#issuecomment-372490062
# RUN apt-get install -y --allow-downgrades --allow-change-held-packages libcudnn7=7.0.5.15-1+cuda9.0
RUN DEBIAN_FRONTEND=noninteractive \
   apt-get install -y --allow-downgrades --allow-change-held-packages libcudnn7=7.1.4.18-1+cuda9.0

# Clean cache.
RUN apt-get clean && \
   rm -rf /var/lib/apt/lists/* && \
   rm -rf /tmp/*

# EXPOSE 10551

# Run jupyter notebook.
 #CMD ["jupyter", "notebook", "--allow-root", "--port=10551", "--ip=0.0.0.0"]
