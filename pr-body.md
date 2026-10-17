This PR adds a 1200×630 Open Graph / Twitter social preview to the single-file reading site. Right now the page has `title` and `description` but **zero `og:`/`twitter:` tags**, so every link shared on social platforms renders as a bare URL with no preview card.

**What's included:**
- Full OG meta set (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) with absolute production URLs
- Twitter Card `summary_large_image` tags
- 1200×630 `og-image.png` in the site's brand palette (#3451b2/#3a5ccc) with CJK typography — headline "用最少的钱、时间 换回寿命、金钱与自由", evidence-grade chips (A/B/C), and site URL
- The same meta block added to `build.py`'s head template so **regenerated index.html keeps the tags** (the current index.html is also patched)
- `make-og-image.py` — portable Pillow-only generator (WQY Zen Hei CJK font, no machine-specific paths) so the card is reproducible

Verified: image QA'd for CJK rendering, alignment, and contrast; file is 104 KB (well under the 1 MB crawler limit); tags placed before title/style in `<head>`.

Preview card will show when the URL is shared on X/Twitter, LinkedIn, Slack, WeChat, etc.