from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.contrib.auth.models import PermissionsMixin
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from ..model.roles import Roles

class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('mobile', username)
        # group, created = Group.objects.get_or_create(name='super_admin')
        # extra_fields.setdefault('group_id', group.id)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class UserPermissionMixin(PermissionsMixin):
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False,
                                       help_text=_(
                                           'Designates that this user has all permissions without '
                                           'explicitly assigning them.'
                                       ),
                                       )

    groups = None
    user_permissions = None
    is_staff = False

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        pass

    def get_all_permissions(self, obj=None):
        pass


class User(AbstractBaseUser,PermissionsMixin):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        email and password are required. Other fields are optional.
        is_active : restrict from login true when login, false is not login
        is_superuser/ is_staff : for superuser, admin this is true
        is_verified : users in category dealership and showrooms are verified by admin
        """
    first_name = models.CharField(_('first name'), max_length=256, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=256, blank=True, null=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    mobile = models.CharField(_('mobiles'), max_length=16, null=True, blank=True, db_index=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        null=True,
        blank=True,unique=True
    )
    # group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE,related_name="user_group")
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'), )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    STATUS_CHOICES = ((1, 'active'),(2, 'inactive'),(3,'deleted'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    
    created_by = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True)
    objects = CustomUserManager()
    email_hash = models.CharField(blank=True,null=True,max_length=255)
    hash_time = models.DateTimeField(blank=True,null=True,)
    login_otp = models.CharField(max_length=10, blank=True, null=True)
    login_otp_time = models.DateTimeField(blank=True, null=True)
    otp = models.CharField(max_length=20, blank=True, null=True)
    otp_time = models.DateTimeField(blank=True, null=True)
    new_otp = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
