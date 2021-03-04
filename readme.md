[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

<p align="center">
  <img width="250" height="250" src="https://i.imgur.com/YCtycJ0.png">
</p>

## Ratatouille in a nutshell

Ratatoille is ready to teach you how to cooking healthy. This service allow us
to perform our own recipes or explore new ones. Moreover this application lets
you to contact with nutricionists in order to balance your diet.

## Local development

Ratatouille is easy to develop in a local environment by using docker. just type in your terminal `make`
and everything you need will make up by itselt. Please copy the content of `build/env/.env.sample` to
your own _.env_ in `build/env/.env`. You can do this by executting:

```cmd
cp ./build/env/.env.sample ./build/env/.env
```

Moreover you can perform the following operations:

- **make**: setting up the containers
- **make sh**: attach a console inside ratatouille.
- **make logs**: shows ratatouille logs
- **make local.build**: recompiles ratatouille image

## Configure pre-commit (Python3 required)

pre-commit is a useful tool which checks your files before any commit push preventings fails in early steps.

Install pre-commit is easy:

```
pip install pre-commit
python3 -m pre_commit install
```
