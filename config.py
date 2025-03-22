# Read README.org before you dive into my config and change my config.
# The best way to read README.org is to see my gitlab at https://gitlab.com/TobbeBob123/Qtile

import os
from os.path import expanduser
import re
import socket
import subprocess
from libqtile import qtile, widget, extension, bar, layout, hook
import qtile_extras
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, Rule
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
myTerm = "kitty"
myLauncher = "rofi -show drun"
myEmacs= "emacsclient -c -a 'emacs' "
myBrowser= "zen-browser"
soundDir = "~/Sound/"
volumeSound = soundDir + "ComputerErrorsoundeffect.mp4"
mySoundPlayer = "ffplay -nodisp -autoexit "
_NET_WM_STRUT_PARTIAL = 1

keys = [
    #Start_keys
    # Programs
    Key([mod], "d", lazy.spawn(myLauncher), desc="Launch program launcher"),
    Key([mod], "e", lazy.spawn(myEmacs), desc="Launch emacs"),
    Key([mod, "shift"], "Tab", lazy.spawn(myBrowser), desc="Launch web"),
    Key([mod, "shift"], "t", lazy.spawn("libreoffice"), desc="Launch LibreOffice"),
    Key([mod, "shift"], "f", lazy.spawn("pcmanfm"), desc="Launch filebrowser"),
    Key([mod], "f", lazy.spawn("discord"), desc="Launch Discord."),
    Key([mod], "Return", lazy.spawn(myTerm), desc="Launch Terminal."),

    #Keys for the scratchpad
    Key([mod, "shift"], "n", lazy.group["sp"].dropdown_toggle("nm"), desc="Launch Nm-connection-editor. An Network GUI manager"),
    Key([mod], "v", lazy.group["sp"].dropdown_toggle("audio"), desc="Launch Pavucontrol. An Volume GUI manager"),
    Key([mod], "b", lazy.group["sp"].dropdown_toggle("blue"), desc="Launch Bluetooth Gui."),
    Key([mod, "shift"], "b", lazy.group["sp"].dropdown_toggle("bit"), desc="Launch bitwarden."),

    # System
    Key([mod], "l", lazy.spawn("light-locker-command -l"), desc="Lock the computer"),
    Key([mod], "p", lazy.spawn(expanduser("~/Script/SkjermBilde.sh"), shell=True), desc="Take fullscreen screenshot"),
    Key([mod, "shift"], "p", lazy.spawn(expanduser("~/Script/Flameshot.sh"), shell=True), desc="Take region screenshot"),
    Key([mod], "BackSpace", lazy.spawn(expanduser("~/.config/rofi/Scripts/rofi-system-menu.sh"), shell=True), desc="Xmenu"),

    # Show keys and fish alias
    Key([mod, "shift"], "s", lazy.spawn(expanduser("~/.config/fish/alias.sh"), shell=True), desc="Show fish alias"),
    Key([mod], "s", lazy.spawn(expanduser("~/.config/qtile/Scripts/keys.sh"), shell=True), desc="Show keys"),

    # Qtile
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),

    # Window manage
    Key([mod], "g", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "h", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "u", lazy.layout.grow(), desc="Grow window to the left"),
    Key([mod], "i", lazy.layout.shrink(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),

    # Layouts
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between layouts",),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "space", lazy.layout.flip(), desc = "Switch window place"),
    Key([mod, "control"], "1", lazy.group.setlayout("monadtall"), desc = "Switch to layout MonadTall"),
    Key([mod, "control"], "2", lazy.group.setlayout("verticaltile"), desc = "Switch to layout VerticalTile"),
    Key([mod, "control"], "3", lazy.group.setlayout("monadwide"), desc = "Switch to layout MonadWide"),
    Key([mod, "control"], "4", lazy.group.setlayout("max"), desc = "Switch to layout Max"),

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
#End_keys
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
                        Match(wm_class="zen"),
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
    DropDown('nm', 'nm-connection-editor', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown('audio', 'pavucontrol', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown("blue", 'blueman-manager', width=0.4, x=0.3, y=0.2, opacity=1),
    DropDown("bit", 'bitwarden-desktop', width=0.4, x=0.3, y=0.2, opacity=1),
]))

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
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    layout.MonadTall(**layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.Zoomy(),
    layout.Max(),
]

widget_defaults = dict(
    font='Source Code Pro',
    fontsize = 11,
    margin_y = 3,
    margin_x = 4,
    padding_y = 2,
    padding_x = 3,
    padding= 5,
)
extension_defaults = widget_defaults.copy()

window_name = widget.WindowName()

def show_cpu():
    qtile.cmd_spawn('kitty -e htop')

def package():
    home = os.path.expanduser('~')
    qtile.cmd_spawn(home + '/.config/qtile/Scripts/AntallPakker.sh', shell=True)

def updates():
    qtile.cmd_spawn('kitty -e paru')

def cleandisk():
    #qtile.cmd_spawn('kitty -e sudo pacman -Rns $(pacman -Qtdq)')
    qtile.cmd_spawn('kitty -e sudo pacman -Sc')

def Pavucontrol():
    qtile.cmd_spawn('pavucontrol')

def xmenu():
    home = os.path.expanduser('~')
    qtile.cmd_spawn(home + '/.config/rofi/Scripts/rofi-system-menu.sh', shell=True)

#powerline = {
 #   "decorations": [
  #      PowerLineDecoration(path="arrow_right")
   # ]
#}

main_bar = bar.Bar(
    [
widget.Sep(
            background="#282a36",
            foreground="#282a36"),
        widget.Image(
            filename = '~/.config/qtile/icon/TobbeOS_logo_q.xpm',
            mouse_callbacks = {'Button1': xmenu},
            scale = False),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
        widget.GroupBox(
             fontsize = 11,
             margin_y = 3,
             margin_x = 4,
             padding_y = 2,
             padding_x = 3,
             borderwidth = 1,
             rounded = False,
             highlight_method="line",
             highlight_color = ["#282a36", "#44475a"],
             this_current_screen_border = '#44475a',
             active = "#8be9fd",
             inactive = "#ff79c6",
             disable_drag = True,
             use_mouse_wheel = False,
            ),
       widget.Spacer(lenght = 8),
       widget.GenPollCommand(
            cmd = 'uname -r',
            shell = True,
            foreground = '#bd93f9',
            font='Source Code Pro',
            update_interval = 5,
       ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.GenPollCommand(
            fmt = 'Installed:{}',
            cmd = '~/.config/qtile/Scripts/Packagecount.sh',
            shell = True,
            foreground = '#8be9fd',
            font='Source Code Pro',
            update_interval = 5,
            mouse_callbacks = {'Button1': package},
       ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.CheckUpdates(
            custom_command = 'checkupdates',
            distro = 'Arch',
            colour_have_updates = 'ff5555',
            colour_no_updates = '50fa7b',
            no_update_string = 'no updates',
            font='Source Code Pro',
            update_interval = 5,
            mouse_callbacks = {'Button1': updates},
       ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
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
            size_percent = 30),
       widget.DF(
            format = '{r: .0f}%',
            fmt = 'Used Disk:{}',
            warn_space = 40,
            visible_on_warn = False,
            warn_color = '#ff5555',
            partition = '/',
            foreground = '#6272a4',
            font='Source Code Pro',
            update_interval = 5,
            mouse_callbacks = {'Button1': cleandisk},
       ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.CPU(
            format = 'CPU: {load_percent}%',
            foreground = "#ff76c6",
            font='Source Code Pro',
            mouse_callbacks = {'Button1': show_cpu},
        ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.Memory(
            format = '{MemUsed: .0f}{mm}',
            fmt = 'Mem:{} used',
            foreground = '#ffb86c',
            font='Source Code Pro',
            mouse_callbacks = {'Button1': show_cpu},
        ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.Volume(
            fmt = 'Vol:{}',
            foreground = "#8be9fd",
            font='Source Code Pro',
            mouse_callbacks = {'Button1': Pavucontrol},
        ),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.Clock(format="%H:%M:%S", font='Source Code Pro'),
       widget.Sep(
            background = "#282a36",
            foreground = "#44475a",
            linewidth = 1,
            size_percent = 30),
       widget.Systray(),
       widget.Sep(
            foreground = "#282a36"),
       ], 30, background= "#282a36", foreground="#f8f8f2", font='Source Code Pro', fontsize=12)

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
        Match(wm_class="Bitwarden"),
        Match(wm_class="zenity"),
    ], **layout_theme
)
# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/Scripts/autostart.sh'])

wmname = "TobbeOS"
