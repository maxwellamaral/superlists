Provisionamento de um novo site
===============================

## Pacotes necessários

* nginx
* Python 3.6
* virtualenv + pip
* Git

Por exemplo, no Ubuntu/Debian

* `sudo add-apt-repository ppa:fkrull/deadsnakes`
* `sudo apt install nginx git python3 python3-venv`

## Config do Nginx Virtual Host

* veja nginx.template.conf
* substitua SITENAME, por exemplo, por staging.my-domain.com

## Serviço Systemd

* veja gunicorn-systemd.template.service
* substitua SITENAME, por exemplo, por staging.my-domain.com

## Estrutura de pastas

```
/home/username
|__ sites
    |__ SITENAME
         |__ database
         |__ source
         |__ static
         |__ virtualenv
```