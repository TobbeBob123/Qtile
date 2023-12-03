# Read README.org before you dive into my config and change my config.
# The best way to read README.org is to see my gitlab at https://gitlab.com/TobbeBob123/Qtile

import os
from os.path import expanduser
import re
import socket
import subprocess
from libqtile import qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, Rule
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
myTerm = "kitty"
myLauncher = "rofi -show drun"
myEmacs= "emacsclient -c -a 'emacs' "
myBrowser= "brave"
soundDir = "~/Sound/"
volumeSound = soundDir + "ComputerErrorsoundeffect.mp4"
mySoundPlayer = "ffplay -nodisp -autoexit "
_NET_WM_STRUT_PARTIAL = 1

keys = [
    Key([mod], "d", lazy.spawn(myLauncher), desc="Launch program launcher"),
    Key([mod], "Return", lazy.spawn(myEmacs), desc="Launch emacs"),
    Key([mod, "shift"], "Tab", lazy.spawn(myBrowser), desc="Launch web"),
    Key([mod, "shift"], "t", lazy.spawn("libreoffice"), desc="Launch LibreOffice"),
    Key([mod, "shift"], "f", lazy.spawn("pcmanfm"), desc="Launch filebrowser"),
    Key([mod], "m", lazy.spawn("geary"), desc="Launch Mailclient."),

    Key([mod], "l", lazy.spawn("light-locker-command -l"), desc="Lock the computer"),
    Key([mod], "p", lazy.spawn(expanduser("~/Script/SkjermBilde.sh"), shell=True), desc="Take fullscreen screenshot"),
    Key([mod, "shift"], "p", lazy.spawn(expanduser("~/Script/Flameshot.sh"), shell=True), desc="Take region screenshot"),
    Key([mod], "BackSpace", lazy.spawn(expanduser("~/xmenu/xmenu.sh"), shell=True), desc="Xmenu"),

    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "g", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "h", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+ unmute")),

    # Screenlight
    Key([], "XF86MonBrightnessDown", lazy.spawn("lux -s 5%"), desc="Decrease screenlight"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("lux -a 5%"), desc="increase screenlight")
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

groups = [
    Group(name=str(i), **group)
    for i, group in enumerate(
            [
                {
                    "label": "Emacs",
                    "matches": [
                        Match(wm_class="Emacs"),
                    ],
                },
                {
                    "label": "Soc",
                    "matches": [
                        Match(wm_class="Signal"),
                        Match(wm_class="discord"),
                    ],
                },
                {
                    "label": "File",
                    "matches": [
                        Match(wm_class="Pcmanfm"),
                    ],
                },
                {
                    "label": "Web",
                    "matches": [
                        Match(wm_class="Brave-browser"),
                        Match(wm_class="firefox"),
                    ],
                },
                {
                    "label": "Work",
                    "matches": [
                        Match(title="LibreOffice"),
                    ],
                },
            ], start=1,
    )
]
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirm"),
        Match(wm_class="file_progress"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="Nm-connection-editor"),
        Match(wm_class="Gtk2_prefs"),
        Match(wm_class="Steam"),
        Match(wm_class="lunarclient"),
        Match(wm_class="Yad"),
        Match(wm_class="fim"),
        Match(wm_class="Pavucontrol"),
        Match(wm_class="CoreImage"),
        Match(wm_class="stacer"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="Geary"),
        Match(wm_class="kitty"),
        Match(wm_class="discord"),
        Match(wm_class="Bitwarden"),
    ], **layout_theme
)

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_labels = ["Emacs", "Soc", "File", "Web", "Work", "Fun", "7", "8", "9",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

groups.append(ScratchPad('sp', [
    DropDown('term', myTerm, width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown('nm', 'nm-connection-editor', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown('audio', 'pavucontrol', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown("blue", 'blueman-manager', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown("steam", 'steam', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown("bit", 'bitwarden-desktop', width=0.4, x=0.3, y=0.2, opacity=1),
]))

keys.extend([
    Key([mod], "e", lazy.group["sp"].dropdown_toggle("term"), desc="Launch terminal"),
    Key([mod, "shift"], "n", lazy.group["sp"].dropdown_toggle("nm"), desc="Launch Nm-connection-editor. An Network GUI manager"),
    Key([mod, "shift"], "l", lazy.group["sp"].dropdown_toggle("audio"), desc="Launch Pavucontrol. An Volume GUI manager"),
    Key([mod], "b", lazy.group["sp"].dropdown_toggle("blue"), desc="Launch Bluetooth Gui."),
    Key([mod, "shift"], "b", lazy.group["sp"].dropdown_toggle("bit"), desc="Launch bitwarden."),
])

layout_theme = {
    "border_width": 1,
    "margin": 0,
    "border_focus": "ff79c6",
    "border_normal": "282a36"
    }
layouts = [
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.MonadTall(**layout_theme),
    layout.Max(),
]

widget_defaults = dict(
    font='Source Code Pro',
    fontsize = 11,
    margin_y = 3,
    margin_x = 4,
    padding_y = 2,
    padding_x = 3,
    padding=5
)
extension_defaults = widget_defaults.copy()

window_name = widget.WindowName()

main_bar = bar.Bar(
    [
        widget.Sep(
            background="#282a36",
            foreground="#282a36"),
        widget.Image(
            filename = '~/.config/qtile/icon/logo.xpm'),
        widget.GroupBox(
             fontsize = 11,
             margin_y = 3,
             margin_x = 4,
             padding_y = 2,
             padding_x = 3,
             borderwidth = 1,
             rounded = False,
             highlight_method="line",
             active = "#8be9fd",
             inactive = "#ff79c6"
            ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.CurrentLayout(
            font='Source Code Pro'),
       widget.Spacer(lenght = 8),
       widget.CheckUpdates(
            custom_command = 'paru -Qu',
            colour_no_updates = '#50fa7b',
            font='Source Code Pro',
            colour_have_updates = '#ff5555',
            no_update_string='No updates',
            update_interval = 60),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.Battery(
            foreground = '#f1fa8c',
            format = '{percent:2.0%}',
            fmt = 'Bat:{}',
            show_short_text = False,
            update_interval = 5,
            ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.CPU(
            format = 'CPU: {load_percent}%',
            foreground = "#ff76c6",
            font='Source Code Pro'),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.Memory(
            format = '{MemUsed: .0f}{mm}',
            fmt = 'Mem:{} used',
            foreground = '#ffb86c',
            font='Source Code Pro'),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.Volume(
            fmt = 'Vol:{}',
            foreground = "#50fa7b",
            font='Source Code Pro'),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.Clock(format="%H:%M:%S %d-%m-%Y", font='Source Code Pro'),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 85),
       widget.Systray(),
       widget.Sep(
            foreground = "#282a36"),
       ], 30, background= "#282a36", foreground="#44475a", font='Source Code Pro', fontsize=12)

            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta

main_screen = Screen(top=main_bar)
screens = [main_screen]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

wmname = "LG3D"
