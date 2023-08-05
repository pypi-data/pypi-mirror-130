FROM python:3.9

# Install poetry and copy poetry.lock file
RUN pip install poetry
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

# Set PYTHONPATH variable
ENV PYTHONPATH /code

# Set container's entrypoint
ENTRYPOINT ["/bin/bash", "-l", "-c"]