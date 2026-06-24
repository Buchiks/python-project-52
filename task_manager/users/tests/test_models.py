import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_user():
    """Тест создания обычного пользователя"""
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )

    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    assert user.check_password('testpass123')
    assert user.pk is not None
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.date_joined is not None
