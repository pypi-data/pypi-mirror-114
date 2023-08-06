#  Copyright © 2021 Ingram Micro Inc. All rights reserved.

import logging
from datetime import timedelta

from dj_cqrs.constants import DEFAULT_CQRS_MESSAGE_TTL, DEFAULT_DELAY_QUEUE_MAX_SIZE

from django.conf import settings
from django.utils import timezone


logger = logging.getLogger('django-cqrs')


def get_expires_datetime():
    """Calculates when message should expire.

    :return: datetime instance, None if infinite
    :rtype: datetime.datetime
    """
    master_settings = settings.CQRS.get('master', {})
    if 'CQRS_MESSAGE_TTL' in master_settings and master_settings['CQRS_MESSAGE_TTL'] is None:
        # Infinite
        return

    min_message_ttl = 1
    message_ttl = master_settings.get('CQRS_MESSAGE_TTL', DEFAULT_CQRS_MESSAGE_TTL)
    if not isinstance(message_ttl, int) or message_ttl < min_message_ttl:
        logger.warning(
            "Settings CQRS_MESSAGE_TTL=%s is invalid, using default %s.",
            message_ttl, DEFAULT_CQRS_MESSAGE_TTL,
        )
        message_ttl = DEFAULT_CQRS_MESSAGE_TTL

    return timezone.now() + timedelta(seconds=message_ttl)


def get_delay_queue_max_size():
    """Returns delay queue "waiting" messages number.

    :return: integer instance, None if infinite
    :rtype: int
    """
    replica_settings = settings.CQRS.get('replica', {})
    max_size = DEFAULT_DELAY_QUEUE_MAX_SIZE
    if 'delay_queue_max_size' in replica_settings:
        max_size = replica_settings['delay_queue_max_size']

    if max_size is not None and max_size <= 0:
        logger.warning(
            "Settings delay_queue_max_size=%s is invalid, using default %s.",
            max_size, DEFAULT_DELAY_QUEUE_MAX_SIZE,
        )
        max_size = DEFAULT_DELAY_QUEUE_MAX_SIZE
    return max_size


def get_prefetch_count():
    """Returns per worker consuming (unacked) messages number limit.

    :return: integer instance, 0 if infinite
    :rtype: int
    """
    delay_queue_max_size = get_delay_queue_max_size()
    prefetch_count = 0  # Infinite
    if delay_queue_max_size is not None:
        # 1 message is in progress, others could be delayed
        prefetch_count = delay_queue_max_size + 1
    return prefetch_count
