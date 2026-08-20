"""
Phrase does not flag a translation as stale when its English source text
changes (confirmed by testing on this demo project). This script fills
that gap: it diffs the pushed resx against the previous commit to find
keys whose English value changed, then calls the Phrase API to mark
those keys' non-English translations "unverified" so they surface in
Phrase's own Verification-required view.

Only covers the mainapp project/tag in this demo. Real rollout would
loop this over every project's resx + project_id.
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

PROJECT_ID = "676b516aed3001e0832302a9060d154f"
RESX_PATH = "Properties/Resources.resx"
SOURCE_LOCALE = "en"
API_BASE = "https://api.phrase.com/v2"


def load_resx(ref):
    result = subprocess.run(
        ["git", "show", f"{ref}:{RESX_PATH}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {}
    root = ET.fromstring(result.stdout)
    entries = {}
    for data in root.findall("data"):
        value_el = data.find("value")
        entries[data.get("name")] = value_el.text if value_el is not None else ""
    return entries


def api(method, path, body=None):
    token = os.environ["PHRASE_ACCESS_TOKEN"]
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        print(f"  API error {e.code} on {method} {path}: {e.read().decode()}", file=sys.stderr)
        return None


def main():
    old = load_resx("HEAD^")
    new = load_resx("HEAD")

    changed_keys = sorted(k for k, v in new.items() if k in old and old[k] != v)

    if not changed_keys:
        print("No existing keys changed - nothing to flag.")
        return

    print(f"Changed keys: {changed_keys}")

    for key_name in changed_keys:
        q = urllib.parse.quote(f"name:{key_name}")
        keys = api("GET", f"/projects/{PROJECT_ID}/keys?q={q}")
        if not keys:
            print(f"  [{key_name}] no matching key found in Phrase, skipping")
            continue

        key_id = keys[0]["id"]
        translations = api("GET", f"/projects/{PROJECT_ID}/keys/{key_id}/translations")
        if not translations:
            continue

        for t in translations:
            locale_code = t.get("locale", {}).get("code")
            if locale_code == SOURCE_LOCALE:
                continue
            api("PATCH", f"/projects/{PROJECT_ID}/translations/{t['id']}/unverify")
            print(f"  [{key_name}] marked {locale_code} translation as unverified")


if __name__ == "__main__":
    main()
