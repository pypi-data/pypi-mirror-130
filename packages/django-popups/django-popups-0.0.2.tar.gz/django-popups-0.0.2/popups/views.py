from django.shortcuts import render
from .models import NotiPopups, EventPopups, ImagePopups

import json
import logging
import pprint

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def test(request):
    noti_popups = NotiPopups.objects
    event_popups = EventPopups.objects
    image_popups = ImagePopups.objects
    context = {'noti_popups': noti_popups, 'event_popups': event_popups, 'image_popups': image_popups}
    logger.info(context)
    return render(request, 'popups/test.html', context)


def make_context() -> dict:
    noti_popups = NotiPopups.objects
    event_popups = EventPopups.objects
    image_popups = ImagePopups.objects
    context = {'noti_popups': noti_popups, 'event_popups': event_popups, 'image_popups': image_popups}
    return context
