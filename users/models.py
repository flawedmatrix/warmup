from django.db import models

from constants import *

class User(models.Model):
    user = models.CharField(max_length=MAX_USERNAME_LENGTH)
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user

    @staticmethod
    def valid_username(username):
        if not username:
            return False
        return len(username) <= MAX_USERNAME_LENGTH

    @staticmethod
    def valid_password(password):
        if (password == None):
            return True
        return len(password) <= MAX_PASSWORD_LENGTH

    @staticmethod
    def login(user, password):
        try:
            u = User.objects.get(user=user, password=password)
        except (User.DoesNotExist):
            return ERR_BAD_CREDENTIALS
        else:
            u.count = u.count + 1
            u.save()
            return u.count

    @staticmethod
    def add(user, password):
        if not (User.valid_username(user)):
            return ERR_BAD_USERNAME
        if not (User.valid_password(password)):
            return ERR_BAD_PASSWORD
        u, created = User.objects.get_or_create(user=user)
        if (created == False):
            return ERR_USER_EXISTS
        else:
            u.password = password
            u.save()
        return u.count

    @staticmethod
    def TESTAPI_resetFixture():
        User.objects.all().delete()
        return SUCCESS
