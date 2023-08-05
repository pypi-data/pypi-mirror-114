# -*- coding:utf-8 -*-
from __future__ import unicode_literals, print_function
from django.dispatch import receiver
from django.db.models.signals import post_save
from xyz_auth.signals import to_get_user_profile
from xyz_saas.signals import to_get_party_settings
from xyz_verify.models import Verify
from . import models, helper, serializers, choices
from django.conf import settings
from xyz_util.datautils import access
import logging

log = logging.getLogger("django")

@receiver(to_get_user_profile)
def get_membership_setting(sender, **kwargs):
    user = kwargs['user']
    if hasattr(user, 'as_clockin_member'):
        return serializers.MemberShipSerializer(user.as_clockin_membership, context=dict(request=kwargs['request']))


@receiver(to_get_party_settings)
def get_school_settings(sender, **kwargs):
    return {'school': {'student': {'unregistered': access(settings, 'SCHOOL.STUDENT.UNREGISTERED')}}}


@receiver(post_save, sender=Verify)
def create_student_after_verify(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        return
    helper.create_student_after_verify(kwargs.get('instance'))


def create_student_for_wechat_user(sender, **kwargs):
    wuser = kwargs['instance']
    helper.create_informal_student(wuser.user)


def bind_create_student_for_wechat_user_receiver():
    b = access(settings, 'SCHOOL.STUDENT.UNREGISTERED')
    if not b or b.lower() != 'create_from_wechat':
        return
    from xyz_wechat.models import User
    from django.db.models.signals import post_save
    print('bind_create_student_for_wechat_user_receiver')
    post_save.connect(create_student_for_wechat_user, sender=User)


bind_create_student_for_wechat_user_receiver()
