import json
import os
import subprocess

from django.conf import settings


def create_signature(data):
    """Создание цифровой подписи."""
    data = json.dumps(data)
    file_path = os.path.join(
        settings.BASE_DIR, 'server/apps/payments/js/create.js'
    )
    return subprocess.run(
        ['node', file_path, data, settings.PRODAMUS_KEY],
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8').strip()


def verify_signature(data, sign):
    """Проверка цифровой подписи."""
    data = json.dumps(data)
    file_path = os.path.join(
        settings.BASE_DIR, 'server/apps/payments/js/verify.js'
    )
    return subprocess.run(
        ['node', file_path, data, settings.PRODAMUS_KEY, sign],
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8').strip()
