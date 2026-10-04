"""Animate the contribution grid itself: a cat hoverboard and travelling tile ripples."""
from datetime import date, timedelta
from math import hypot, sin

from build_artwork_v4 import cat, svg, text
from build_artwork_v5 import recolour


def section_heading(theme='light',mobile=False):
    """A theme-aware section heading in the profile's existing visual style."""
    blue,mint,chip=('#8bc9f4','#92d8c0','#25485f') if theme=='dark' else ('#2869a4','#237d72','#dcecf8')
    width,height=(400,76) if mobile else (960,48)
    icon_y=20 if mobile else 8
    s=f'<defs><linearGradient id="heading-ink"><stop stop-color="{blue}"/><stop offset="1" stop-color="{mint}"/></linearGradient></defs>'
    s+=f'<g transform="translate(1 {icon_y})"><rect width="34" height="34" rx="10" fill="{chip}"/>'
    s+=f'<path d="M7 23C13 24 12 14 20 14C24 14 24 18 27 18C26 25 17 29 7 23Z" stroke="{mint}" stroke-width="1.8" stroke-linejoin="round"/>'
    s+=f'<path d="M7 28Q12 26 17 28T27 28" stroke="{blue}" stroke-width="1.5" stroke-linecap="round"/>'
    s+='<path d="M26 6V12M23 9H29" stroke="#d8ad5f" stroke-width="1.5" stroke-linecap="round"/></g>'
    if mobile:
        s+=text(48,29,'Small steps,',26,'url(#heading-ink)',750,'letter-spacing="-.6"')
        s+=text(48,59,'cosmic ripples',26,'url(#heading-ink)',750,'letter-spacing="-.6"')
    else:
        s+=text(48,35,'Small steps, cosmic ripples',32,'url(#heading-ink)',750,'letter-spacing="-.7"')
    return svg(width,height,'Small steps, cosmic ripples',s)


def layout(snapshot,mobile=False):
    last=date.fromisoformat(snapshot['as_of'])
    first=(last-timedelta(days=(last.weekday()+1)%7)-timedelta(weeks=12)) if mobile else date.fromisoformat(snapshot['from'])
    origin=first-timedelta(days=(first.weekday()+1)%7)
    days=[day for day in snapshot['days'] if date.fromisoformat(day['date'])>=first]
    columns=(last-origin).days//7+1
    gx,gy,pitch,size=(69,104,20,14) if mobile else (76,98,16,12)
    cells=[]
    for item in days:
        day=date.fromisoformat(item['date'])
        col,row=(day-origin).days//7,(day.weekday()+1)%7
        cells.append(dict(item,column=col,row=row,x=gx+col*pitch,y=gy+row*pitch,size=size))
    route=[]
    for col in range(columns):
        week=[cell for cell in cells if cell['column']==col]
        if any(cell['count'] for cell in week):
            target=max(week,key=lambda cell:(cell['count'],cell['date']))
        else:
            # A gentle path inside quiet weeks, following an actual cell in the grid.
            row=round(3+2*sin(col/4))
            target=min(week,key=lambda cell:abs(cell['row']-row))
        route.append((target['x']+size/2,target['y']+size/2))
    return days,cells,route,first


def motion_frames(route,steps=6):
    """Round off vertical turns while visiting the centre of each real day.

    A smoothstep curve eases the climb without skipping calendar cells. Travel
    time follows distance, so a steep climb gets more time than a flat section.
    """
    stops=route+route[-2:0:-1]+route[:1]
    frames=[]
    for index,((x0,y0),(x1,y1)) in enumerate(zip(stops,stops[1:])):
        for step in range(steps):
            t=step/steps
            eased=t*t*(3-2*t)
            slope=(y1-y0)*6*t*(1-t)/(x1-x0)
            angle=max(-8,min(8,slope*4))
            frames.append(((index+t)/(len(stops)-1)*100,
                           x0+(x1-x0)*t,y0+(y1-y0)*eased,angle))
    frames.append((100,*route[0],0))
    distances=[0.]
    for previous,current in zip(frames,frames[1:]):
        distances.append(distances[-1]+hypot(current[1]-previous[1],current[2]-previous[2]))
    return [(distance/distances[-1]*100,x,y,angle)
            for distance,(_,x,y,angle) in zip(distances,frames)]


def ripple_frames(column,columns,kind,forward=None):
    if forward is None:
        forward=column/(columns-1)*50
    peaks=[forward,100-forward]
    positions={0.,100.}
    for peak in peaks:
        positions.update([max(0.,peak-2),peak,min(100.,peak+2)])
    frames=[]
    for position in sorted(positions):
        distance=min(min(abs(position-peak),100-abs(position-peak)) for peak in peaks)
        strength=max(0,1-distance/2)
        value=f'transform:translateY(calc(var(--lift)*{strength:.3f}))' if kind=='lift' else f'opacity:{strength*.85:.3f}'
        frames.append(f'{position:.4f}%{{{value}}}')
    return ''.join(frames)


def rider(theme):
    # Keep the profile mascot, with balancing paws and a tiny wind-blown scarf.
    # Its face uses the same dark eyes in both themes, against the pale blue fur.
    s='<g class="scarf"><path d="M-9-11L-24-8L-20-4L-8-9Z" fill="#edbe70" stroke="#b48d4f" stroke-width=".8"/></g>'
    s+=recolour(cat(-13.2,-29,2.4).replace('#34304b','#e3cff4'),theme)
    s+='<g class="cat-eyes" fill="#24465c"><rect x="-8.4" y="-19.4" width="2.4" height="2.4"/><rect x="1.2" y="-19.4" width="2.4" height="2.4"/></g>'
    s+='<path d="M-15.6-7H-10.8M8.4-7H13.2" stroke="#446b85" stroke-width="4.8"/><path d="M-14.4-7H-10.8M8.4-7H12" stroke="#bbdcef" stroke-width="2.4"/>'
    s+='<path d="M-8.4-10.8H6" stroke="#edbe70" stroke-width="2.4"/>'
    s+='<path d="M-21 1Q0-5 21 1L15 5H-15Z" fill="#74bbaa" stroke="#527e90" stroke-width="1.1"/><path d="M-13 8H13" stroke="url(#rainbow)" stroke-width="3" stroke-linecap="round"/>'
    s+='<path d="M-14 0Q0-3 14 0" stroke="#d4f5e8" stroke-width=".9" opacity=".8"/>'
    s+='<circle cx="-14" cy="2" r="1.5" fill="#ffe298"/><circle cx="14" cy="2" r="1.5" fill="#ffe298"/>'
    return s


def render(snapshot,theme='light',mobile=False):
    dark=theme=='dark'
    width,height=(400,298) if mobile else (960,252)
    ink,muted=('#e1edf5','#9fb8ca') if dark else ('#19364b','#597487')
    levels=['#233849','#345f57','#4d8f77','#6cbaa0','#9ee8c1'] if dark else ['#e1ebef','#b0d9c5','#83bea1','#559c7b','#327b5c']
    colours=['#69bcd0','#98aee7','#edbe70','#77c5a6']
    days,cells,route,first=layout(snapshot,mobile)
    total=sum(day['count'] for day in days)
    count=sum(bool(day['count']) for day in days)
    last=date.fromisoformat(snapshot['as_of'])
    period=f'{first:%d %b %Y} — {last:%d %b %Y}'
    columns=len(route)
    duration=20 if mobile else 26
    frames=motion_frames(route)
    path=''.join(f'{position:.4f}%{{transform:translate({x:.2f}px,{y:.2f}px)}}' for position,x,y,angle in frames)
    bank=''.join(f'{position:.4f}%{{transform:rotate({angle:.2f}deg)}}' for position,x,y,angle in frames)
    css=f'.rider,.wake{{animation:ride {duration}s linear infinite}}.bank{{animation:bank {duration}s linear infinite}}@keyframes ride{{{path}}}@keyframes bank{{{bank}}}'
    css+=f'.facing{{animation:facing {duration}s step-end infinite}}@keyframes facing{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(-1)}}}}'
    css+='.board-float{animation:hover 2.6s ease-in-out infinite}.scarf{animation:breeze 1.3s ease-in-out infinite}.cat-eyes{animation:blink 6.7s step-end infinite}@keyframes hover{0%,100%{transform:translateY(-1px)}50%{transform:translateY(1px)}}@keyframes breeze{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(4deg)}}@keyframes blink{0%,93%,97%,100%{opacity:1}94%,96%{opacity:0}}'
    for column in range(columns):
        arrival=frames[column*6][0]
        css+=f'.c{column}{{animation:lift{column} {duration}s ease-in-out infinite}}.g{column}{{animation:glow{column} {duration}s ease-in-out infinite}}@keyframes lift{column}{{{ripple_frames(column,columns,"lift",arrival)}}}@keyframes glow{column}{{{ripple_frames(column,columns,"glow",arrival)}}}'
    busiest=max(range(columns),key=lambda column:sum(cell['count'] for cell in cells if cell['column']==column))
    initial_phase=frames[max(0,busiest-2)*6][0]/100*duration
    css+=f'.rider,.bank,.facing,.tile,.tile-glow{{animation-delay:-{initial_phase:.4f}s}}'
    css+='@media(prefers-reduced-motion:reduce){.tile,.tile-glow,.rider,.wake,.bank,.facing,.board-float,.scarf,.cat-eyes{animation:none}.tile-glow{opacity:0}.surf-motion{display:none}}'
    title=f'Contribution surf. {total} real contributions across {count} active days, {period}. A blue pixel cat leans into turns on a hoverboard inside the contribution grid, leaving a fading rainbow wake. Nearby squares lift in a travelling ripple and active squares gain a colourful outline. Counts and activity colours stay unchanged.'
    s=f'<defs><linearGradient id="rainbow"><stop stop-color="#69bcd0"/><stop offset=".35" stop-color="#98aee7"/><stop offset=".7" stop-color="#edbe70"/><stop offset="1" stop-color="#77c5a6"/></linearGradient><radialGradient id="board-glow"><stop stop-color="#69bcd0" stop-opacity=".2"/><stop offset="1" stop-color="#69bcd0" stop-opacity="0"/></radialGradient></defs><style>{css}</style>'
    s+=text(25,22 if mobile else 30,'Contribution surf',17 if mobile else 19,ink,700,'letter-spacing="-.4"')
    accent_y=32 if mobile else 44
    s+=f'<rect x="25" y="{accent_y}" width="44" height="2.5" rx="1.25" fill="url(#rainbow)"/>'
    if mobile:
        s+=text(25,48,f'{total} contributions · latest 13 weeks',11,muted)
    else:
        s+=text(925,30,f'{total} contributions · {count} active days',12,muted,extra='text-anchor="end"')
    pitch,size=(20,14) if mobile else (16,12)
    gy=104 if mobile else 98
    for row,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
        s+=text(25,gy+row*pitch+size/2+3,label,9,muted)
    previous_month=None
    for cell in cells:
        day=date.fromisoformat(cell['date'])
        if day.month!=previous_month and (day.day<=7 or previous_month is None):
            if cell['column']<columns-1:
                s+=text(cell['x'],70 if mobile else 64,day.strftime('%b'),9,muted)
            previous_month=day.month
        x,y,level,col=cell['x'],cell['y'],cell['level'],cell['column']
        # Animation changes position and outlines; the real intensity fill never changes.
        distance=abs(y+size/2-route[col][1])/pitch
        lift=.6+2.9*max(0,1-distance/3)
        s+=f'<g class="tile c{col}" style="--lift:-{lift:.3f}px"><rect data-date="{cell["date"]}" data-count="{cell["count"]}" data-level="{level}" x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{levels[level]}"><title>{cell["date"]}: {cell["count"]} contributions</title></rect>'
        if level:
            s+=f'<rect class="tile-glow g{col}" x="{x-1}" y="{y-1}" width="{size+2}" height="{size+2}" rx="4" fill="none" stroke="{colours[col%4]}" stroke-width="1.8" opacity="0"/>'
        s+='</g>'
    x,y=route[0]
    # Closely spaced afterimages follow the same curved journey, forming a short
    # tapered ribbon. They are decoration, never new activity or intensity fills.
    s+='<g class="surf-motion" aria-hidden="true" pointer-events="none">'
    journey_length=sum(hypot(right[1]-left[1],right[2]-left[2]) for left,right in zip(frames,frames[1:]))
    spacing=3*duration/journey_length
    for index in range(16,0,-1):
        phase=(initial_phase-spacing*index)%duration
        taper=1-index/18
        radius=.6+1.5*taper
        s+=f'<g class="wake" style="transform:translate({x:g}px,{y:g}px);animation-delay:-{phase:.4f}s" opacity="{.18+.65*taper:.3f}">'
        for dy,colour in [(4,'#69bcd0'),(6.8,'#a9a7e8'),(9.6,'#edbe70')]:
            s+=f'<circle cy="{dy}" r="{radius:.2f}" fill="{colour}"/>'
        s+='</g>'
    s+=f'<g class="rider" style="transform:translate({x:g}px,{y:g}px)"><g class="bank"><g class="board-float"><circle cy="4" r="19" fill="url(#board-glow)"/><g class="facing">{rider(theme)}</g></g></g></g></g>'
    foot=259 if mobile else 235
    s+=text(25,foot,'quiet',9,muted)
    for level in range(5):
        s+=f'<rect x="{58+level*15}" y="{foot-8}" width="10" height="10" rx="2" fill="{levels[level]}"/>'
    s+=text(141,foot,'bright',9,muted)
    if mobile:
        s+=text(25,282,period,10,muted)
    else:
        s+=text(925,foot,period,10,muted,extra='text-anchor="end"')
    return svg(width,height,title,s)
