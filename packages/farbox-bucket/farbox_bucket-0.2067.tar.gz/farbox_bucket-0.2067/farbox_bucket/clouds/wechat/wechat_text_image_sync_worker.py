#coding: utf8
import re
import requests
import gevent
import ujson as json
from flask import request
from farbox_bucket.utils.memcache import get_cache_client
from farbox_bucket.utils import smart_unicode
from farbox_bucket.bucket.utils import get_now_from_bucket
from farbox_bucket.bucket.record.get.path_related import get_json_content_by_path
from farbox_bucket.server.helpers.file_manager_downloader import download_from_internet_and_sync
from farbox_bucket.server.helpers.markdown_doc_append_worker import append_to_markdown_doc_and_sync
from farbox_bucket.server.helpers.file_manager import sync_file_by_server_side

from .bind_wechat import set_name_by_wechat_user_id, get_name_by_wechat_user_id
from .utils.token import get_access_token


#    #tag #hello [[ #wiki_tag ]] [[#more]] test
def compile_tag_to_wiki_link_syntax(content, is_voice=False):
    content = re.sub("(?<!\[)(#[^# \t]+)", "[[\g<1>]]", content)
    content = re.sub("(\[\s*){2,}\[", "[[", content)
    content = re.sub("(\]\s*){2,}\]", "]]", content)
    if is_voice and u"标签" in content:
        p1, p2 = content.rsplit(u"标签", 1)
        if u"，" not in p2:
            p2 = p2.replace(u"。", "").strip()
            if len(p2) <= 5:
                content = u"%s[[#%s]]。" % (p1, p2)
    return content


def get_video_from_wechat(bucket, access_token, media_id, path):
    if not bucket or not access_token or not media_id or not path:
        return
    url = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (access_token, media_id)
    try:
        response = requests.get(url, timeout=160, verify=False)
        if response.status_code == 200:
            if len(response.content) < 10*1024:
                try:
                    video_url = response.json().get("video_url")
                    if video_url:
                        download_from_internet_and_sync(bucket=bucket, url=video_url, path=path, timeout=160, client="wechat")
                        # break now
                        return
                except:
                    pass
            sync_file_by_server_side(bucket=bucket,
                                     relative_path=path,
                                     content=response.content,
                                     is_dir=False,
                                     is_deleted=False,
                                     client="wechat")

    except:
        pass

def get_audio_from_wechat(bucket, access_token, media_id, path):
    url = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (access_token, media_id)
    download_from_internet_and_sync(bucket=bucket, url=url, path=path, timeout=60, client="wechat")


def wechat_text_image_handler(wechat_user_id, bucket, xml_data):
    msg_id = xml_data.get("MsgId")
    create_time = xml_data.get("CreateTime")
    msg_type = xml_data.get("MsgType")
    media_id = xml_data.get("MediaId")

    # post_root, auto_add_date(bool), silent_reply(bool), image_folder, image_insert_type(image/markdown_syntax)
    wechat_configs = get_json_content_by_path(bucket, "__wechat.json", force_dict=True)

    is_chanel_2 = request.values.get("chanel") == "2"

    # for Debug
    xml_data["is_chanel_2"] = is_chanel_2
    cache_client = get_cache_client()
    cache_client.set("last_wechat_message", data = json.dumps(xml_data), expiration=60*60*24)

    today = get_now_from_bucket(bucket, "%Y-%m-%d")
    silent_reply = wechat_configs.get("silent_reply") or False
    post_root = (wechat_configs.get("post_folder") or "").strip("/")
    auto_add_date = wechat_configs.get("auto_add_date", False)
    add_nickname = wechat_configs.get("add_nickname", False)
    draft_by_default = wechat_configs.get("draft_by_default", False)
    one_user_one_post = wechat_configs.get("one_user_one_post", False)
    user_post_per_day = wechat_configs.get("user_post_per_day", False)

    if msg_type == "image":  # 纯图片
        pic_url = xml_data.get("PicUrl")
        if not pic_url:
            return "error: PicUrl is blank"
        filename = "%s.jpg" % (msg_id or create_time)
        image_insert_type = wechat_configs.get("image_insert_type")
        raw_image_folder = smart_unicode(wechat_configs.get("image_folder") or "").strip("/")
        image_folder = smart_unicode(raw_image_folder) or today
        if image_insert_type == "image":  # 直接保存图片
            path = "%s/%s" % (image_folder, filename)
            download_from_internet_and_sync(bucket=bucket, url=pic_url, path=path, timeout=60) # 下载图片并进行保存
            if silent_reply:
                return ""
            else:
                return u"将保存到 %s" % path
        else:
            if raw_image_folder:
                # 还是按照 day 增加一层子目录，避免多了找不到的情况
                path = "/%s/%s/%s" % (raw_image_folder, today, filename)
            else:
                path = "/_image/%s/%s" % (today, filename)
            text_to_append = "![](%s)" % path  # 插入图片的语法
            download_from_internet_and_sync(bucket=bucket, url=pic_url, path=path, timeout=60)
    elif (msg_type == "video" or msg_type == "shortvideo") and media_id:
        path_to_store = get_now_from_bucket(bucket, time_format="/_private/video/%Y/%Y-%m-%d/%Y-%m-%d %H-%M-%S.mp4")
        # text_to_append = "![%s](%s)" % (media_id, path_to_store)
        text_to_append = "![](%s)" % path_to_store

        access_token = get_access_token(is_chanel_2=is_chanel_2)
        if access_token:
            gevent.spawn(get_video_from_wechat, bucket, access_token, media_id, path_to_store)
        else:
            text_to_append = ""

    else:
        text_to_append = xml_data.get("Content") or xml_data.get("Recognition") or xml_data.get("EventKey") or ""

    if msg_type == "voice":
        # 语音也保存一份
        path_to_store = get_now_from_bucket(bucket, time_format="/_private/audio/%Y/%Y-%m-%d/%Y-%m-%d %H-%M-%S.amr")
        access_token = get_access_token(is_chanel_2=is_chanel_2)
        if access_token:
            get_audio_from_wechat(bucket=bucket, access_token=access_token, media_id=media_id, path=path_to_store)


    text_to_append = text_to_append.strip()

    if "\n" not in text_to_append and re.match(u"name ", text_to_append):
        name = text_to_append[5:].strip()
        if name:
            set_name_by_wechat_user_id(wechat_user_id, name)
            return u"昵称已设定为 %s" % name

    if one_user_one_post:
        if user_post_per_day:
            today_string = get_now_from_bucket(bucket, "%Y-%m-%d")
        else:
            today_string = ""
        if post_root:
            if today_string:
                post_path = "%s/%s/%s.txt" % (post_root, wechat_user_id, today_string)
            else:
                post_path = "%s/%s.txt" %  (post_root, wechat_user_id)
        else:
            if today_string:
                post_path = "%s/%s.txt" % (wechat_user_id, today_string)
            else:
                post_path = "%s.txt" % wechat_user_id
    else:
        if post_root:
            post_path = post_root + "/" + get_now_from_bucket(bucket, "%Y-%m-%d.txt")
        else:
            post_path = get_now_from_bucket(bucket, "%Y/%Y-%m-%d.txt")


    if text_to_append.strip() == "reset":
        if one_user_one_post:
            sync_file_by_server_side(bucket=bucket, relative_path=post_path, content=" ")
            return u"%s 已重置" % post_path
        else:
            return u"只有 `One User One Post` 的时候才能使用 reset 命令。"

    if text_to_append:
        if add_nickname:
            nickname = get_name_by_wechat_user_id(wechat_user_id)
            if nickname:
                text_to_append = "%s: %s" % (nickname, text_to_append)

        if auto_add_date and "\n" not in text_to_append:
            if text_to_append.startswith("---") or re.match(u"\w+[:\uff1a]", text_to_append):
                auto_add_date = False
        if auto_add_date: # 添加时间戳
            bucket_now = get_now_from_bucket(bucket, "%Y-%m-%d %H:%M:%S")
            text_to_append = "%s %s"%(bucket_now, text_to_append)

        is_voice = True if xml_data.get("Recognition") else False
        text_to_append = compile_tag_to_wiki_link_syntax(text_to_append, is_voice=is_voice)

        # 保存文章, 5 分钟的间隔自动多一个空line
        append_to_markdown_doc_and_sync(bucket=bucket, path=post_path, content=text_to_append,
                                        lines_more_diff=5*60, draft_by_default=draft_by_default)

        if silent_reply:
            return ""
        else:
            return u"已保存至 %s" % post_path
