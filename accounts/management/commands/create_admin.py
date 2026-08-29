from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = config('ADMIN_USERNAME', default='')
        email = config('ADMIN_EMAIL', default='')
        password = config('ADMIN_PASSWORD', default='')

        if not username or not password:
            self.stdout.write('ADMIN_USERNAME または ADMIN_PASSWORD が設定されていません。スキップします。')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'ユーザー "{username}" は既に存在します。スキップします。')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f'管理者アカウント "{username}" を作成しました。')