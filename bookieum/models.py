from django.db import models


class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_name = models.CharField(max_length=20)
    reading_level = models.IntegerField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    home_addr = models.CharField(max_length=50, blank=True, null=True)
    register_datetime = models.DateTimeField()
    share_cnt = models.IntegerField()
    access_token = models.CharField(max_length=300, blank=True, null=True)
    survey = models.CharField(max_length=5, default=False)
    genre = models.CharField(max_length=200, blank=True, null=True)
    mood = models.CharField(max_length=200, blank=True, null=True)
    interest = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'
        

class Books(models.Model):
    isbn_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    page_num = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(db_column='Keyword', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genres = models.CharField(max_length=255, blank=True, null=True)
    mood = models.CharField(max_length=255, blank=True, null=True)
    interest = models.CharField(max_length=255, blank=True, null=True)
    emotion_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Books'
        

class Recommend(models.Model):
    recommend_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.Case)
    recommend_datetime = models.DateTimeField(auto_now_add=True)
    emotion = models.CharField(max_length=20)
    answer_content = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Recommend'


class RecommendBooks(models.Model):
    mybook_id = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(Books, on_delete=models.Case)
    recommend = models.ForeignKey(Recommend, on_delete=models.Case)
    user = models.ForeignKey(Users, on_delete=models.Case)
    is_selected = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    reading_datetime = models.DateTimeField(blank=True, null=True)
    curr_page = models.IntegerField(blank=True, null=True)
    is_completed = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'Recommend_books'


class RegisterBooks(models.Model):
    register_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.Case)
    isbn = models.ForeignKey(Books, on_delete=models.Case)
    register_datetime = models.DateTimeField(auto_now_add=True)
    reading_datetime = models.DateTimeField(blank=True, null=True)
    curr_page = models.IntegerField()
    is_completed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Register_books'


class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=20)
    user = models.ForeignKey(Users, on_delete=models.Case)
    review_content = models.CharField(max_length=200, blank=True, null=True)
    satisfied = models.IntegerField(db_column='Satisfied')  # Field name made lowercase.
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Review'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
        
"""
from django.db import models

class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_name = models.CharField(max_length=20)
    reading_level = models.IntegerField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    home_addr = models.CharField(max_length=50, blank=True, null=True)
    register_datetime = models.DateTimeField()
    share_cnt = models.IntegerField()
    access_token = models.CharField(max_length=300, blank=True, null=True)
    survey = models.CharField(max_length=5, default=False)
    genre = models.CharField(max_length=200, blank=True, null=True)
    mood = models.CharField(max_length=200, blank=True, null=True)
    interest = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'
        

class Books(models.Model):
    isbn_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    page_num = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(db_column='Keyword', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genres = models.CharField(max_length=255, blank=True, null=True)
    mood = models.CharField(max_length=255, blank=True, null=True)
    interest = models.CharField(max_length=255, blank=True, null=True)
    emotion_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Books'
        

class Recommend(models.Model):
    recommend_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.Case)
    recommend_datetime = models.DateTimeField(auto_now_add=True)
    emotion = models.CharField(max_length=20)
    answer_content = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Recommend'


class RecommendBooks(models.Model):
    mybook_id = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(Books, on_delete=models.Case)
    recommend = models.ForeignKey(Recommend, on_delete=models.Case)
    user = models.ForeignKey(Users, on_delete=models.Case)
    is_selected = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    reading_datetime = models.DateTimeField(blank=True, null=True)
    curr_page = models.IntegerField(blank=True, null=True)
    is_completed = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'Recommend_books'


class RegisterBooks(models.Model):
    register_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.Case)
    isbn = models.ForeignKey(Books, on_delete=models.Case)
    register_datetime = models.DateTimeField(auto_now_add=True)
    reading_datetime = models.DateTimeField(blank=True, null=True)
    curr_page = models.IntegerField()
    is_completed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Register_books'


class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=20)
    user = models.ForeignKey(Users, on_delete=models.Case)
    review_content = models.CharField(max_length=200, blank=True, null=True)
    satisfied = models.IntegerField(db_column='Satisfied')  # Field name made lowercase.
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Review'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'