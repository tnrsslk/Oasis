from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Составление строки для хеширования
        return (
            text_type(user.pk) +
            text_type(timestamp) +
            text_type(user.is_active)
        )

# Создание экземпляра генератора токенов для активации аккаунта
account_activation_token = AccountActivationTokenGenerator()
