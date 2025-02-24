import json
from datetime import datetime
from fastapi import APIRouter, Body, Request
from pywebpush import webpush, WebPushException

import config
import logging

router = APIRouter()

logger = logging.getLogger("uvicorn.error")


def get_subscriptions(id: int):
    try:
        with open("subscriptions.json", "r") as file:
            subscriptions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        subscriptions = {}

    return subscriptions.get(str(id), [])


def save_subscriptions(subscriptions):
    with open("subscriptions.json", "w") as file:
        json.dump(subscriptions, file)


@router.post("/publish")
def publish(request: Request, payload: dict = Body(...)):

    options = {
        "body": payload.get("body"),
        "tag": "notification: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "icon":               "/assets/img/icon/cloud-192.png",
        "badge":              "/assets/img/icon/cloud-192.png",
        "requireInteraction": False,
    }

    message = {
        "title": payload.get("title"),
        "options": options,
    }

    id = payload.get("id")
    subscriptions = get_subscriptions(id)
    if not subscriptions:
        return {"status": "error", "message": "Subscription not found"}

    webpush_options = {
        "subscriber":      "mailto:example@example.com",
        "VAPIDPublicKey":  config.VAPID_PUBLIC_KEY,
        "VAPIDPrivateKey": config.VAPID_PRIVATE_KEY,
    }

    for subscription in subscriptions[:]:
        try:
            # Send the push notification
            webpush(
                subscription_info=subscription,
                data=json.dumps(message),
                vapid_private_key=webpush_options.get("VAPIDPrivateKey"),
                vapid_claims={"sub": webpush_options.get("subscriber")}
            )
        except WebPushException as ex:
            if ex.response is not None and ex.response.status_code in [404, 410]:
                subscriptions.remove(subscription)
                logger.info("Removed subscription invalid subscription.")
                save_subscriptions({str(id): subscriptions})
            else:
                return {"status": "error", "message": str(ex)}

    return {"status": "success"}


@router.get("/vapid-public-key")
async def get_vapid_public_key():
    return {"publicKey": config.VAPID_PUBLIC_KEY}


@router.post("/subscribe")
def subscribe(request: Request, payload: dict = Body(...)):
    try:
        with open("subscriptions.json", "r") as file:
            subscriptions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        subscriptions = {}

    id = str(payload.get("id"))
    subscription_info = payload.get("subscription")

    if id not in subscriptions:
        subscriptions[id] = []

    subscriptions[id].append(subscription_info)

    with open("subscriptions.json", "w") as file:
        json.dump(subscriptions, file)

    return {"status": "success"}


@router.post("/unsubscribe")
def unsubscribe(request: Request, payload: dict = Body(...)):
    try:
        with open("subscriptions.json", "r") as file:
            subscriptions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        subscriptions = {}

    id = str(payload.get("id"))
    subscription_info = payload.get("subscription")

    if id in subscriptions:
        subscriptions[id] = [
            sub for sub in subscriptions[id]
            if sub != subscription_info]

    with open("subscriptions.json", "w") as file:
        json.dump(subscriptions, file)

    return {"status": "success"}
