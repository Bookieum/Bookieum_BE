from django.db import models


class Answer(models.Model):
    answer_id = models.CharField(primary_key=True, max_length=20)
    question = models.ForeignKey('Question', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    answer_content = models.CharField(max_length=20)
    answer_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'answer'


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


class Books(models.Model):
    isbn_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    pub_date = models.CharField(max_length=255, blank=True, null=True)
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
        db_table = 'books'


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


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Question(models.Model):
    question_id = models.CharField(primary_key=True, max_length=20)
    question_content = models.CharField(max_length=20)
    question_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question'


class Recommend(models.Model):
    recommend_id = models.CharField(primary_key=True, max_length=20)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    recommend_datetime = models.DateTimeField()
    emotion = models.CharField(max_length=20)
    answer_content = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'recommend'


class RecommendBooks(models.Model):
    mybook_id = models.CharField(primary_key=True, max_length=20)
    recommend = models.ForeignKey(Recommend, models.DO_NOTHING)
    isbn = models.ForeignKey(Books, models.DO_NOTHING)
    user_id = models.CharField(max_length=20)
    is_selected = models.IntegerField(db_comment='1: 선택 / 0: 선택X')
    created_datetime = models.DateTimeField()
    reading_datetime = models.DateTimeField(blank=True, null=True)
    curr_page = models.IntegerField(blank=True, null=True)
    is_completed = models.IntegerField(db_comment='1: 완료 / 0: 미완료')

    class Meta:
        managed = False
        db_table = 'recommend_books'


class RegisterBooks(models.Model):
    register_id = models.CharField(primary_key=True, max_length=20)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    isbn = models.ForeignKey(Books, models.DO_NOTHING)
    register_datetime = models.DateTimeField()
    reading_datetime = models.DateTimeField(blank=True, null=True)
    curr_page = models.IntegerField()
    is_completed = models.IntegerField(blank=True, null=True, db_comment='1: 완료 / 0: 미완료')

    class Meta:
        managed = False
        db_table = 'register_books'


class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=20)
    isbn = models.ForeignKey(Books, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    review_content = models.CharField(max_length=200)
    satisfied = models.IntegerField(db_comment='1: 만족 / 0: 불만족')
    created_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=200)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.JSONField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)
    provider_id = models.CharField(max_length=200)
    settings = models.JSONField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    user_name = models.CharField(max_length=20)
    reading_level = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, db_comment=' F: 여성 / M: 남성')
    home_addr = models.CharField(max_length=50, blank=True, null=True)
    register_datetime = models.DateTimeField()
    share_cnt = models.IntegerField()
    genre = models.CharField(max_length=30, db_comment='선호 장르')

    class Meta:
        managed = False
        db_table = 'users'
