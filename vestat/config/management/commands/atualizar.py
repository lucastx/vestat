# -*- encoding: utf-8 -*-
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from vestat.config.management.converter_dump import converter_cartoes

def versao_1_2_0(cmd, *args):
    # Sincroniza o banco de dados
    call_command('syncdb', interactive=False)

    # Evolui o banco de dados com o Django Evolution
    call_command('evolve', interactive=False, execute=True, hint=True, database="default")

    # Cria supe
    call_command('createsuperuser', interactive=False, username=settings.AUTOLOGIN_USERNAME, email="dev@lucasteixeira.com")

    # Configura a senha
    superuser = User.objects.get(username=settings.AUTOLOGIN_USERNAME)
    superuser.set_password(settings.AUTOLOGIN_PASSWORD)
    superuser.save()

def versao_1_2_1(cmd, *args):
    if len(args) != 1:
        raise CommandError("Uso: atualizar 1.2.1 <dump_file>\n\ndump: arquivo de dump do banco de dados anterior (JSON)")


    print("Convertendo cartões de crédito e pagamentos para novo modelo...")

    novo_bd_json = converter_cartoes(args[0])
    tmp_dump_filename = "fixture_convertida.json"

    print("Armazenando dados convertidos em {tmp_dump_filename}".format(**vars()))

    with open(tmp_dump_filename, "w") as tmp_dump_file:
        tmp_dump_file.write(novo_bd_json)

    print("Carregando dados convertidos no banco de dados...")

    call_command("loaddata", tmp_dump_filename)

    print("Removendo arquivo temporário...")
    os.remove(tmp_dump_filename)


class Command(BaseCommand):
    args = '<versao>'
    help = 'Faz as modificações necessárias para uma determinada versão'

    def handle(self, *args, **options):
        versoes_disponiveis = { nome.replace("versao_", "").replace("_", "."): item for nome, item in globals().items() if nome.startswith("versao_") }
        nomes_das_versoes = [ nome for nome, _ in versoes_disponiveis.items() ]

        if len(args) < 1:
            raise CommandError("Uso: atualizar " + self.args + " [ARG...]\n" + \
                "\nVersões disponíveis:\n\n" + \
                "\n".join(nomes_das_versoes))

        versao = args[0]

        try:
            funcao = versoes_disponiveis[versao]
        except KeyError:
            raise CommandError("\nVersões disponíveis:\n\n" + \
                "\n".join(nomes_das_versoes))

        funcao(self, *args[1:])
