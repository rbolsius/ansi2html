#    This file is part of ansi2html.
#    Copyright (C) 2012  Kuno Woudt <kuno@frob.nl>
#    Copyright (C) 2013  Sebastian Pipping <sebastian@pipping.org>
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see
#    <http://www.gnu.org/licenses/>.


class Rule(object):

    def __init__(self, klass, **kw):

        self.klass = klass
        self.kw = '; '.join([(k.replace('_', '-')+': '+kw[k])
                             for k in sorted(kw.keys())]).strip()
        self.kwl = [(k.replace('_', '-'), kw[k][1:])
                             for k in sorted(kw.keys())]

    def __str__(self):
        return '%s { %s; }' % (self.klass, self.kw)


def index(r, g, b):
    return str(16 + (r * 36) + (g * 6) + b)


def color(r, g, b):
    return "#%.2x%.2x%.2x" % (r * 42, g * 42, b * 42)


def level(grey):
    return "#%.2x%.2x%.2x" % (((grey * 10) + 8,) * 3)


def index2(grey):
    return str(232 + grey)

# http://en.wikipedia.org/wiki/ANSI_escape_code#Colors
SCHEME = {
    # black red green brown/yellow blue magenta cyan grey/white
    'ansi2html': (
        "#000316", "#aa0000", "#00aa00", "#aa5500",
        "#0000aa", "#E850A8", "#00aaaa", "#F5F1DE",
        "#7f7f7f", "#ff0000", "#00ff00", "#ffff00",
        "#5c5cff", "#ff00ff", "#00ffff", "#ffffff"),

    'xterm': (
        "#000000", "#cd0000", "#00cd00", "#cdcd00",
        "#0000ee", "#cd00cd", "#00cdcd", "#e5e5e5",
        "#7f7f7f", "#ff0000", "#00ff00", "#ffff00",
        "#5c5cff", "#ff00ff", "#00ffff", "#ffffff"),

    'osx': (
        "#000000", "#c23621", "#25bc24", "#adad27",
        "#492ee1", "#d338d3", "#33bbc8", "#cbcccd") * 2,

    # http://ethanschoonover.com/solarized
    'solarized': (
        "#262626", "#d70000", "#5f8700", "#af8700",
        "#0087ff", "#af005f", "#00afaf", "#e4e4e4",
        "#1c1c1c", "#d75f00", "#585858", "#626262",
        "#808080", "#5f5faf", "#8a8a8a", "#ffffd7"),

    'mint-terminal': (
        "#2E3436", "#CC0000", "#4E9A06", "#C4A000",
        "#3465A4", "#75507B", "#06989A", "#D3D7CF",
        "#555753", "#EF2929", "#8AE234", "#FCE94F",
        "#729FCF", "#AD7FA8", "#34E2E2", "#EEEEEC"),

    'nightshade-vivid': (
        "#222222", "#9C574F", "#358F57", "#E7AF57",
        "#317CB5", "#8F5F8F", "#4FAAA2", "#BABAA0",
        "#6F6F67", "#DC7363", "#9FEA5F", "#E0D35F",
        "#5FA6EF", "#BC7BAC", "#7BDCD2", "#DCDCD0"),

    'nightshade': (
        "#222222", "#BF7A70", "#7F9F7F", "#DFAF8F",
        "#6092BF", "#A87390", "#72AEB0", "#BABAA0",
        "#878780", "#CC9393", "#C5D47F", "#F0DCA5",
        "#6092BF", "#BF86A5", "#8CD0D3", "#DCDCD0"),

    'daylight': (
        "#000000", "#9B2F23", "#208020", "#E2951D",
        "#0F57A0", "#833B70", "#2C9093", "#777777",
        "#6F6F67", "#D7372D", "#7DC215", "#CFB700",
        "#1685FF", "#BF56A6", "#37BFC2", "#FFFFFF"),

    }


def get_styles(dark_bg=True, scheme='ansi2html'):

    css = [
        Rule('pre, code, tt', font_family='"DejaVu Sans Mono", "Bitstream Vera Sans Mono", Consolas, monospace', font_size='12px'),
        Rule('.ansi2html-content', white_space='pre-wrap', word_wrap='break-word', display='inline'),
        Rule('.body_foreground', color=('#222222', '#DCDCD0')[dark_bg]),
        Rule('.body_background', background_color=('#DCDCD0', '#222222')[dark_bg]),
        Rule('.body_foreground > .bold,.bold > .body_foreground, body.body_foreground > pre > .bold',
             color=('#222222', '#FFFFFF')[dark_bg], font_weight=('bold', 'normal')[dark_bg]),
        Rule('.inv_foreground', color=('#222222', '#DCDCD0')[not dark_bg]),
        Rule('.inv_background', background_color=('#DCDCD0', '#222222')[not dark_bg]),
        Rule('.ansi1', font_weight='bold'),
        Rule('.ansi2', font_weight='lighter'),
        Rule('.ansi3', font_style='italic'),
        Rule('.ansi4', text_decoration='underline'),
        Rule('.ansi5', text_decoration='blink'),
        Rule('.ansi6', text_decoration='blink'),
        Rule('.ansi8', visibility='hidden'),
        Rule('.ansi9', text_decoration='line-through'),
        ]

    # set palette
    pal = SCHEME[scheme]
    for _index in range(8):
        css.append(Rule('.ansi3%s' % _index, color=pal[_index]))
        css.append(Rule('.inv3%s' % _index, background_color=pal[_index]))
        # Code 1 (bold or increased intensity) is generally rendered in most
        # terminals using the brighter colors from the range 8-15
        css.append(Rule('.ansi3%s.ansi1' % _index, color=pal[_index + 8], font_weight='normal'))
    for _index in range(8):
        css.append(Rule('.ansi4%s' % _index, background_color=pal[_index]))
        css.append(Rule('.inv4%s' % _index, color=pal[_index]))

    # set palette colors in 256 color encoding
    pal = SCHEME[scheme]
    for _index in range(len(pal)):
        css.append(Rule('.ansi38-%s' % _index, color=pal[_index]))
        css.append(Rule('.inv38-%s' % _index, background_color=pal[_index]))
    for _index in range(len(pal)):
        css.append(Rule('.ansi48-%s' % _index, background_color=pal[_index]))
        css.append(Rule('.inv48-%s' % _index, color=pal[_index]))

    # css.append("/* Define the explicit color codes (obnoxious) */\n\n")

    for green in range(0, 6):
        for red in range(0, 6):
            for blue in range(0, 6):
                css.append(Rule(".ansi38-%s" % index(red, green, blue),
                                color=color(red, green, blue)))
                css.append(Rule(".inv38-%s" % index(red, green, blue),
                                background=color(red, green, blue)))
                css.append(Rule(".ansi48-%s" % index(red, green, blue),
                                background=color(red, green, blue)))
                css.append(Rule(".inv48-%s" % index(red, green, blue),
                                color=color(red, green, blue)))

    for grey in range(0, 24):
        css.append(Rule('.ansi38-%s' % index2(grey), color=level(grey)))
        css.append(Rule('.inv38-%s' % index2(grey), background=level(grey)))
        css.append(Rule('.ansi48-%s' % index2(grey), background=level(grey)))
        css.append(Rule('.inv48-%s' % index2(grey), color=level(grey)))

    return css
