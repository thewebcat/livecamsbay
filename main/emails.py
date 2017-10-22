# coding=utf-8
from email_sender.email_actions import email_action_reg


@email_action_reg(u'Контент отправлен на модерацию')
def content_to_moderate(content):
    profile = content.profile
    return profile, {'name': profile.name, 'content_name': content.title, 'content_type': content.get_beauty_name_plural()}


@email_action_reg(u'Контент опубликован')
def content_to_publish(content):
    profile = content.profile
    return profile, {'name': profile.name, 'content_name': content.title,
                     'content_type': content.get_beauty_name_plural(), 'content_link': content.absolute_public_url}


@email_action_reg(u'Новый отзыв')
def model_recall(recall):
    profile = recall.order.performer
    return profile, {'name': profile.name, 'order_name': recall.order,
                     'recall_link': profile.absolute_public_url + '?to_recalls=1'}


@email_action_reg(u'Модель появилась онлайн!')
def model_went_online(profile, model):
    return profile, {'name': profile.name, 'model_name': model.display_name,
                     'service_name': model.cam_service.name, 'model_link': model.absolute_public_url}