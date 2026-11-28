"""Generates every page of southby.app from one template so headers and footers stay identical."""
import os
import feature_icons

# The repository root (this script lives in _build/). Run: python3 _build/build_site.py
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = 16  # bump whenever style.css or icons change, so browsers fetch the new files
TAGLINE = "Made in Swindon, fuelled by tea · © 2026 Michael Southby"
ICON_CREDIT = 'Feature icons based on <a href="https://lucide.dev">Lucide</a> (ISC licence). '

APPLE_TM = ("Apple, Apple Watch, iPad, iPhone and Siri are trademarks of Apple Inc., registered in the U.S. and other "
            "countries and regions. App Store is a service mark of Apple Inc.")


def page(path, title, description, body, extra_footer="", app=None):
    # Small tab icon: plain "s" for the studio, or the app's own icon on its page.
    # Large Home Screen / bookmark icon: "s." for the studio, or the app's icon.
    if app:
        icons = (f'<link rel="icon" href="/assets/icons/{app}.svg?v={VERSION}" type="image/svg+xml">\n'
                 f'  <link rel="apple-touch-icon" href="/assets/icons/{app}-touch.png?v={VERSION}">')
    else:
        icons = (f'<link rel="icon" href="/assets/favicon.svg?v={VERSION}" type="image/svg+xml">\n'
                 f'  <link rel="icon" href="/assets/favicon-32.png?v={VERSION}" type="image/png" sizes="32x32">\n'
                 f'  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v={VERSION}">')
    html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="color-scheme" content="light dark">
  <link rel="stylesheet" href="/assets/style.css?v={VERSION}">
  {icons}
  <meta name="apple-mobile-web-app-title" content="southby.app">
</head>
<body>
  <header class="nav">
    <div class="wrap">
      <a class="brand" href="/">southby<span>.app</span></a>
      <ul>
        <li><a href="/afon/">Afon</a></li>
        <li><a href="/concourse/">Concourse</a></li>
        <li><a href="/settee/">Settee</a></li>
        <li><a href="/lineside/">Lineside</a></li>
        <li class="soon"><a href="/kerbside/">Kerbside</a></li>
        <li class="soon"><a href="/interchange/">Interchange</a></li>
        <li class="soon"><a href="/glovebox/">Glovebox</a></li>
        <li><a href="/support/">Support</a></li>
      </ul>
    </div>
  </header>

{body}

  <footer>
    <div class="wrap">
      <span class="tagline"><span>Made in Swindon, fuelled by tea</span><span class="sep"> · </span><span>© 2026 Michael Southby</span></span>
      <nav>
        <a href="/about/">About</a>
        <a href="/support/">Support</a>
        <a href="/privacy/">Privacy</a>
      </nav>
      <p class="legal">{extra_footer}{ICON_CREDIT}{APPLE_TM}</p>
    </div>
  </footer>
</body>
</html>
"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)


# Where each app is: fill these in as builds go out. Empty means "Coming soon".
#   store:          version live on the App Store, e.g. "1.0.12" (and store_url, its App Store link)
#   testflight:     version in TestFlight, e.g. "2.0.1" (and testflight_url, the public link if there is
#                   one; without it, "Request access" emails support)
RELEASES = {
    "afon":      {"store": None, "store_url": None, "testflight": "1.8.5", "testflight_url": None},
    "concourse": {"store": None, "store_url": None, "testflight": "1.1.2", "testflight_url": None},
    "settee":    {"store": None, "store_url": None, "testflight": "1.2.2", "testflight_url": None},
    "lineside":  {"store": None, "store_url": None, "testflight": "1.1.1", "testflight_url": None},
    "kerbside":  {"store": None, "store_url": None, "testflight": None, "testflight_url": None},
    "interchange": {"store": None, "store_url": None, "testflight": None, "testflight_url": None},
    "glovebox":  {"store": None, "store_url": None, "testflight": None, "testflight_url": None},
}

APP_NAMES = {"afon": "Afon", "concourse": "Concourse", "settee": "Settee", "lineside": "Lineside", "kerbside": "Kerbside", "interchange": "Interchange", "glovebox": "Glovebox"}


def release_badge(app):
    """The pill on the home page's app cards."""
    r = RELEASES.get(app, {})
    if r.get("store"):
        return "On the App Store"
    if r.get("testflight"):
        return "In TestFlight"
    return "Coming soon"


def release_html(app):
    """Under the app's name on its page: the button, then one line per release, e.g.
         Version 1.0.12 on the App Store
         Version 2.0.1 in TestFlight · Request access"""
    r = RELEASES.get(app, {})
    store, beta = r.get("store"), r.get("testflight")
    if not store and not beta:
        return '<span class="btn disabled">Coming soon</span>'
    name = APP_NAMES.get(app, app)
    beta_link = r.get("testflight_url") or f"mailto:support@southby.app?subject={name}%20TestFlight%20access"
    beta_action = "Join the beta" if r.get("testflight_url") else "Request access"
    lines = []
    if store:
        button = f'<a class="btn" href="{r.get("store_url") or "#"}">Download on the App Store</a>'
        lines.append(f"Version {store} on the App Store")
    else:
        button = f'<a class="btn" href="{beta_link}">{beta_action}</a>'
    if beta:
        tail = f' · <a href="{beta_link}">{beta_action}</a>' if store else ""
        lines.append(f"Version {beta} in TestFlight{tail}")
    status = "".join(f"<span>{line}</span>" for line in lines)
    return f'{button}\n      <p class="release">{status}</p>'


def icon(app, size=""):
    cls = "icon lg" if size == "lg" else "icon"
    px = 120 if size == "lg" else 72
    return (f'<span class="{cls}" aria-hidden="true">'
            f'<img src="/assets/icons/{app}.svg?v={VERSION}" alt="" width="{px}" height="{px}"></span>')


_icon_ids = [0]


def feature(icon_name, heading, text, app="studio"):
    """A feature with its icon, drawn like the app icons (see feature_icons.py)."""
    _icon_ids[0] += 1
    art = feature_icons.svg(icon_name, app, f"fi{_icon_ids[0]}")
    return f"""          <div class="feature">
            <div class="glyph">{art}</div>
            <h3>{heading}</h3>
            <p>{text}</p>
          </div>"""


def app_card(app, name, blurb):
    return f"""          <a class="card app" href="/{app}/">
            <div class="card-head">
              {icon(app)}
              <span class="badge">{release_badge(app)}</span>
            </div>
            <div>
              <h3>{name}</h3>
              <p>{blurb}</p>
            </div>
          </a>"""


def steps_html(steps):
    items = "\n".join(
        f"""          <li class="step"><span class="num">{i}</span><div><h3>{h}</h3><p>{t}</p></div></li>"""
        for i, (h, t) in enumerate(steps, 1))
    return f"""    <section>
      <div class="wrap">
        <h2>How it works.</h2>
        <ol class="steps">
{items}
        </ol>
      </div>
    </section>
"""


def audience_html(heading, people):
    chips = "".join(f'<li>{p}</li>' for p in people)
    return f"""    <section class="alt">
      <div class="wrap">
        <h2>{heading}</h2>
        <ul class="chips">{chips}</ul>
      </div>
    </section>
"""


def roadmap_html(now, nxt, later, now_title="Now · release 1",
                 lead="Release 1 does a few things well. Here's where it goes after that."):
    """Items can be plain text, or (text, tag) where tag is e.g. "Afon+" to mark a paid feature."""
    def item(i):
        if isinstance(i, tuple):
            text, tag = i
            return f'<li>{text} <span class="plus">{tag}</span></li>'
        return f"<li>{i}</li>"
    def col(title, label, items):
        lis = "".join(item(i) for i in items)
        return f"""          <div class="card road"><span class="road-label {label}">{title}</span><ul>{lis}</ul></div>"""
    return f"""    <section>
      <div class="wrap">
        <h2>What's next.</h2>
        <p class="lead">{lead}</p>
        <div class="grid three">
{col(now_title, "now", now)}
{col("Next", "next", nxt)}
{col("Later", "later", later)}
        </div>
        <p class="small">Plans can change. Features arrive when they're ready, not before.</p>
      </div>
    </section>
"""


def pricing_html():
    return """    <section>
      <div class="wrap">
        <h2>Free, with Afon+ if you want more.</h2>
        <p class="lead">Everything to do with safety is free and always will be: flood warnings, river levels, the map and the charts.</p>
        <div class="grid two">
          <div class="card">
            <h3>Afon</h3>
            <p class="small">Free</p>
            <ul>
              <li>Every river gauge in England and Wales</li>
              <li>Flood warnings, with notifications</li>
              <li>24-hour and 7-day charts</li>
              <li>Rain forecast</li>
              <li>Two saved rivers</li>
            </ul>
          </div>
          <div class="card">
            <h3>Afon+ <span class="plus">Coming soon</span></h3>
            <p class="small">Monthly or yearly subscription. Shared with your family.</p>
            <ul>
              <li>Alerts when your river passes a level you choose, or rises fast</li>
              <li>Alerts for more places</li>
              <li>Unlimited saved rivers</li>
              <li>21-day history and detailed rain charts</li>
              <li>Home Screen and Lock Screen widgets</li>
              <li>Compare rivers on one chart</li>
              <li>Conditions for swimmers and paddlers</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
"""


def shots_html(labels):
    """Phone-shaped placeholders until real screenshots are ready."""
    frames = "\n".join(
        f'          <figure class="shot"><div class="frame"><span>Screenshot<br>coming soon</span></div><figcaption>{l}</figcaption></figure>'
        for l in labels)
    return f"""    <section>
      <div class="wrap">
        <h2>A closer look.</h2>
        <div class="shots">
{frames}
        </div>
      </div>
    </section>
"""


def app_page(app, name, tagline, lead_heading, lead, features, private_text, callout, extra="", shots=()):
    feats = "\n".join(feature(*f, app=app) for f in features)
    return f"""  <main>
    <div class="wrap hero">
      {icon(app, "lg")}
      <h1>{name}</h1>
      <p>{tagline}</p>
      {release_html(app)}
    </div>

    <section class="alt">
      <div class="wrap">
        <h2>{lead_heading}</h2>
        <p class="lead">{lead}</p>
        <div class="features">
{feats}
        </div>
      </div>
    </section>

{shots_html(shots) if shots else ""}
{extra}
    <section class="alt">
      <div class="wrap">
        <h2>Private by design.</h2>
        <p class="lead">{private_text} <a href="/privacy/">Read the privacy policy</a>.</p>
        <div class="callout">
          <p>{callout}</p>
        </div>
      </div>
    </section>
  </main>"""


# ---------------------------------------------------------------- Home
home_body = f"""  <main>
    <div class="wrap hero">
      <h1>Apps that feel at home<br class="wide"> on your iPhone.</h1>
      <p>Simple, private, Apple-native apps for iPhone, made by one person in Swindon.</p>
    </div>

    <section class="alt" id="apps">
      <div class="wrap">
        <h2>Apps</h2>
        <p class="lead">Small apps, made carefully.</p>
        <div class="grid apps">
{app_card("afon", "Afon", "River levels and flood warnings for the places you care about, explained in plain English.")}
{app_card("concourse", "Concourse", "Live UK train times, beautifully simple. Departures, arrivals and your regular journeys at a glance.")}
{app_card("settee", "Settee", "A beautiful remote for Kodi. Browse your library, pick up where you left off and control playback, all from the sofa.")}
{app_card("lineside", "Lineside", "Railtours, light engines and railway specials, live. Know what's running today and when it's coming past.")}
{app_card("kerbside", "Kerbside", "Bus times with where your bus really is. Starting in Swindon, then the rest of England.")}
{app_card("interchange", "Interchange", "London's Tube, trains and buses, live, with step-free first. Concourse's companion for London.")}
{app_card("glovebox", "Glovebox", "MOT, tax and recalls for your vehicles, with reminders before anything runs out.")}
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="features">
{feature("phone", "Apple-native", "Designed to look and behave like it belongs on your iPhone, built with Apple's own controls, in light and dark mode.")}
{feature("lock", "Private by design", "No accounts, no ads, no tracking. Your data stays on your device.")}
{feature("mail", "A real person", "southby.app is a small, independent studio. Email support and you'll hear back from me, the person who built the app.")}
        </div>
        <p class="more"><a href="/about/">More about southby.app →</a></p>
      </div>
    </section>
  </main>"""
page("index.html", "southby.app — Apple-native apps, made in Swindon",
     "Simple, private, Apple-native apps for iPhone, made by one person in Swindon.", home_body)

# ---------------------------------------------------------------- Afon (agreed release 1)
afon_body = app_page(
    "afon", "Afon",
    "River levels and flood warnings for the places you care about, explained in plain English.",
    "Know what your river is doing.",
    "Live data from the Environment Agency and Natural Resources Wales, presented the way it should be.",
    [
        ("warning", "Flood warnings", "Current flood alerts and warnings near you and at your saved places, ordered by severity."),
        ("bell", "Flood warning notifications", "A notification when the Environment Agency or Natural Resources Wales issues, changes or lifts a warning near your places. Free, always."),
        ("levels", "River levels", "Readings from monitoring stations across England and Wales, with a simple chart of the last few days."),
        ("plain", "Plain English", "No jargon. Afon tells you whether a river is low, normal, high or rising, and what that means."),
        ("map", "Map", "A full-screen map of gauges and warning areas, with each warning's outline, centred on where you are."),
        ("full", "How full", "See at a glance how high a river is compared with its usual range, not just a number in metres."),
        ("saved", "Saved places", "Keep the rivers you care about one tap away: home, the allotment, the fishing spot."),
        ("rain", "Rain forecast", "How much rain is on the way near you over the next 24 hours, hour by hour, from Apple Weather."),
        ("along", "Along the river", "See the other gauges on the same river, so you know what's coming downstream."),
        ("gaps", "Honest about gaps", "If a gauge stops reporting, Afon says so, with the time of its last reading."),
        ("widget", "Widgets with Afon+", "Your saved rivers at a glance on the Home Screen and Lock Screen, without opening the app."),
    ],
    "Afon has no account, no ads and no tracking. Your location and saved places stay on your device. Flood warning notifications only need the codes of the warning areas near your places, never where you are.",
    "<strong>Afon is not an official warning service.</strong> Always follow official advice. Check "
    '<a href="https://check-for-flooding.service.gov.uk/">GOV.UK Check for flooding</a>, '
    '<a href="https://flood-warning.naturalresources.wales/">Natural Resources Wales flood warnings</a> or call Floodline on '
    "0345 988 1188. If life is at risk, call 999.",
    extra=steps_html([
        ("Save the places you care about", "Home, the allotment, the fishing spot, the bridge you cycle over. Or just let Afon find what's near you."),
        ("Afon checks the official data", "River levels and flood warnings come straight from the Environment Agency and Natural Resources Wales, which update most stations every 15 minutes."),
        ("You get the answer, not the numbers", "Is it low, normal, high or rising? Afon says so in plain English, with the readings there if you want them."),
    ]) + audience_html("Made for people who live and play by water.", [
        "Homeowners near rivers", "Anglers", "Kayakers and paddleboarders", "Walkers and dog walkers",
        "Allotment holders", "Farmers", "Wild swimmers", "Anyone who's ever wondered 'is it up?'"]) + roadmap_html(
        ["Flood warnings near you, with notifications", "River levels with 24-hour and 7-day charts", "Plain-English summaries",
         "Full-screen map with warning outlines", "How full each river is", "Rain forecast", "Other gauges on the same river",
         "Two saved rivers"],
        ["Wales", "5-day flood risk outlook", "How today compares with the river's history",
         ("Alerts when your river passes a level you choose", "Afon+"), ("Alerts when a river is rising fast", "Afon+"),
         ("Alerts for more places", "Afon+"), ("Unlimited saved rivers", "Afon+"),
         ("21-day history and detailed rain charts", "Afon+"), ("Home Screen and Lock Screen widgets", "Afon+"),
         ("Compare rivers on one chart", "Afon+"), ("Conditions for swimmers and paddlers", "Afon+"),
         "Siri and Shortcuts", ("Storm overflows and water quality, if the data proves reliable", "Afon+")],
        ["Live Activities while a river is rising", "Apple Watch", "Tides", "Rain gauges", "Rivers beyond the UK, starting with the USA"],
        now_title="1.0 · at launch",
        lead="Afon 1.0 is free and does the important things well. Here's where it goes next.") + pricing_html(),
    shots=["Your rivers", "River detail", "Map", "Flood warning"]
)
page("afon/index.html", "Afon — River levels and flood warnings",
     "Afon shows river levels and flood warnings for the places you care about, explained in plain English. For iPhone and iPad.",
     afon_body, "Contains public sector information licensed under the Open Government Licence v3.0. Rain forecasts from Apple Weather. ",
     app="afon")

# ---------------------------------------------------------------- Concourse (agreed release 1)
concourse_body = app_page(
    "concourse", "Concourse",
    "Live UK train times, beautifully simple.",
    "Every train, at a glance.",
    "Live information for every National Rail station, without the clutter.",
    [
        ("board", "Live departures and arrivals", "Real-time boards for every National Rail station, with platforms and expected times."),
        ("near", "Your nearest station, live", "Open the app and the next trains from the station nearest you are already there."),
        ("destination", "Where are you going?", "Pick a destination and see only the trains that get you there."),
        ("saved", "Stations and journeys", "Save your stations and regular journeys, so the trains you care about come first."),
        ("stops", "Every stop, explained", "Live times, platforms, where the train is now, whether it's catching up, and where it divides."),
        ("info", "Station information", "Facilities, step-free access and help points for every station, one tap away."),
        ("track", "Track your train", "Follow your train on the Lock Screen and in the Dynamic Island, with an alert if the platform changes or it's cancelled."),
        ("bell", "Follow someone's train", "Choose a train today or later this week, perhaps one family are catching, and get a notification for its platform, delays, and when it leaves and arrives."),
        ("stop", "Meet someone off a train", "Notifications for its platform where you're waiting, any delay, and when it gets in."),
        ("mail", "Share your train", "Send a link that opens Concourse ready to follow your train, so family don't have to find it."),
        ("repay", "Delay Repay, made easy", "When your train is late enough to claim, Concourse says so. With Concourse+, it shows what you can claim and has your journey details ready for the form."),
        ("earlier", "Earlier trains", "Trains from the last hour too, so you can check whether someone's train left on time."),
        ("search", "Search", "Find any station by name or code, with your recent and nearby stations ready."),
    ],
    "Concourse has no account, no ads and no tracking. Your location and favourites stay on your device.",
    "Concourse is an independent app and isn't affiliated with National Rail or any train operator. "
    "Always check station information before you travel.",
    extra=steps_html([
        ("Pick your stations", "Nearby stations appear automatically, worked out on your iPhone. Save the ones you use and your regular journeys."),
        ("Live from the rail network", "Times, platforms and disruption come from National Rail's live data, refreshed every 30 seconds or so."),
        ("Tap any train for the full story", "Every stop, live expected times, how many coaches, and the reason for any delay or cancellation."),
    ]) + audience_html("Made for anyone who takes the train.", [
        "Daily commuters", "Weekly office-goers", "Day-trippers", "Students heading home",
        "People meeting someone off a train", "Anyone tired of cluttered rail apps"]) + roadmap_html(
        ["Live departures and arrivals", "Your nearest station, live", "Where are you going?", "Saved stations and two saved journeys",
         "Every stop, with dividing trains", "Station information", "Earlier trains", "Search",
         "Track your train on the Lock Screen", "A Delay Repay hint when your train is late enough to claim",
         "Follow a train today or later this week", "Meet someone off a train", "Share your train with family",
         "Severe disruption in red, from National Rail's own severity",
         ("Help claiming Delay Repay", "Concourse+"), ("Follow several trains at once", "Concourse+")],
        ["Home Screen widgets and Siri", "Each operator's service status at a glance",
         "Step-free and accessibility details for each train: wheelchair spaces, accessible toilet, bike spaces",
         ("Engineering works alerts for your journeys", "Concourse+"),
         ("Alerts when an incident affects a train you follow", "Concourse+"),
         ("Unlimited saved journeys", "Concourse+"), ("Know your train: coaches, formation and unit numbers", "Concourse+")],
        ["Journey planning with changes", "Apple Watch"],
        now_title="1.0 · at launch",
        lead="Concourse 1.0 is free. Concourse+ will add extras for regular travellers."),
    shots=["Trains", "Departures", "Your train", "Station information"]
)
page("concourse/index.html", "Concourse — Live UK train times",
     "Concourse shows live UK train times for every National Rail station, beautifully simple. For iPhone.",
     concourse_body, "Concourse is not affiliated with National Rail or any train operator. ", app="concourse")

# ---------------------------------------------------------------- Settee (agreed release 1)
settee_body = app_page(
    "settee", "Settee",
    "A beautiful remote for Kodi.",
    "The remote Kodi deserves.",
    "Everything you need to run Kodi from the sofa, designed for iPhone.",
    [
        ("finds", "Finds Kodi for you", "Settee spots Kodi on your home network automatically. No IP addresses to type, nothing extra to install."),
        ("touch", "Touch remote", "Swipe and tap, or switch to an Apple-style direction pad, with play, pause, seek and volume always to hand."),
        ("type", "Type from your phone", "Search boxes and logins on the TV, typed with your iPhone's keyboard."),
        ("play", "Now playing", "Artwork, progress, a smooth scrubber and volume for whatever's on."),
        ("library", "Your library", "Browse your films, TV shows and music, search across all of it, and tap to play."),
        ("resume", "Pick up where you left off", "Continue Watching and Up Next, with Resume or Start Over on anything you've started."),
        ("watched", "Watched and unwatched", "Mark things watched, even if you saw them somewhere else."),
        ("tidy", "Keep the library tidy", "Update or clean Kodi's library from your phone, with a quiet note when it's done."),
    ],
    "Settee talks only to Kodi on your own network. Nothing is sent to me, and there's no account, no ads and no tracking.",
    "Settee is an independent app and isn't affiliated with or endorsed by the Kodi project or the XBMC Foundation. "
    "Kodi® is a registered trademark of the XBMC Foundation.",
    extra=steps_html([
        ("Turn on remote control in Kodi", "One switch in Kodi's settings: Services, then Control, then allow remote control over HTTP."),
        ("Open Settee on the same Wi-Fi", "It finds Kodi by itself. No IP addresses, no port numbers, no fiddling."),
        ("Sit back", "Browse your library, carry on with what you were watching, and control it all from your phone."),
    ]) + audience_html("Made for Kodi households.", [
        "Kodi on Apple TV or a media PC", "Home cinema setups", "Families sharing one library",
        "Anyone who's lost the remote down the sofa"]) + roadmap_html(
        ["Automatic Kodi discovery", "Touch remote and direction pad", "Keyboard input", "Now playing with artwork",
         "Films, TV and music, with search", "Continue Watching and Up Next", "Resume or Start Over", "Library update and clean"],
        ["Wake your Kodi box from your phone", "Volume with your iPhone's buttons", "Sleep timer", "Play queue"],
        ["Live Activities and the Dynamic Island", "Control Centre and Home Screen widgets", "Siri and Shortcuts", "Apple Watch remote"],
        now_title="1.0 · at launch",
        lead="Settee 1.0 covers everything you do from the sofa. Here's where it goes next."),
    shots=["Remote", "Now Playing", "Library", "Continue Watching"]
)
page("settee/index.html", "Settee — A beautiful remote for Kodi",
     "Settee is a beautiful, Apple-native remote for Kodi on iPhone.",
     settee_body, "Kodi® is a registered trademark of the XBMC Foundation. Settee is not affiliated with or endorsed by the Kodi project. ",
     app="settee")

# ---------------------------------------------------------------- Lineside (in development)
lineside_body = app_page(
    "lineside", "Lineside",
    "Railtours and railway specials, live.",
    "Know what's coming down the line.",
    "The trains you won't find on a departure board, from Network Rail's own timetable and live running.",
    [
        ("today", "Today's specials", "Railtours, empty coaches, light engines, test trains and freight specials running today, in time order."),
        ("choose", "Choose your trains", "Railtours, empty coaches and light engines, test trains, freight specials and booked freight. All on to start; turn off what you don't need in Settings."),
        ("live", "Live running", "Once a train is on its way, see where it was last reported and how early or late it's running."),
        ("near", "Nearest to you", "For each train, the station on its route closest to you, worked out on your iPhone."),
        ("spots", "Spots", "Save the stations you watch from and see everything due past them today."),
        ("bell", "Spot alerts", "A notification before a train passes one of your spots, and when a late-notice special is added."),
        ("light", "Light at your spot", "Front lit, side lit or into the sun, from the direction of the track and the sun at the planned time, with Apple Weather's forecast."),
        ("track", "Follow Live", "Follow a train on your Lock Screen, with an alert when it's reported a few minutes before your spot."),
        ("coming", "Coming up", "Everything planned for the next seven days, day by day."),
        ("search", "Search", "Find a train by headcode, place or operator."),
        ("late", "Late-notice trains", "Specials planned at short notice appear as soon as Network Rail publishes them."),
        ("route", "Map of the route", "Each train's route drawn along the real tracks, with a pin where it was last reported."),
        ("honest", "Honest times", "Times exactly as planned and reported, never guessed. If something isn't in the data, Lineside says so."),
    ],
    "Lineside has no account, no ads and no tracking. Your location and spots stay on your device, and the nearest station on each route is worked out there too.",
    "<strong>Stay safe and legal.</strong> Watch from stations, public footpaths and bridges, and never go onto the railway. "
    "Lineside is an independent app and isn't affiliated with Network Rail or any train or charter operator.",
    extra=steps_html([
        ("Choose what you're interested in", "Every type of special to start, plus booked freight near you. Turn off what you don't need."),
        ("Lineside reads Network Rail's data", "The full timetable is checked every night, with late-notice plans and live train movements as they happen."),
        ("Be in the right place", "See which station on the route is nearest you, when the train's due, and whether it's running early or late."),
    ]) + audience_html("Made for people who love trains.", [
        "Railway photographers", "Railtour passengers", "Families waving someone off", "Enthusiasts and spotters",
        "Heritage railway fans", "Anyone who heard a loco go past and wondered what it was"]) + roadmap_html(
        ["Today's specials, live", "Five train types to choose from", "Nearest station on each route", "Spots, with alerts",
         "Light at your spot, with the weather", "Follow a train live on your Lock Screen", "Route maps along the real tracks",
         "Coming up: the next seven days", "Search", "Late-notice trains"],
        ["Map of specials on the move, from real reported positions only",
         "Passing times at spots between stations, from the live staff boards"],
        ["A log of what you've seen", "Home Screen widgets", "Apple Watch",
         "Signal by signal: a special two signals from your spot (on trial first)",
         "Locomotive details, if they're ever published as open data"],
        now_title="1.0 · at launch",
        lead="Lineside 1.0 is free. Here's what it does, and where it goes next."),
    shots=["Today", "Train detail", "Spots", "Coming Up"]
)
page("lineside/index.html", "Lineside — Railtours and railway specials, live",
     "Lineside shows railtours, light engines, test trains and freight specials running today, live, with the nearest station on each route. For iPhone.",
     lineside_body, "Contains information of Network Rail Infrastructure Limited licensed under the Open Government Licence v3.0, through the Rail Data Marketplace. Track shapes © <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors. Lineside is not affiliated with Network Rail or any train or charter operator. ",
     app="lineside")

kerbside_body = app_page(
    "kerbside", "Kerbside",
    "Bus times, done properly.",
    "Know where your bus really is.",
    "Kerbside uses the Bus Open Data Service, the government's open data for local buses in England: timetables, and where each bus actually is. Testing has started in Swindon; the rest of England follows.",
    [
        ("stop", "Stops near you", "The stops around you, nearest first, each with its buses for the next three hours."),
        ("bus", "Where your bus really is", "Its last reported position on the map, and how many stops away it is. Never a guessed countdown."),
        ("favourites", "Favourite stops", "Star the stops you use and see their next buses as soon as you open the app."),
        ("route", "Every line", "Each line's buses running now, and its stops in each direction."),
        ("map", "Live map", "Every bus reporting around you, with stops when you zoom in. Buses silent for 15 minutes are left off."),
        ("search", "Search", "Find a stop by its name or street, or a line by its number."),
        ("honest", "Honest times", "Scheduled times from the timetable, live positions as reported. If a bus isn't reporting, Kerbside says so."),
    ],
    "Kerbside will have no account, no ads and no tracking. Your location and saved stops stay on your device.",
    "<strong>Coming soon.</strong> Kerbside is being tested in Swindon now. Email <a href=\"mailto:support@southby.app?subject=Kerbside\">support@southby.app</a> if you'd like to hear when it's ready to try.",
    extra=roadmap_html(
        ["Stops near you, with the next three hours", "Where each bus is, in stops away", "Favourite stops",
         "Every line, with its buses now", "Live map", "Search", "Swindon and the places its buses reach"],
        ["The rest of England", "How late a bus is, measured at the stop it last passed", "London times from TfL"],
        ["Home Screen widgets", "Apple Watch"],
        now_title="1.0 · at launch",
        lead="Kerbside 1.0 starts small and honest. Here's where it goes next."),
)
page("kerbside/index.html", "Kerbside — Bus times, done properly",
     "Kerbside: bus times with where your bus really is. Testing in Swindon now, coming soon from southby.app.",
     kerbside_body, "Will contain public sector information from the Bus Open Data Service, licensed under the Open Government Licence v3.0. ",
     app="kerbside")

# ---------------------------------------------------------------- Interchange (in development)
interchange_body = app_page(
    "interchange", "Interchange",
    "London, live, with step-free first.",
    "Get around London, step-free if you need it.",
    "Interchange uses Transport for London's own open data: live trains and buses, line status in TfL's words, and every lift and platform as TfL records them. It's Concourse's companion for London.",
    [
        ("near", "Nearby", "The station nearest you with its next trains, then the stations and bus stops around you."),
        ("tube", "Live trains", "TfL's own predictions at every station, by line and direction."),
        ("stepfree", "Step-free first", "Lifts, and how you board at each platform: level access, ramps, and the step and gap where TfL has measured them. Turn on Step-free First to see them before the trains."),
        ("warning", "Lifts out", "Every lift out of service across the network, in TfL's own words."),
        ("bus", "Buses instead", "When a lift is out, the bus stops near the station and their next buses, as a step-free way on."),
        ("live", "Every line", "Each line's status in TfL's own words, and its stops, with lifts that are out marked."),
        ("stop", "London buses", "Every bus stop, with its next buses, and where each bus goes next."),
        ("bell", "Alerts", "When one of your lines starts or stops having problems, and when a lift at one of your saved stations goes out or comes back."),
        ("search", "Search", "Find a station, a line, a bus stop, or a place and the stations nearest it."),
        ("route", "Works with Concourse", "At stations with National Rail trains, open Concourse for the departures."),
        ("honest", "Honest information", "Shown exactly as TfL publishes it. Where TfL hasn't recorded something, Interchange doesn't guess."),
    ],
    "Interchange will have no account, no ads and no tracking. The stations and stops near you are worked out on your iPhone, so your location never leaves it.",
    "<strong>Coming soon.</strong> Interchange is being built now. Email <a href=\"mailto:support@southby.app?subject=Interchange\">support@southby.app</a> if you'd like to hear when it's ready to try. "
    "Interchange is an independent app and isn't affiliated with Transport for London.",
    extra=audience_html("Made for getting around London.", [
        "Wheelchair users", "Parents with buggies", "Anyone with heavy luggage", "Commuters",
        "Visitors to London", "Concourse users heading into London"]),
)
page("interchange/index.html", "Interchange — London, live, with step-free first",
     "Interchange: London's Tube, trains and buses, live, with step-free information first. Coming soon from southby.app.",
     interchange_body, "Powered by TfL Open Data. Contains OS data © Crown copyright and database rights. Interchange is not affiliated with Transport for London. ",
     app="interchange")

# ---------------------------------------------------------------- Glovebox (in development)
glovebox_body = app_page(
    "glovebox", "Glovebox",
    "MOT, tax and recalls for your vehicles.",
    "Never miss an MOT or tax date.",
    "Glovebox uses the official records for vehicles in Great Britain: MOT history and safety recalls from the DVSA, and vehicle tax from the DVLA. Add your car, van or motorbike by its registration and everything you need is in one place.",
    [
        ("car", "Your garage", "Each vehicle with its number plate, MOT and tax at a glance, and the days left on each."),
        ("dates", "MOT and tax dates", "When the MOT and tax run out, with the MOT shown as a gauge running down over its year."),
        ("bell", "Reminders", "A month, two weeks and a day before the MOT or tax is due, worked out on your iPhone."),
        ("history", "MOT history", "Every MOT with its result, mileage and advisories, with the tester's notes in plainer English."),
        ("full", "Mileage", "The mileage at each MOT on a chart, with a clear flag if it ever went down."),
        ("warning", "Recalls", "Any open safety recall the DVSA has for the vehicle, so you know if it needs fixing."),
        ("saved", "Your own dates", "Insurance, servicing and anything else, each with its own reminders. Add any date to Calendar."),
        ("share", "Share its history", "A one-page PDF of the vehicle's MOT history, ready to share when you sell."),
        ("search", "Look up any vehicle", "Enter any registration to see its MOT, tax and recalls."),
        ("buying", "Buying Check", "With Glovebox+, the things a buyer would want to know about a vehicle you look up, straight from the DVSA and DVLA. Nothing guessed or scored."),
        ("advisory", "Watch out for", "With Glovebox+, advisories that keep coming back MOT after MOT."),
        ("honest", "Honest information", "Exactly what the DVSA and DVLA record. If something isn't in their records, Glovebox says so."),
    ],
    "Glovebox has no account, no ads and no tracking. Your vehicles and dates stay on your iPhone, and only a registration is ever sent, to look it up.",
    "<strong>Coming soon.</strong> Glovebox is being tested now. Two vehicles are free; Glovebox+ adds as many as you like, Buying Check, Watch Out For and your choice of reminder times. "
    "Email <a href=\"mailto:support@southby.app?subject=Glovebox\">support@southby.app</a> if you'd like to hear when it's ready to try. "
    "Glovebox is an independent app and isn't affiliated with the DVSA or DVLA.",
)
page("glovebox/index.html", "Glovebox — MOT, tax and recalls for your vehicles",
     "Glovebox: MOT, tax and recalls for your cars, vans and motorbikes, with reminders before anything runs out. Coming soon from southby.app.",
     glovebox_body, "Contains public sector information from the DVSA and DVLA, licensed under the Open Government Licence v3.0. Glovebox is not affiliated with the DVSA or DVLA. ",
     app="glovebox")

# ---------------------------------------------------------------- About
about_body = """  <main class="wrap">
    <article class="prose">
      <h1>About southby.app</h1>
      <p class="updated">Small apps, made properly.</p>

      <p class="intro">southby.app is a small, independent app studio in Swindon, run by me, Michael. I make Apple-native apps for everyday life in Britain: rivers, trains, railtours and the telly. Every one follows the same six principles.</p>

      <ol class="principle-list">
        <li>
          <h2>Apple-native</h2>
          <p>Built with Apple's own tools and design language, so each app feels familiar from the first tap. Widgets, dark mode, Dynamic Type and VoiceOver aren't extras; they're part of the job.</p>
        </li>
        <li>
          <h2>Private by design</h2>
          <p>No accounts, no adverts, no tracking, no analytics. If an app needs your location, it's used on your device and never sent to me. The <a href="/privacy/">privacy policy</a> is short because there's very little to say.</p>
        </li>
        <li>
          <h2>Open data, honestly credited</h2>
          <p>Afon, Concourse and Lineside turn public UK data into something genuinely easy to use. They always say where the data comes from, and never pretend to be the official source.</p>
        </li>
        <li>
          <h2>Small and focused</h2>
          <p>Each release does a few things properly rather than many things badly. New features arrive when they're ready, and each app's page shows what's coming next.</p>
        </li>
        <li>
          <h2>Fair pricing</h2>
          <p>No adverts, ever. If an app has paid extras, they'll be optional and clearly priced, and the app will still be useful without them.</p>
        </li>
        <li>
          <h2>A real person behind it</h2>
          <p>Email <a href="mailto:support@southby.app">support@southby.app</a> and you'll hear back from the person who built the app, usually within a couple of working days.</p>
        </li>
      </ol>

      <h2>Who's behind it</h2>
      <p>I've spent my career in IT and make apps in my own time, starting with things I wanted to use myself: <a href="/afon/">Afon</a> for river levels and flood warnings, <a href="/concourse/">Concourse</a> for live train times, <a href="/settee/">Settee</a> for controlling Kodi from the sofa, and <a href="/lineside/">Lineside</a> for railtours and railway specials.</p>
    </article>
  </main>"""
page("about/index.html", "About — southby.app",
     "How southby.app makes apps: Apple-native, private by design, built on open data, small and focused, fairly priced.", about_body)

# ---------------------------------------------------------------- Support
def qa(q, a):
    return f"""      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>"""

support_body = f"""  <main class="wrap">
    <article class="prose">
      <h1>Support</h1>
      <p class="updated">Here to help with Afon, Concourse, Settee, Lineside and Glovebox.</p>

      <div class="callout">
        <p><strong>Email:</strong> <a href="mailto:support@southby.app">support@southby.app</a><br>
        southby.app is just me, so I usually reply within a couple of working days. Please mention which app you're using, your device and your iOS version.</p>
      </div>

      <h2>Afon</h2>
{qa("Where does Afon's data come from?", "River levels and flood warnings come from the Environment Agency's public real-time flood-monitoring service and, in Wales, from Natural Resources Wales. Afon contains public sector information licensed under the Open Government Licence v3.0, including Natural Resources Wales information © Natural Resources Wales and Database Right. Rain forecasts come from Apple Weather. With Afon+, storm overflow data comes from Anglian Water, Northumbrian Water, Severn Trent Water, South West Water, Southern Water, Thames Water, United Utilities, Wessex Water and Yorkshire Water, each licensed under <a href='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</a>; Afon simplifies the statuses and tidies river names. Bathing water quality comes from the Environment Agency.")}
{qa("Is Afon free?", "Yes. Flood warnings, river levels, the map, charts, rain forecasts and two saved rivers are free, and always will be. Afon+, coming soon, is a monthly or yearly subscription for people who want more: alerts at a level you choose, unlimited saved rivers, longer history and widgets. It's shared with your family, and you can cancel at any time.")}
{qa("Is Afon an official flood warning service?", "No. Afon presents official data, but it can be delayed or unavailable. Always follow official advice. Check GOV.UK Check for flooding or Natural Resources Wales's flood warnings, sign up to their free flood warning services, or call Floodline on 0345 988 1188. If life is at risk, call 999.")}
{qa("How do flood warning notifications work?", "When you turn them on, Afon works out on your iPhone which Environment Agency and Natural Resources Wales flood warning areas are near your places, and sends my server only those area codes and an Apple push code for your iPhone. When the Environment Agency or Natural Resources Wales issues, changes or lifts a warning in one of those areas, you get a notification. Your location is never sent. Turn them off at any time in Afon or in iOS Settings.")}
{qa("Which areas does Afon cover?", "England and Wales, using data from the Environment Agency and Natural Resources Wales.")}
{qa("Why is a reading missing or out of date?", "Monitoring stations sometimes go offline for maintenance or report late. Afon shows the time of each station's last reading, marks it as delayed after 6 hours and offline after 7 days, and greys it out on the map. These are problems at the station, not with Afon, and the agency that runs it is usually already fixing them.")}
{qa("Why does Afon ask for my location?", "So it can show the stations and warnings nearest to you. Your location is only used on your device and is never sent to me: Afon only ever asks my server about specific gauges. You can say no and choose a home place in Settings instead.")}

      <h2>Concourse</h2>
{qa("Where does Concourse's information come from?", "Live train times come from National Rail's real-time data services, the same source used by station departure boards.")}
{qa("Why is a train showing differently from the station board?", "Information can change quickly during disruption. Concourse refreshes regularly, but if in doubt, follow the station's own boards and announcements.")}
{qa("Why does Concourse ask for my location?", "To show your nearest stations. Your location is only used on your device and is never sent to me. You can say no and search for stations instead.")}
{qa("Can I buy tickets in Concourse?", "No. Concourse is for live times and journeys, not tickets.")}
{qa("Can I see trains that have already left?", "Yes. Open Earlier trains at the top of a station's board or journey to see the last hour, including when each train actually left.")}
{qa("Where do station facilities come from?", "From National Rail's station information. Tap ⓘ on any station's board to see facilities, step-free access and help points. If something looks wrong, check with the station before you travel.")}

      <h2>Settee</h2>
{qa("How do I connect Settee to Kodi?", "In Kodi, go to Settings → Services → Control and turn on 'Allow remote control via HTTP'. Make sure your iPhone and Kodi are on the same Wi-Fi, then open Settee and it should find Kodi automatically.")}
{qa("Why does Settee ask for local network access?", "iOS asks before any app talks to devices on your home network. Settee needs this to find and control Kodi. It doesn't talk to anything else.")}
{qa("Settee can't find my Kodi. What can I try?", "Check that remote control via HTTP is enabled in Kodi, that both devices are on the same network, and that local network access is allowed for Settee in Settings → Privacy &amp; Security → Local Network. You can also add Kodi manually by its address.")}
{qa("Is Settee made by the Kodi team?", "No. Settee is an independent app and isn't affiliated with or endorsed by the Kodi project or the XBMC Foundation. Kodi® is a registered trademark of the XBMC Foundation.")}

      <h2>Lineside</h2>
{qa("Where does Lineside's information come from?", "From Network Rail's open data, through the Rail Data Marketplace: the published timetable, plans added at short notice, and live train movements. It's the same information the railway runs on, but specials can still change or be cancelled at short notice.")}
{qa("Why can't I see which locomotive is on a train?", "It isn't published in Network Rail's open data. The timetable says a train is loco-hauled, but not which locomotive, or whether it's steam or diesel. Lineside won't guess.")}
{qa("Why isn't a train I know about showing?", "Check the train types you've chosen: test trains and freight specials are off to start with. Some specials are only planned a day or two ahead, and a few are never published in open data.")}
{qa("How does Lineside know which station is nearest me?", "Your iPhone works it out from each train's route. Your location is never sent to me. You can say no to location and still see every train.")}
{qa("Where can I watch from?", "Stations, public footpaths and bridges. Never go onto the railway or trespass on railway land, and follow any instructions from railway staff.")}

      <h2>Glovebox</h2>
{qa("Where does Glovebox's information come from?", "MOT history and safety recalls come from the DVSA (Driver and Vehicle Standards Agency), and tax from the DVLA (Driver and Vehicle Licensing Agency). Glovebox contains public sector information licensed under the Open Government Licence v3.0. It isn't affiliated with either agency.")}
{qa("Which vehicles does Glovebox cover?", "Vehicles registered in Great Britain (England, Scotland and Wales). Vehicles registered in Northern Ireland have their MOT records kept separately, so Glovebox can't show them.")}
{qa("Is Glovebox free?", "Yes, for two vehicles, with their MOT, tax, recalls, history and reminders. Glovebox+, a monthly or yearly subscription, adds as many vehicles as you like, Buying Check for any vehicle you look up, Watch Out For, and your choice of when reminders arrive.")}
{qa("Why is a date or detail missing?", "Glovebox shows exactly what the DVSA and DVLA hold. New vehicles have no MOT until they're three years old, and some older records are incomplete. If something looks wrong, check it on GOV.UK.")}
{qa("Is Glovebox a substitute for checking on GOV.UK?", "No. It shows the official records, but they can be delayed. If it matters, for example before you drive or buy, check GOV.UK's own MOT and vehicle tax services.")}

      <h2>All apps</h2>
{qa("Do I need an account?", "No. None of my apps have accounts. Your settings and saved items are stored on your device.")}
{qa("How do I request a refund?", 'App Store purchases are handled by Apple. Request a refund at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.')}

      <h2>Privacy</h2>
      <p>For questions about your data, see the <a href="/privacy/">privacy policy</a> or email <a href="mailto:privacy@southby.app">privacy@southby.app</a>.</p>
    </article>
  </main>"""
page("support/index.html", "Support — southby.app",
     "Get help with Afon, Concourse, Settee, Lineside and Glovebox.", support_body)

# ---------------------------------------------------------------- Privacy
privacy_body = """  <main class="wrap">
    <article class="prose">
      <h1>Privacy Policy</h1>
      <p class="updated">Last updated: 28 November 2026</p>

      <div class="callout">
        <p><strong>In short:</strong> My apps don't have accounts, adverts, analytics or tracking. I don't collect, sell or share your personal data. Anything an app needs, such as your location, saved places or Kodi address, stays on your device. The exceptions are notifications you choose to turn on (Afon's flood warnings, Concourse's tracked and followed trains, and Lineside's spot alerts): these need an Apple push code and what the notification is about, never your location. If you follow a train in Concourse you can add a first name for its notifications; it's deleted soon after the train arrives. Glovebox sends my server the registration of a vehicle you add or look up, and nothing else. Otherwise, the only personal data I receive is what you choose to send me by email.</p>
      </div>

      <h2>Who I am</h2>
      <p>Southby is the trading name of Michael Southby, an individual developer based in the United Kingdom. For the purposes of UK data protection law (the UK GDPR and the Data Protection Act 2018), I am the data controller for any personal data described in this policy.</p>
      <p>Contact: <a href="mailto:privacy@southby.app">privacy@southby.app</a></p>

      <h2>This policy covers</h2>
      <ul>
        <li>Afon for iPhone and iPad</li>
        <li>Concourse for iPhone</li>
        <li>Settee for iPhone</li>
        <li>Lineside for iPhone</li>
        <li>Glovebox for iPhone</li>
        <li>Any other app published by southby.app that links to this policy</li>
        <li>This website, southby.app</li>
      </ul>

      <h2>What all my apps have in common</h2>
      <ul>
        <li>No accounts or sign-in.</li>
        <li>No advertising, analytics or third-party tracking code.</li>
        <li>Location, if you allow it, is used on your device only. It is never sent to me or stored by me. You can change this at any time in Settings → Privacy &amp; Security → Location Services.</li>
        <li>Saved items and settings are stored on your device. If you use iCloud backups, they may be included in your backup, which Apple handles under its own privacy policy. I can't access it.</li>
        <li>Notifications are generated on your device, except Afon's flood warning notifications, Concourse's train tracking and Lineside's spot alerts, explained below.</li>
      </ul>

      <h2>Afon</h2>
      <p>Afon gets river levels and flood warnings from the Environment Agency's public flood-monitoring service and Natural Resources Wales, and rain forecasts from Apple's WeatherKit service. To make this fast and reliable, these requests go through a small server I run (api.southby.app), which collects the data and passes it on.</p>
      <p>Your iPhone only ever asks my server for information about specific river gauges, or for the full list of gauges and flood warnings for England and Wales. It never sends your location, your saved rivers or any identifier from Afon. Working out which gauges and warnings are near you happens on your device. When a rain forecast is needed, my server asks Apple about the area around a gauge, not about you. To find the flood warning areas near your places for notifications, your iPhone asks the Environment Agency and, in and near Wales, the Welsh Government's DataMapWales service directly, so that never passes through my server.</p>
      <p>Like any web server, mine sees your device's IP address. I don't link it to you or use it for anything except keeping the service secure and working, and server logs are deleted within 14 days. If my server can't be reached, Afon may contact the Environment Agency's service directly instead, which will also see your IP address; the Environment Agency's own privacy notice applies to its services.</p>
      <p><strong>Flood warning notifications.</strong> If you turn these on, Afon works out on your iPhone which flood warning areas are near your places, then sends my server those area codes and an Apple push code (a "device token") so a notification can reach your iPhone through Apple's push service. Your location and saved places are never sent. The push code doesn't identify you, and I don't link it to anything else. I keep it only to send these notifications; if Afon hasn't been in touch for 60 days it's deleted automatically, and it's removed as soon as you turn notifications off. My lawful basis is your consent, which you can withdraw at any time in Afon or in iOS Settings. Apple delivers the notifications under its own privacy policy.</p>

      <h2>Concourse</h2>
      <p>To show live train times, Concourse requests information about the stations and services you look at from National Rail's data services. These requests may pass through a small server I run, which forwards them and returns the results. The request contains only the station or service you asked about, never your location or any identifier from Concourse. Like any web server, mine sees your device's IP address. I don't link it to you or use it for anything except keeping the service secure and working, and server logs are deleted within 14 days.</p>
      <p><strong>Tracking a train.</strong> If you choose "Track This Train", Concourse shows the train on your Lock Screen and in the Dynamic Island (a Live Activity). To keep it up to date, Concourse sends my server the train's National Rail service code, your two station codes and an Apple push code for that one Live Activity, so updates can reach your iPhone through Apple's push service. Your location is never sent, and the push code doesn't identify you. I keep these only while the train is being tracked: they're deleted when the train arrives, if it's cancelled, when you stop tracking, or after 8 hours at most. Apple delivers the updates under its own privacy policy.</p>
      <p><strong>Following and meeting a train.</strong> If you follow a train (perhaps one someone else is catching) or meet someone off one, Concourse sends my server that train's details (the day, the two station codes, its timetabled times and, once it's running, its National Rail service code), an Apple push code (a "device token") so notifications can reach your iPhone through Apple's push service, and, only if you type one, a first name to use in the notifications. Your location is never sent. I keep these only to send the notifications: they're deleted a couple of hours after the train arrives or is cancelled, when you stop following it, and in any case within a day of the train being due. My lawful basis is your consent, which you can withdraw at any time by stopping following the train or in iOS Settings. Apple delivers the notifications under its own privacy policy.</p>
      <p><strong>Sharing a train.</strong> "Share So Others Can Follow" creates a link containing only the train's details (the day, station codes, timetabled times and, on the day, its service code). It contains no name or location. Opening it shows a page on this website, or opens Concourse if it's installed.

      <h2>Lineside</h2>
      <p>Lineside gets railtours and other specials from a small server I run (api.southby.app), which reads Network Rail's open timetable and live running data. Your iPhone asks it for the trains of the types you've chosen on a given day, the trains past the stations you've saved as spots, and anything you search for. These requests contain only those choices, station codes and search words, never your location or any identifier from Lineside. Working out which station on each route is nearest you happens on your device. If Freight is switched on in Settings, Today also sends the codes of the stations within your chosen "near you" distance, so it can show freight trains near you. That list narrows down roughly where you are, though not your exact position; turn Freight off if you'd rather it wasn't sent. Like any web server, mine sees your device's IP address. I don't link it to you or use it for anything except keeping the service secure and working, and server logs are deleted within 14 days.</p>
      <p><strong>Weather.</strong> Lineside shows Apple Weather's forecast for a station at the time a train is due. To get it, your iPhone sends Apple the position of that station (never your own position) through Apple's WeatherKit service, which handles it under Apple's own privacy policy. Nothing about this comes to me.</p>
      <p><strong>Spot alerts.</strong> If you turn these on, Lineside sends my server your spots' station codes, the train types you've chosen, how much warning you want and an Apple push code (a "device token"), so a notification can reach your iPhone through Apple's push service. Your location is never sent, and the push code doesn't identify you. I keep these only to send the alerts; they're deleted as soon as you turn alerts off, and automatically if Lineside hasn't been in touch for 60 days. My lawful basis is your consent, which you can withdraw at any time in Lineside or in iOS Settings. Apple delivers the notifications under its own privacy policy.</p>

      <h2>Glovebox</h2>
      <p>Glovebox gets MOT history and recalls from the DVSA and vehicle tax from the DVLA through a small server I run (api.southby.app). To look a vehicle up, your iPhone sends my server only its registration: never your location, your other vehicles or any identifier from Glovebox. The registration is sent in the body of the request, so it doesn't appear in web server logs, and my server never logs it. To avoid asking the DVSA and DVLA again for the same vehicle, my server keeps each answer in memory for up to six hours, then forgets it; it's never written to disk. To stop the service being used to work through the DVSA's and DVLA's records, it limits how many new lookups one address can make in an hour, keeping addresses only as a one-way hash, only in memory and only for an hour.</p>
      <p>Your vehicles, your own dates and your reminders are kept on your iPhone. MOT and tax reminders are worked out and scheduled on your device, with no server involved. Adding a date to Calendar uses Apple's own screen, so Glovebox never has access to your calendars. A shared MOT history PDF is made on your iPhone and goes only where you send it.</p>
      <p>Glovebox+ is a subscription handled by Apple through the App Store. Glovebox checks it on your iPhone; nothing about your subscription is sent to me.</p>

      <h2>Settee</h2>
      <p>Settee communicates only with Kodi on your own local network. It needs iOS's Local Network permission to find and control Kodi, and it doesn't contact any other device or service. The address of your Kodi, and any username and password you enter for it, are stored on your device, with the password kept in the iOS Keychain. Nothing about your library, what you watch or your network is sent to me.</p>

      <h2>Information from Apple</h2>
      <p>Apple may provide me with aggregated, anonymous App Store information, such as download numbers. If you have chosen to share analytics with app developers in your device settings, Apple may also share anonymised crash reports and usage statistics. I use these only to fix problems and improve the apps. They do not identify you.</p>

      <h2>When you contact me</h2>
      <p>If you email support@southby.app or privacy@southby.app, I receive your email address, your name if you include it, and whatever you write. I use this only to reply and help with your query. My lawful basis is legitimate interests: responding to people who get in touch. I keep support emails for up to 24 months, then delete them, unless I need them longer to resolve an ongoing issue. Email is delivered through my email provider, which processes it on my behalf.</p>

      <h2>This website</h2>
      <p>southby.app uses no cookies, analytics or tracking. The site is hosted by GitHub Pages, and GitHub may log visitors' IP addresses for security and operational purposes under its own privacy statement.</p>

      <h2>Sharing your data</h2>
      <p>I do not sell, rent or share personal data with anyone, except where required by law.</p>

      <h2>International transfers</h2>
      <p>My service providers (such as my email, website and server hosts) may process data outside the UK. Where they do, appropriate safeguards required by UK data protection law apply.</p>

      <h2>Your rights</h2>
      <p>Under UK data protection law you have the right to ask for a copy of your personal data, and to ask me to correct, delete or restrict it, or to object to how I use it. Since my apps don't collect personal data, this mainly applies to emails you've sent me. To make a request, email <a href="mailto:privacy@southby.app">privacy@southby.app</a>. I'll respond within one month.</p>
      <p>If you're unhappy with how I've handled your data, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk</a>. I'd appreciate the chance to put things right first.</p>

      <h2>Children</h2>
      <p>My apps are suitable for general audiences and do not knowingly collect personal data from anyone, including children.</p>

      <h2>Changes to this policy</h2>
      <p>If an app's data practices change, for example if a future feature needs a server, I'll update this policy before the change goes live and revise the date at the top of this page.</p>
    </article>
  </main>"""
page("privacy/index.html", "Privacy Policy — southby.app",
     "How southby.app's apps, Afon, Concourse, Settee, Lineside and Glovebox, handle your personal data.", privacy_body)

# ---------------------------------------------------------------- Concourse: a shared train
# "Share So Others Can Follow" links (https://southby.app/concourse/follow/?d=…&f=…) open Concourse where
# it's installed (a universal link, see the apple-app-site-association file below) and this page otherwise.
page("concourse/follow/index.html", "Follow a train — Concourse",
     "Someone has shared a train with you. Open the link on an iPhone with Concourse to follow it.",
     """  <main>
    <div class="wrap hero">
      <span class="icon lg" aria-hidden="true"><img src="/assets/icons/concourse.svg?v=""" + str(VERSION) + """" alt="" width="120" height="120"></span>
      <h1>Follow this train.</h1>
      <p>Someone has shared a train with you. Open this link on an iPhone with Concourse and you'll get a notification for its platform, any delay, when it leaves and when it arrives.</p>
      <a class="btn" href="/concourse/">About Concourse</a>
    </div>
  </main>""", app="concourse")

# Universal links: lets "Share So Others Can Follow" links open the Concourse app. GitHub Pages only
# publishes the hidden .well-known folder because _config.yml includes it.
os.makedirs(os.path.join(ROOT, ".well-known"), exist_ok=True)
with open(os.path.join(ROOT, ".well-known", "apple-app-site-association"), "w") as f:
    f.write("""{
  "applinks": {
    "details": [
      {
        "appIDs": ["L9U83YL7ZP.app.southby.concourse"],
        "components": [{ "/": "/concourse/follow/*", "comment": "Share So Others Can Follow" }]
      }
    ]
  }
}
""")
with open(os.path.join(ROOT, "_config.yml"), "w") as f:
    f.write('# GitHub Pages: publish the .well-known folder (universal links). Written by _build/build_site.py.\ninclude: [".well-known"]\n')

# ---------------------------------------------------------------- 404
page("404.html", "Page not found — southby.app", "Page not found.",
     """  <main>
    <div class="wrap hero">
      <h1>Not found.</h1>
      <p>That page doesn't exist. <a href="/">Go to the home page</a>.</p>
    </div>
  </main>""")

print("built")
