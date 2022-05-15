from pyyoutube import Api
from videoapi.models import Video, ApiKey, Query
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from concurrent.futures import ProcessPoolExecutor
from pyyoutube.error import PyYouTubeException

api = None
api_key = None

def getConnection(expired=False):
    if expired and globals()["api_key"] and globals()["api"]:
        try:
            k = ApiKey.objects.get(key=globals()["api_key"])
            k.is_exhausted = True
            k.last_used = timezone.now()
            k.save()
        except ApiKey.DoesNotExist:
            pass
    keys = ApiKey.objects.filter(last_used__lte=timezone.now() - timedelta(hours=24))
    donot = True
    if not keys.exists():
        keys = ApiKey.objects.all()
        donot = False
        print("No Keys Available")
    if donot:
        keys.exclude(key=globals()["api_key"])
    key = keys[0]
    key.last_used = timezone.now()
    key.is_exhausted = False
    key.save()
    api = Api(api_key=key.key)
    globals()["api_key"] = key.key
    globals()["api"] = api


getConnection()


def update_data():
    queries = Query.objects.all().values_list("query", flat=True)
    proc_count = min(queries.count(), 8)
    if proc_count == 0:
        proc_count = 4
    objs = []
    with ProcessPoolExecutor(proc_count) as exec:
        for i in exec.map(get_videos, queries):
            objs.extend(i)
    Video.objects.bulk_create(objs, ignore_conflicts=True)
    return 0


def get_videos(query: str):
    running = False
    try:
        published = timezone.now() - timedelta(seconds=20)
        searches = api.search_by_keywords(
            q=query, search_type=["video"], count=100,
            limit=100,publishedAfter=published.strftime("%Y-%m-%dT%H:%M:%SZ")
        )
    except PyYouTubeException as e:
        print("expired ",api_key)
        if str(e).__contains__("exceeded"):
            getConnection(expired=True)
            running = True
    if running:
        return list()

    searches = searches.items
    proc_count = min(len(searches), 16)
    if proc_count == 0:
        proc_count = 4
    with ProcessPoolExecutor(proc_count) as exec:
        objs = list(exec.map(insert_in_db, searches))
    return objs


def insert_in_db(data):
    data = data.to_dict()
    obj = Video(id=data["id"]["videoId"])
    obj.title = data["snippet"]["title"]
    obj.description = data["snippet"]["description"]
    if obj.thumbnails is None:
        obj.thumbnails = []
    for _, thumbs in data["snippet"]["thumbnails"].items():
        if thumbs is None or "url" not in thumbs:
            pass
        obj.thumbnails.append(thumbs["url"])
    obj.publishedAt = datetime.strptime("%Y-%m-%dT%H:%M:%S%Z")
    return obj
