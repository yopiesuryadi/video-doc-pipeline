#!/usr/bin/env python3
"""Set metadata, thumbnail, and captions on a YouTube video via the Data API.

The video file itself is uploaded manually in YouTube Studio (or via yt_upload.py
once the project passes API audit). This script fills in everything else — the
part that is all clicks and easy to get wrong by hand.

Usage:
  yt_publish.py --video-id <ID> \
      --title "..." \
      --description-file work/youtube/DESCRIPTION.txt \
      [--tags "a,b,c"] \
      [--category 22] \
      [--thumbnail work/youtube/COVER.jpg] \
      [--caption en=work/youtube/KENYA-EN.srt] \
      [--caption id=work/youtube/KENYA-ID.srt] \
      [--privacy unlisted]

--video-id is the 11-char id from the watch URL (youtu.be/<ID>).
Each --caption is LANG=path; repeat for multiple languages. Existing tracks in
the same language are replaced, not duplicated.
"""
import argparse
import os
import sys
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from yt_common import get_service


def set_metadata(yt, video_id, title, description, tags, category, privacy):
    # Fetch current snapshot so we only override what we were given.
    resp = yt.videos().list(part="snippet,status", id=video_id).execute()
    if not resp.get("items"):
        raise SystemExit(f"Video {video_id} not found (wrong account?)")
    item = resp["items"][0]
    snip = item["snippet"]
    if title is not None:
        snip["title"] = title
    if description is not None:
        snip["description"] = description
    if tags is not None:
        snip["tags"] = tags
    if category is not None:
        snip["categoryId"] = str(category)
    body = {"id": video_id, "snippet": snip}
    parts = "snippet"
    if privacy:
        item["status"]["privacyStatus"] = privacy
        body["status"] = item["status"]
        parts = "snippet,status"
    yt.videos().update(part=parts, body=body).execute()
    print(f"metadata updated: title={snip['title']!r} privacy={privacy or 'unchanged'}")


def set_thumbnail(yt, video_id, path):
    yt.thumbnails().set(
        videoId=video_id, media_body=MediaFileUpload(path)
    ).execute()
    print(f"thumbnail set: {path}")


def set_caption(yt, video_id, lang, path):
    # Replace an existing same-language track so re-runs don't pile up duplicates.
    existing = yt.captions().list(part="snippet", videoId=video_id).execute()
    for track in existing.get("items", []):
        if track["snippet"]["language"] == lang:
            yt.captions().delete(id=track["id"]).execute()
            print(f"  removed old {lang} caption")
    yt.captions().insert(
        part="snippet",
        body={"snippet": {"videoId": video_id, "language": lang, "name": lang.upper(), "isDraft": False}},
        media_body=MediaFileUpload(path),
    ).execute()
    print(f"caption added: {lang} <- {path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video-id", required=True)
    p.add_argument("--title")
    p.add_argument("--description-file")
    p.add_argument("--tags")
    p.add_argument("--category", default="22")  # 22 = People & Blogs
    p.add_argument("--thumbnail")
    p.add_argument("--caption", action="append", default=[], metavar="LANG=PATH")
    p.add_argument("--privacy", choices=["private", "unlisted", "public"])
    args = p.parse_args()

    description = None
    if args.description_file:
        with open(args.description_file, encoding="utf-8") as f:
            description = f.read()
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    yt = get_service()
    try:
        set_metadata(yt, args.video_id, args.title, description, tags, args.category, args.privacy)
        if args.thumbnail:
            set_thumbnail(yt, args.video_id, args.thumbnail)
        for spec in args.caption:
            lang, _, path = spec.partition("=")
            if not path:
                sys.exit(f"bad --caption {spec!r}, expected LANG=PATH")
            set_caption(yt, args.video_id, lang, path)
    except HttpError as e:
        sys.exit(f"YouTube API error: {e}")
    print("done.")


if __name__ == "__main__":
    main()
