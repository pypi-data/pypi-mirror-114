FROM xzregg/py37:base

ARG environment=dev
# 打包时间
ARG build_data

LABEL build-date="${build_data}"

ENV C_FORCE_ROOT true
ENV ENVIRONMENT $environment
ENV BUILD_DATE $build_data
ENV PYTHONUNBUFFERED 1
#ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

WORKDIR /app
ADD . /app

RUN pip3 install --upgrade --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/ \
    && mkdir -p tmp \
    && mkdir -p logs \
    && rm -rf /root/.cache \
    && rm -rf /tmp/*

EXPOSE 18809 80 8080 18888 13891
#CMD ["python3","manage.py","migrate"]
CMD ["mysupervisorctl"]
#CMD ["/bin/bash -c 'python3 manage.py migrate && mysupervisorctl'"]
