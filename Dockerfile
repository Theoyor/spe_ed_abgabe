#FROM rust:latest
#WORKDIR /src/spe_ed_rust
#COPY . .
#RUN cargo install --path src/spe_ed_rust/


FROM konstin2/maturin:latest
WORKDIR /
COPY  . .
RUN maturin build --release -m /src/spe_ed_rust/Cargo.toml -o /src/spe_ed_rust/spe_ed_lib

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster
EXPOSE 4200

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt


WORKDIR /app/src
ADD . /app
COPY . .
COPY --from=0 /src/spe_ed_rust/spe_ed_lib ./src/spe_ed_rust/spe_ed_lib
#RUN python -m pip install cffi
RUN python -m pip install ./src/spe_ed_rust/spe_ed_lib/spe_ed_rust-0.1.0-cp38-cp38-manylinux2010_x86_64.whl
#RUN cargo install --path
#RUN maturin build --release -m ./src/spe_ed_rust/Cargo.toml

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:4200", "src.game:server"]
