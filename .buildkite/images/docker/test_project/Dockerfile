ARG BASE_IMAGE

FROM $BASE_IMAGE

ADD build_cache/ /
ADD test_pipelines test_pipelines

ENV GOOGLE_APPLICATION_CREDENTIALS="/gac.json"

RUN pip install \
        -e dagster \
        -e dagster-graphql \
        -e dagster-cron \
        -e dagit \
        -e dagster-postgres \
        -e dagster-pandas \
        -e dagster-aws \
        -e dagster-gcp \
        -e dagster-k8s \
        -e dagster-airflow \
        -e test_pipelines

WORKDIR /test_pipelines/

EXPOSE 80
