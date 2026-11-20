# Feature icons for southby.app, drawn like the app icons: a soft white shape behind, a solid one in
# front, on the app's own gradient. svg(name, app, uid) returns one inline SVG.
import math
def rr(x,y,w,h,r): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
def c(x,y,r): return f'<circle cx="{x}" cy="{y}" r="{r}"/>'
def p(d, extra=""): return f'<path d="{d}"{extra}/>'
def star(cx,cy,R,r):
    pts=[]
    for k in range(10):
        a=math.radians(-90+36*k); rad=R if k%2==0 else r
        pts.append(f"{cx+rad*math.cos(a):.1f} {cy+rad*math.sin(a):.1f}")
    return p("M"+" L".join(pts)+"Z")
def drop(x,y,s=1):
    return p(f"M{x} {y} C{x-4*s} {y+8*s} {x-7*s} {y+12*s} {x-7*s} {y+16*s} A{7*s} {7*s} 0 0 0 {x+7*s} {y+16*s} C{x+7*s} {y+12*s} {x+4*s} {y+8*s} {x} {y}Z")
WAVE_LO='M0 66 C17 56 33 56 50 66 S83 76 100 66 V100 H0Z'
WAVE_HI='M0 50 C17 40 33 40 50 50 S83 60 100 50 V100 H0Z'
def clock(cx,cy,R, h1=(0,-1), h2=(0.7,0.4)):
    # face in front, hands cut
    return c(cx,cy,R), (rr(cx-3.5,cy-R*0.62,7,R*0.62+3.5,3.5) + p(f"M{cx-3} {cy-1} L{cx+R*0.45} {cy+R*0.3} L{cx+R*0.45-4} {cy+R*0.3+6} L{cx-3} {cy+6}Z"))
def pin(cx,top,w,h):
    r=w/2; cy=top+r
    return p(f"M{cx} {top} C{cx-r*0.85} {top} {cx-r} {top+r*0.55} {cx-r} {cy} C{cx-r} {cy+r*0.9} {cx} {top+h} {cx} {top+h} C{cx} {top+h} {cx+r} {cy+r*0.9} {cx+r} {cy} C{cx+r} {top+r*0.55} {cx+r*0.85} {top} {cx} {top}Z")
def magnifier():
    back=c(50,50,40)
    front=c(42,42,24)+p("M55 60 L64 51 L88 75 A6.4 6.4 0 0 1 79 84 Z")
    cut=c(42,42,14)
    return back,front,cut
def bookmark():
    return (p("M14 22 H48 V84 L31 72 L14 84 Z"), p("M34 12 H80 V92 L57 76 L34 92 Z"), star(57,42,13,5.5))
def calendar(lines=True):
    back=rr(8,20,84,74,14)
    front=rr(16,26,68,62,10)+rr(28,12,8,20,4)+rr(64,12,8,20,4)
    cut=rr(16,40,68,5,0)
    if lines:
        for i,x in enumerate([24,40,56,72]):
            for y in [52,68]:
                cut+=rr(x-2,y,9,9,2.5)
    return back,front,cut
ICONS = {
 # Afon
 "warning": (p(WAVE_LO.replace('66','74').replace('56','64').replace('76','84')),
             p("M50 16 L86 80 H14 Z",' stroke="#fff" stroke-width="10" stroke-linejoin="round"'),
             rr(45.5,38,9,24,4.5)+c(50,70,5)),
 "bell": (c(50,48,40), p("M50 16 C34 16 28 30 28 44 V58 L18 70 H82 L72 58 V44 C72 30 66 16 50 16Z")+p("M40 76 A10 10 0 0 0 60 76Z"), ""),
 "levels": (p(WAVE_HI), p(WAVE_LO)+rr(62,10,14,90,3), rr(62,20,7,4,0)+rr(62,32,7,4,0)+rr(62,44,7,4,0)),
 "plain": (rr(30,30,62,46,14)+p("M76 74 L84 88 L66 76Z"), rr(8,14,62,48,14)+p("M22 60 L16 76 L36 62Z"), rr(20,28,38,6,3)+rr(20,40,28,6,3)),
 "map": (p("M6 30 L34 18 L66 30 L94 18 V74 L66 86 L34 74 L6 86 Z"), pin(50,10,48,66), c(50,34,9)),
 "full": (rr(28,10,44,84,14), rr(28,10,44,84,14).replace('rx="14"','rx="14" opacity="0"')+p("M28 52 C35 48 42 48 50 52 S65 56 72 52 V80 A14 14 0 0 1 58 94 H42 A14 14 0 0 1 28 80Z"), ""),
 "saved": bookmark(),
 "rain": (drop(32,62)+drop(52,68)+drop(72,62), c(36,40,15)+c(56,30,20)+c(74,42,13)+rr(21,36,66,19,9.5), ""),
 "along": (p("M-5 70 C20 40 40 80 60 50 S90 20 105 30",' stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round"'),
           c(20,52,12)+c(56,56,12)+c(86,30,12), c(20,52,5)+c(56,56,5)+c(86,30,5)),
 "gaps": (c(50,50,42),)+clock(50,50,30)[0:1]+(clock(50,50,30)[1],),
 "widget": (rr(18,6,64,96,16), rr(26,16,22,22,6)+rr(52,16,22,22,6)+rr(26,42,48,22,6)+rr(26,68,22,22,6)+rr(52,68,22,22,6), ""),
 # Concourse
 "board": (rr(4,18,92,70,12), rr(12,26,76,54,8), rr(20,35,22,6,3)+rr(48,35,32,6,3)+rr(20,49,22,6,3)+rr(48,49,32,6,3)+rr(20,63,22,6,3)+rr(48,63,32,6,3)),
 "near": (c(50,50,44), c(50,50,28), c(50,50,17)+''),
 "destination": (rr(44,40,12,62,3), p("M14 16 H74 L90 31 L74 46 H14 Z")+p("M86 52 H26 L10 67 L26 82 H86 Z").replace('/>',' opacity=".45"/>'), ""),
 "stops": (rr(44,4,12,96,6), c(50,22,11)+c(50,50,11)+c(50,78,11)+rr(66,17,26,10,5)+rr(66,45,20,10,5)+rr(66,73,24,10,5)+rr(8,17,22,10,5).replace('/>',' opacity="0"/>'), c(50,22,4.5)+c(50,50,4.5)+c(50,78,4.5)),
 "info": (c(50,50,44), c(50,50,32), c(50,34,5.5)+rr(45,44,10,26,5)),
 "earlier": (c(50,50,44), c(50,50,30)+p("M8 30 L28 30 L20 12 Z"), rr(46.5,32,7,21,3.5)+rr(46.5,46.5,20,7,3.5)),
 "search": magnifier(),
 # Settee
 "finds": (c(50,86,62), p("M10 46 A56 56 0 0 1 90 46 L80 56 A42 42 0 0 0 20 56Z")+p("M28 64 A32 32 0 0 1 72 64 L62 74 A18 18 0 0 0 38 74Z")+c(50,86,9), ""),
 "touch": (rr(10,10,80,80,20), rr(18,18,64,64,14), c(50,50,14)),
 "type": (rr(4,20,92,64,14), rr(12,28,76,48,9), "".join(rr(20+i*13,36,9,8,2.5) for i in range(5))+"".join(rr(26+i*13,50,9,8,2.5) for i in range(4))+rr(32,64,36,6,3)),
 "play": (c(50,44,40), c(50,44,28)+rr(10,84,80,8,4), p("M44 32 L62 44 L44 56Z")+rr(10,84,46,8,0).replace('/>',' opacity="0"/>')),
 "library": (rr(26,8,58,72,10), rr(14,22,58,72,10), rr(24,34,38,24,4)+rr(24,66,26,6,3)+rr(24,78,18,6,3)),
 "resume": (c(50,50,44), p("M50 18 A32 32 0 1 1 18 50 H30 A20 20 0 1 0 50 30 Z")+p("M50 6 L68 24 L50 42 Z"), ""),
 "watched": (c(50,50,44), c(50,50,32), p("M34 50 L45 61 L67 39",' stroke="url(#g)" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"')),
 "tidy": (star(70,30,22,9), star(42,58,34,13), ""),
 # Lineside
 "today": calendar(),
 "choose": (rr(8,14,84,72,16), rr(16,22,68,24,12)+rr(16,54,68,24,12), c(70,34,8)+c(30,66,8)),
 "live": (c(50,50,44), p("M18 50 A32 32 0 0 1 82 50 H70 A20 20 0 0 0 30 50Z")+c(50,58,13), ""),
 "spots": (p("M6 76 L50 60 L94 76 L50 94Z"), pin(50,8,50,72), c(50,33,10)),
 "coming": calendar(),
 "late": (star(50,50,44,18), star(50,50,30,12), ""),
 "route": (p("M6 30 L34 18 L66 30 L94 18 V74 L66 86 L34 74 L6 86 Z"), p("M18 70 C30 40 50 70 62 44 S80 30 84 26",' stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"')+c(62,44,9), c(62,44,4)),
 "honest": (c(50,50,42),)+clock(50,50,30),
 # Kerbside
 "stop": (c(50,50,44), rr(44,36,12,64,3)+c(50,30,24), rr(38,24,24,12,6)),
 "bus": (pin(50,4,60,92), rr(30,18,40,46,10), rr(36,26,28,12,2)+c(39,54,3.5)+c(61,54,3.5)),
 # Home
 "phone": (rr(18,4,64,96,18), rr(26,10,48,84,12), rr(42,16,16,5,2.5)),
 "lock": (p("M28 46 V36 A22 22 0 0 1 72 36 V46 H62 V36 A12 12 0 0 0 38 36 V46Z"), rr(16,42,68,52,14), c(50,62,7)+rr(46.5,62,7,16,3.5)),
 "mail": (rr(4,22,92,64,14), rr(12,28,76,52,10), p("M14 32 L50 58 L86 32",' stroke="url(#g)" stroke-width="7" fill="none" stroke-linejoin="round" stroke-linecap="round"')),
}
APPS = {"afon": ("#2aa7ff","#0057d9"), "concourse": ("#ffc94d","#f08c00"), "settee": ("#ff8a65","#d63a2f"),
        "lineside": ("#6d5dfc","#2a1d73"), "kerbside": ("#3ddc84","#0a7a45"), "studio": ("#2aa7ff","#0057d9")}
def svg(name, app, uid="g"):
    back, front, cut = ICONS[name]
    a, b = APPS[app]
    defs = f'<defs><linearGradient id="{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="40" y2="100"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
    fix = lambda s: s.replace('url(#g)', f'url(#{uid})')
    return (f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{defs}'
            f'<rect width="100" height="100" fill="url(#{uid})"/><g fill="#fff" opacity=".4">{fix(back)}</g>'
            f'<g fill="#fff" opacity=".92">{fix(front)}</g><g fill="url(#{uid})">{fix(cut)}</g></svg>')
