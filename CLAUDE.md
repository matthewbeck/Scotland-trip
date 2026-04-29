# Scotland & Netherlands 2026 Trip — Itinerary App

A self-contained HTML app deployed to GitHub Pages, used as a phone home-screen "app" during a 28-day family trip across Scotland and the Netherlands (Apr 14 – May 12, 2026). Family of three: me, my wife Lisa, our infant son Casper.

## Live URL
https://matthewbeck.github.io/Scotland-trip/

## Source of truth
`index.html` — single file. All data is embedded as JS objects in a `<script>` block. No build step. GitHub Pages serves the file directly from `main`.

## Design system

"Editorial Voyager" — don't change the design system without flagging:

- **Fonts:** Epilogue (serif headings) + Plus Jakarta Sans (body)
- **Palette:** Obsidian dark (#131313), Sunset Orange (#ffb59c), Electric Blue (#adc7ff)
- **Layout:** Tonal layering instead of borders, glassmorphism nav/footer
- **Interaction:** Expand/collapse timeline cards, inline explore sections, alerts at top

The `apple-touch-icon` is embedded inline as a base64 data URI (S&N monogram).

## Data structure

Two top-level arrays in the `<script>` block:

1. **`alerts`** — top-of-page warnings/info messages (`{ type, text }`). Prune entries whose date has passed; they're for upcoming logistics, not history.
2. **`segments`** — the timeline cards

Each segment:

```js
{
  id: 's0',                    // sequential, x-suffix for explore (s4x, s10x, s11x)
  type: 'flight',              // flight | train | car | stay | explore
  icon: '✈',
  eyebrow: 'Flight · Departure',
  title: 'YVR → AMS',
  sub: 'Apr 14 · 17:50 – 12:05+1',
  emailLink: 'https://mail.google.com/...',  // optional Gmail deep link
  start: '2026-05-01',                        // optional ISO date — drives the "↓ Today" button
  end:   '2026-05-04',                        // optional ISO end date for multi-day stays
  details: [                                  // optional, for bookings
    { label: 'Depart', value: '...' },
  ],
  explore: [                                  // optional, for explore segments
    { cat: '☕ Coffee', items: [{ name, meta, tag, maps }] },
  ],
  tickets: [                                  // optional, scannable QR per passenger
    { passenger: 'Adult 1 · CBBNXCQJV4N', image: 'data:image/png;base64,...' },
  ],
}
```

**`start`/`end` semantics:** the "↓ Today" button in the header finds the active segment by checking, in order: an active `stay` whose `start <= today <= end`; an event with `start === today`; the next upcoming `start > today`. Past segments don't need dates (they'll never be "current" again), but future segments should have them.

When inserting new segments mid-timeline, **don't renumber** — use the next available id (e.g. `s10b` between `s10` and `s10x`).

### Generating QR codes for `tickets`

QR payload strings (e.g. `CBBNXCQJV4N`) come from the `agentic-email` MCP server's `get_travel_itinerary` call (under `rawBarcodes`). To turn a payload into a scannable QR data URI:

```bash
python3 -c "
import segno, base64, io
qr = segno.make('CBBNXCQJV4N', error='H')
buf = io.BytesIO(); qr.save(buf, kind='png', scale=8, border=2)
print('data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode())
"
```

Each PNG is ~275 bytes (~390-char data URI). `segno` is pure-Python, no deps; install once with `python3 -m pip install --user segno`.

There is also a dormant `qrUrl` field on a couple of segments (KLM, Eurostar) referencing external QR-generator URLs — its render path isn't wired up. Use `tickets` instead.

## Critical gotcha: apostrophes

**Apostrophes inside single-quoted JS strings break the parser.** Things like `'St Bernard's Well'`, `'Mary King's Close'`, `'London's best...'` fail silently — the page goes blank.

Two fixes:
- Switch the entry to double quotes: `"St Bernard's Well"`
- Reword to avoid it: `London's` → `London`

## Workflow

After every edit:

```bash
python3 scripts/validate.py
```

Must print `OK: balanced`. If not, fix before committing.

Then:

```bash
git add index.html
git commit -m ""
git push origin main
```

GitHub Pages redeploys in ~60 seconds.

## Trip itinerary (current state as of Apr 29, 2026)

| Dates | Segment | Status |
|-------|---------|--------|
| Apr 14–15 | KL0682 YVR→AMS | Done |
| Apr 15–20 | The Hague | Done |
| Apr 20 | NS Den Haag→London via Brussels | Done |
| Apr 20 | LNER London→Edinburgh | Done |
| Apr 20–23 | Stockbridge Airbnb | Done |
| Apr 23 | Avis pickup Edinburgh | Done |
| Apr 23–26 | Snowberry Cottages, Onich | Done |
| Apr 26 | CalMac Mallaig→Armadale | Done |
| Apr 26–29 | Skye Airbnb, Staffin | Done |
| Apr 29 | Avis dropoff Edinburgh | Done |
| Apr 29–May 1 | The Raeburn Hotel, Edinburgh | **Currently here** |
| May 1 | LNER Edinburgh→London (09:00–13:10) | Done |
| May 1–4 | The Cumberland, London | Upcoming |
| May 4 | Eurostar London→Brussels + NS to Rotterdam | Upcoming |
| May 5–12 | B&B Bepper, Leiden | Upcoming |
| May 12 | KL0681 AMS→YVR | Upcoming |

## Common edits I'll ask for

- **Add a booking** — new segment with `details`, get the data from Gmail or a forwarded confirmation
- **Add explore content** — new `explore` array category for a stay segment, or new items in an existing category
- **Update an alert** — append, remove, or modify entries in `alerts`
- **Fix typos / reword copy** — straightforward string edits

For new bookings, the structured data comes from my `agentic-email` MCP server (parses PDFs, decodes QR/Aztec barcodes, returns structured JSON). It's not always available — if it's not connected in your session, ask me to paste the booking details.

## Things to flag, not just do

- Schema changes (adding new fields to segments)
- Design system changes (colors, fonts, layout)
- Removing existing content (vs. adding new)
- Anything that touches more than ~20 lines

For everything else, just edit, validate, commit, push.
