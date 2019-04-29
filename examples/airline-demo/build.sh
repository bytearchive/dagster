#!/bin/bash
# For the avoidance of doubt, this script is meant to be run with the airline-demo directory as pwd
# Builds the Docker image for Airflow and scaffolds the DAGs

set -eux

pip install --upgrade pip

function cleanup {
    rm -rf dagster
    rm -rf dagster-graphql
    rm -rf dagstermill
}
trap cleanup EXIT

cp -R ../../python_modules/dagster .
cp -R ../../python_modules/dagster-graphql .
cp -R ../../python_modules/dagstermill .

rm -rf dagster/.tox
rm -rf dagster-graphql/.tox
rm -rf dagstermill/.tox

rm -rf dagster/dist
rm -rf dagster-graphql/dist
rm -rf dagstermill/dist

rm -rf .tox dist

docker build -t airline-demo-airflow .
docker tag airline-demo-airflow dagster/airline-demo-airflow