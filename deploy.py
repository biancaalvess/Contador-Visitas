#!/usr/bin/env python3
"""
Script de deploy para a API do Contador de Visitas
"""

import subprocess
import sys
import os
from datetime import datetime


def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f" {descricao}...")
    try:
        resultado = subprocess.run(
            comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f" {descricao} - Sucesso")
            if resultado.stdout:
                print(f"   {resultado.stdout.strip()}")
            return True
        else:
            print(f" {descricao} - Erro")
            if resultado.stderr:
                print(f"   Erro: {resultado.stderr.strip()}")
            return False
    except Exception as e:
        print(f" {descricao} - Exceção: {e}")
        return False


def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = [
        'app.py',
        'requirements.txt',
        'README.md',
        'Procfile',
        'runtime.txt'
    ]

    print(" Verificando arquivos necessários...")

    faltando = []
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"    {arquivo}")
        else:
            print(f"    {arquivo} (faltando)")
            faltando.append(arquivo)

    if faltando:
        print(f"\n Arquivos faltando: {', '.join(faltando)}")
        return False

    print(" Todos os arquivos necessários estão presentes")
    return True


def fazer_backup():
    """Faz backup dos dados antes do deploy"""
    print("Fazendo backup dos dados...")
    if os.path.exists('backup_script.py'):
        return executar_comando('python backup_script.py', 'Backup dos dados')
    else:
        print("  Script de backup não encontrado, pulando...")
        return True


def commit_git():
    """Faz commit das mudanças"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    executar_comando('git add .', 'Adicionando arquivos ao git')
    executar_comando(
        f'git commit -m "Deploy API Contador de Visitas - {timestamp}"', 'Fazendo commit')

    return True


def deploy_heroku():
    """Deploy para o Heroku"""
    print("\n Iniciando deploy para Heroku...")

    # Verifica se o Heroku CLI está instalado
    if not executar_comando('heroku --version', 'Verificando Heroku CLI'):
        print(" Heroku CLI não encontrado. Instale em: https://devcenter.heroku.com/articles/heroku-cli")
        return False

    # Faz login no Heroku (se necessário)
    executar_comando('heroku auth:whoami', 'Verificando login Heroku')

    # Cria app se não existir
    nome_app = input(
        "Nome do app Heroku (ou Enter para gerar automaticamente): ").strip()
    if nome_app:
        executar_comando(
            f'heroku create {nome_app}', f'Criando app {nome_app}')
    else:
        executar_comando('heroku create', 'Criando app com nome automático')

    # Faz o deploy
    if executar_comando('git push heroku main', 'Deploy para Heroku'):
        print(" Deploy concluído com sucesso!")
        executar_comando('heroku open', 'Abrindo aplicação')
        return True
    else:
        print(" Falha no deploy")
        return False


def menu_principal():
    """Menu principal do script de deploy"""
    print(" Script de Deploy - API Contador de Visitas")
    print("=" * 50)
    print("1. Verificar arquivos")
    print("2. Fazer backup")
    print("3. Commit Git")
    print("4. Deploy Heroku")
    print("5. Deploy completo (tudo)")
    print("0. Sair")
    print()

    escolha = input("Escolha uma opção: ").strip()

    if escolha == '1':
        verificar_arquivos()
    elif escolha == '2':
        fazer_backup()
    elif escolha == '3':
        commit_git()
    elif escolha == '4':
        deploy_heroku()
    elif escolha == '5':
        print(" Executando deploy completo...\n")
        if (verificar_arquivos() and
            fazer_backup() and
            commit_git() and
                deploy_heroku()):
            print("\n🎉 Deploy completo realizado com sucesso!")
        else:
            print("\n Deploy falhou em alguma etapa")
    elif escolha == '0':
        print(" Saindo...")
        return False
    else:
        print(" Opção inválida")

    print("\n" + "=" * 50)
    return True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'auto':
            # Deploy automático
            print(" Deploy automático iniciado...")
            if (verificar_arquivos() and
                fazer_backup() and
                commit_git() and
                    deploy_heroku()):
                print("🎉 Deploy automático concluído!")
            else:
                print(" Deploy automático falhou")
        else:
            print("Uso: python deploy.py [auto]")
    else:
        # Menu interativo
        while menu_principal():
            pass
