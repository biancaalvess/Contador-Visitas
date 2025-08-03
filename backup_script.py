#!/usr/bin/env python3
"""
Script para fazer backup dos dados de visitas
"""

import json
import shutil
from datetime import datetime
import os


def fazer_backup():
    """Faz backup do arquivo de visitas"""
    try:
        # Nome do arquivo original
        arquivo_original = 'visitas.json'

        # Verifica se o arquivo existe
        if not os.path.exists(arquivo_original):
            print(" Arquivo visitas.json não encontrado!")
            return False

        # Gera nome do backup com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo_backup = f'visitas_backup_{timestamp}.json'

        # Copia o arquivo
        shutil.copy2(arquivo_original, arquivo_backup)

        # Verifica o número de visitas
        with open(arquivo_original, 'r') as f:
            visitas = json.load(f)

        print(f" Backup criado: {arquivo_backup}")
        print(f"Total de visitas salvas: {len(visitas)}")

        return True

    except Exception as e:
        print(f" Erro ao fazer backup: {e}")
        return False


def listar_backups():
    """Lista todos os backups disponíveis"""
    backups = [f for f in os.listdir('.') if f.startswith(
        'visitas_backup_') and f.endswith('.json')]

    if not backups:
        print(" Nenhum backup encontrado")
        return

    print(f"Backups encontrados ({len(backups)}):")
    backups.sort(reverse=True)  # Mais recente primeiro

    for backup in backups:
        try:
            # Pega informações do arquivo
            stat = os.stat(backup)
            tamanho = stat.st_size
            modificado = datetime.fromtimestamp(stat.st_mtime)

            # Conta visitas no backup
            with open(backup, 'r') as f:
                visitas = json.load(f)

            print(f"   {backup}")
            print(f"       {modificado.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"      {len(visitas)} visitas ({tamanho} bytes)")
            print()

        except Exception as e:
            print(f"   {backup} (erro: {e})")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        listar_backups()
    else:
        fazer_backup()
