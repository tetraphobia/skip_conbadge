import sys
import math
import time
import os
import machine
from badgeware.sprite import SpriteSheet

sys.path.insert(0, "/system/apps/skip_conbadge")
os.chdir("/system/apps/skip_conbadge")


# Constants
BADGE_VIEW = 0
SOCIALS_VIEW = 1
ARTIST_VIEW = 2

# For consistency with animation timing
_frame_index = 0
_last_frame_ms = 0

# Background Swirlies
CX = screen.width / 2
CY = screen.height / 2

_bg_color = color.rgb(30, 180, 255)

# Views
current_view = BADGE_VIEW

views = {
    machine.Pin.board.BUTTON_A: BADGE_VIEW,
    machine.Pin.board.BUTTON_B: SOCIALS_VIEW,
    machine.Pin.board.BUTTON_C: ARTIST_VIEW,
}

# Socials
socials = [
    {
        'social': 'discord',
        'handle': 'skipkin'
    },
    {
        'social': 'github',
        'handle': 'tetraphobia'
    },
    {
        'social': 'twitch',
        'handle': 'skippykin'
    },
    {
        'social': 'steam',
        'handle': 'notvalkyrie'
    },
    {
        'social': 'telegram',
        'handle': 'skipkin'
    },
]

def shadow_text(text, x, y, font, shadow_color=color.rgb(0, 10, 0, 90), text_color=color.rgb(255, 255, 255)):
    screen.font = font

    screen.pen = shadow_color
    screen.text(text, x + 1, y + 1)

    screen.pen = text_color
    screen.text(text, x, y)

def draw_bg_swirl(r, g, b, alpha=50, arms = 10, speed = 1.5, curve = 0.3):
    global _bg_color
    cy = CY - 8
    cx = CX

    if _bg_color is not None:
        screen.pen = _bg_color
        screen.rectangle(0, 0, screen.width, screen.height)
        

    y = 0
    for _row in range(12):
        x = 0
        for _col in range(16):
            dx = (x + 5) - cx
            dy = (y + 5) - cy

            dist = math.sqrt(dx * dx + dy * dy)
            theta = math.atan2(dy, dx)

            phase = (theta * arms) + (dist * curve) - (badge.ticks * speed / 1000)
            pulse = (math.sin(phase) / 2) + 0.5
            pulse = 0.8 + (pulse / 2)

            screen.pen = color.rgb(r, g, b, alpha * pulse)
            screen.rectangle(x, y, 10, 10)


            x += 10
        y += 10

def draw_badge_view():
    global _frame_index, _last_frame_ms, _bg_color

    _bg_color = color.rgb(222, 100, 17)

    draw_bg_swirl(
        r=255,
        g=245,
        b=220,
        alpha=100,
        arms=4,
        speed=3,
        curve=0.08,
    )


    NUM_FRAMES = 8
    SPEED = 6 # frames per second

    sheet = SpriteSheet("assets/skip.png", 1, NUM_FRAMES)
    anim = sheet.animation(x=0, y=0, count=NUM_FRAMES, horizontal=False)

    now = time.ticks_ms()

    if time.ticks_diff(now, _last_frame_ms) >= 1000 // SPEED:
        _frame_index = (_frame_index + 1) % NUM_FRAMES
        _last_frame_ms = now

    # circles
    screen.pen = color.rgb(245, 209, 184, 80)
    screen.shape(shape.circle(45, 45, 40))
    screen.shape(shape.circle(screen.width - 65, screen.height - 65, 60))


    # platform
    screen.pen = color.rgb(245, 209, 184)
    screen.shape(shape.rectangle(screen.width / 4, screen.height - 25, screen.width / 2, 20))
    # left edge
    screen.triangle(
            screen.width / 4, screen.height - 5,
            screen.width / 4, screen.height - 26,
            screen.width / 4 - 20, screen.height - 5,
        )
    screen.triangle(
            screen.width / 4 * 3 - 1, screen.height - 5,
            screen.width / 4 * 3, screen.height - 26,
            screen.width / 4 * 3 + 20, screen.height - 5,
        )

    # sprite
    screen.blit(anim.frame(_frame_index), vec2(CX - sheet.sw / 2, screen.height - sheet.sh - 5))

    # skip
    screen.font = rom_font.outflank

    screen.pen = color.rgb(0, 10, 0, 90)
    screen.text("Skip,", screen.width - 42, 1)

    screen.pen = color.rgb(255, 255, 255)
    screen.text("Skip,", screen.width - 41, 0)

    # teacup gryphon
    screen.font = rom_font.kobold

    screen.pen = color.rgb(0, 10, 0, 90)
    screen.text("Teacup", screen.width - 46, 21)
    screen.text("Gryphon", screen.width - 52, 30)

    screen.pen = color.rgb(255, 255, 255)
    screen.text("Teacup", screen.width - 45, 20)
    screen.text("Gryphon", screen.width - 51, 29)

def draw_socials_view():
    global _bg_color
    _bg_color=color.rgb(9, 101, 230)

    draw_bg_swirl(
        r=247,
        g=202,
        b=148,
        alpha=70,
        arms=30,
        speed=2,
        curve=0.002,
    )

    screen.pen = color.rgb(255, 255, 255)


    vert_offset = (screen.height / 2) - (len(socials) * 20 / 2)

    for s in socials:
        icon = image.load(f"assets/socials/{s['social']}.png")
        screen.blit(icon, vec2(5, vert_offset))
        shadow_text(s['handle'], 25, vert_offset, font=rom_font.kobold)
        vert_offset += 20


def draw_artist_view():
    global _bg_color
    _bg_color=color.rgb(107, 24, 168)

    draw_bg_swirl(
        r=226,
        g=207,
        b=240,
        alpha=100,
        arms=-2,
        speed=3,
        curve=0.08,
    )
    # bg
    screen.pen = color.rgb(44, 26, 50, 97)
    screen.rectangle(0, screen.height - 20, screen.width, screen.height)

    # sprite
    shion = image.load("assets/shion.png")
    screen.blit(shion, vec2(-90, 30))

    # 'artist'
    shadow_text("Artist", 5, 5, font=rom_font.kobold)

    # 'shiones'
    shadow_text("Shiones", 5, 15, font=rom_font.more)

    # qr
    qr = image.load("assets/shionesqr.png")
    screen.pen = color.rgb(44, 26, 50, 70)
    screen.rectangle(screen.width - qr.width - 1, 1, qr.width, qr.height)
    screen.blit(qr, vec2(screen.width - qr.width - 1, 1))

    # 'scan me'
    shadow_text("Scan me!", screen.width - 55, 62, font=rom_font.sins)

def update():
    global current_view

    if (len(badge.pressed()) > 0):
        if badge.pressed()[-1] in views.keys():
            current_view = views[badge.pressed()[-1]]

    if current_view == BADGE_VIEW:
        draw_badge_view()
    elif current_view == SOCIALS_VIEW:
        draw_socials_view()
    elif current_view == ARTIST_VIEW:
        draw_artist_view()
    else:
        draw_badge_view()

run(update)
