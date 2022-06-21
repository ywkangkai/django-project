FROM python:3.7-alpine
LABEL maintainer='kangkai'
LABEL description='Deploying Django project'

WORKDIR /usr/src/app
COPY ./AutoMationPlatform ./AutoMationPlatform/
COPY ./gunicorn_config.py ./configs/
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR AutoMationPlatform/
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk update
RUN apk add --allow-untrusted build-base mariadb-connector-c-dev curl iputils libffi-dev
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ cffi==1.14.5
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ paramiko==2.7.0
#RUN pip  install ruamel.yaml==0.16.10
#RUN pip  install ruamel.yaml.clib==0.2.0
RUN pip  install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/  -r requirements.txt 
RUN pip  install -i https://pypi.tuna.tsinghua.edu.cn/simple/  gunicorn
RUN apk add ca-certificates bash
RUN apk update && apk upgrade
RUN	rm -rf /var/cache/apk/* && \
    chmod u+x /docker-entrypoint.sh

VOLUME /usr/src/app/logs/
VOLUME /usr/src/app/AutoMationPlatform/

EXPOSE 8000
# CMD ["/usr/local/bin/gunicorn", "-c", "/usr/src/app/configs/gunicorn_config.py", "AutoMationPlatform.wsgi"]
ENTRYPOINT ["/docker-entrypoint.sh"]

