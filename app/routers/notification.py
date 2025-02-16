from datetime import datetime
import json
from fastapi import Body, Request
from pywebpush import webpush, WebPushException

from fastapi import APIRouter

router = APIRouter()


def get_subscriptions(id: int):
    try:
        with open("subscriptions.json", "r") as file:
            subscriptions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        subscriptions = {}

    return subscriptions.get(str(id))


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
    subscription = get_subscriptions(id)
    if subscription is None:
        return {"status": "error", "message": "Subscription not found"}

    if not subscription.get("active"):
        return {"status": "error", "message": "Subscription is not active"}

    subscription = subscription.get("sub")
    webpush_options = {
        "subscriber":      "mailto:example@example.com",
        "VAPIDPublicKey":  "BDOpUfHEw7LFRJWhDxF5TW7SR-kiaOY-_6iFrVweY8rfmi9ySzjxSGWbbm-wwriXwAYWVX5808Pb2U2ApYXYKLc",
        "VAPIDPrivateKey": "TkyndbWdGc_D3ukx9tbfh5_ElMjRzL0ixQ86JAMtDzI",
    }
    try:
        # Send the push notification
        webpush(
            subscription_info=subscription,
            data=json.dumps(message),
            vapid_private_key=webpush_options.get("VAPIDPrivateKey"),
            vapid_claims={"sub": webpush_options.get("subscriber")}
        )
        return {"status": "success"}
    except WebPushException as ex:
        return {"status": "error", "message": str(ex)}


@router.post("/subscribe")
def subscribe(request: Request, payload: dict = Body(...)):
    try:
        with open("subscriptions.json", "r") as file:
            subscriptions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        subscriptions = {}

    data = {
        str(payload.get("id")): {
            "sub": payload.get("subscription"),
            "active": True
        }}
    subscriptions.update(data)

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

    subscriptions.update({str(payload.get("id")): {"active": False}})

    with open("subscriptions.json", "w") as file:
        json.dump(subscriptions, file)

    return {"status": "success"}
