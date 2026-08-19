#!/usr/bin/env python3
"""
Check every quotation on index.html against the sources it attributes them to.

Prefers a live fetch of each source. Falls back to the committed snapshot in
sources/ when the network is unavailable, and says which mode it used.

Exit codes: 0 all quotations verbatim, 1 one or more failed, 2 could not
obtain a source at all.

Each quotation is checked against the sources its own claim cites, not against
whichever article happens to contain it.

Read the COVERAGE section this prints. A green run means every quotation is
verbatim. It does not mean the page is checked.
"""
import json, os, re, sys, html, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def to_text(raw):
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("—", "-"), ("–", "-")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().strip('"')


def load_sources():
    spec = json.load(open(os.path.join(HERE, "sources.json"), encoding="utf-8"))
    out = {}
    for s in spec:
        text, mode = None, None
        try:
            req = urllib.request.Request(s["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                text, mode = to_text(r.read().decode("utf-8", "replace")), "live"
        except Exception as e:
            snap = os.path.join(HERE, s["snapshot"])
            if os.path.exists(snap):
                text = open(snap, encoding="utf-8").read()
                mode = "snapshot %s (live fetch failed: %s)" % (s["fetched_utc"], type(e).__name__)
        if text is None:
            print("CANNOT OBTAIN SOURCE: %s" % s["name"])
            sys.exit(2)
        out[s["name"]] = {"text": norm(text), "mode": mode, "url": s["url"]}
    return out


def main():
    page = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    srcs = load_sources()
    url_to_name = {s["url"]: n for n, s in srcs.items()}

    for name, s in srcs.items():
        print("SOURCE %-9s %s" % (name, s["mode"]))
    print()

    # Pair each quotation with the sources its own <li> cites, so a sentence
    # that appears in both articles is checked against the one claimed.
    items = re.findall(r"<li>(.*?)</li>", page, flags=re.S)
    pairs = []
    for item in items:
        cited = [url_to_name[u] for u in re.findall(r'href="([^"]+)"', item)
                 if u in url_to_name]
        for q in re.findall(r"<q>(.*?)</q>", item, flags=re.S):
            pairs.append((q, cited))
    loose = [q for q in re.findall(r"<q>(.*?)</q>", page, flags=re.S)
             if not any(q == pq for pq, _ in pairs)]
    for q in loose:
        pairs.append((q, []))

    fails = warns = unattributed = 0
    for q, cited in pairs:
        exact = norm(q)
        lenient = exact.rstrip(",.;:")
        tail = exact[len(lenient):]

        search = cited if cited else list(srcs)
        if not cited:
            unattributed += 1

        where = src_tail = None
        for name in search:
            i = srcs[name]["text"].find(lenient)
            if i != -1:
                where = name
                src_tail = srcs[name]["text"][i + len(lenient):i + len(lenient) + 1]
                break

        if where is None:
            elsewhere = [n for n in srcs if lenient in srcs[n]["text"]]
            fails += 1
            print("FAIL  %s%s"
                  % (exact[:88],
                     ("  (found in %s, which this claim does not cite)" % ", ".join(elsewhere))
                     if elsewhere else ""))
            continue

        # Trailing punctuation compared explicitly. The lenient match above is
        # what let a comma-to-period change pass silently once already.
        if tail and src_tail and tail[0] != src_tail:
            warns += 1
            print("WARN  [%s] ends %r, source has %r  |  %s"
                  % (where, tail[0], src_tail, exact[:66]))
        else:
            print("OK    [%s]%s %s"
                  % (where, "" if cited else " (unattributed)", exact[:84]))

    claims = re.findall(r"<li>\s*<p>(.*?)</p>", page, flags=re.S)
    unquoted = 0
    for c in claims:
        stripped = re.sub(r"<q>.*?</q>", "", c, flags=re.S)
        if len(norm(stripped)) > 40:
            unquoted += 1

    print("\nRESULT  %d quotations, %d failed, %d punctuation warnings, %d unattributed"
          % (len(pairs), fails, warns, unattributed))
    print("""
COVERAGE, and what this does not catch
  1. It checks quotations only. Assertions in prose are not verified by
     anything here. This page previously stated "He did not get into the
     class", which no source says; that was caught by re-reading, not by
     this script, and a green run would not have flagged it.
  2. %d sourced paragraphs carry prose outside their quotation marks. Every
     one of those sentences is unchecked by this tool.
  3. It cannot tell whether a quotation is fair in context, or whether the
     claim built around it follows from it.
  4. Snapshots in sources/ are a point-in-time copy. If an article is later
     corrected, a snapshot run will keep passing against the old text.""" % unquoted)

    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
