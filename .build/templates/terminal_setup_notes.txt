
'''
We want to use the weaver fab lib to run a basic install, on my
laptop, of the terminal settings defined in here.

I have a libary of functions in fedorafab, that I can use to write
files to the (remote) laptop, and also setup and configure as needed.

Its all here bar the fat lady singing.

'''


BASE_TMPL = '''
!-------------------------------------------------------------------------------
! Xft settings
!-------------------------------------------------------------------------------

Xft.dpi:                    96
Xft.antialias:              false
Xft.rgba:                   rgb
Xft.hinting:                true
Xft.hintstyle:              hintslight

!-------------------------------------------------------------------------------
! URxvt settings
! Colours lifted from Solarized (http://ethanschoonover.com/solarized)
! More info at:
! http://pod.tst.eu/http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.1.pod
!-------------------------------------------------------------------------------

URxvt.depth:                32
URxvt.geometry:             90x30
URxvt.transparent:          false
URxvt.fading:               0
! URxvt.urgentOnBell:         true
! URxvt.visualBell:           true
URxvt.loginShell:           true
URxvt.saveLines:            50
URxvt.internalBorder:       3
URxvt.lineSpace:            0

! Fonts
URxvt.allow_bold:           false
/* URxvt.font:                 -*-terminus-medium-r-normal-*-12-120-72-72-c-60-iso8859-1 */
URxvt*font: -*-terminus-*-*-*-*-32-*-*-*-*-*-*-*
URxvt*boldFont: -*-terminus-*-*-*-*-32-*-*-*-*-*-*-*

! Fix font space
URxvt*letterSpace: -1

! Scrollbar
URxvt.scrollStyle:          rxvt
URxvt.scrollBar:            false

! Perl extensions
URxvt.perl-ext-common:      default,matcher
URxvt.matcher.button:       1
URxvt.urlLauncher:          firefox

! Cursor
URxvt.cursorBlink:          true
URxvt.cursorColor:          #657b83
URxvt.cursorUnderline:      false

! Pointer
URxvt.pointerBlank:         true

!!Source http://github.com/altercation/solarized

*background: #002b36
*foreground: #657b83
!!*fading: 40
*fadeColor: #002b36
*cursorColor: #93a1a1
*pointerColorBackground: #586e75
*pointerColorForeground: #93a1a1

!! black dark/light
*color0: #073642
*color8: #002b36

!! red dark/light
*color1: #dc322f
*color9: #cb4b16

!! green dark/light
*color2: #859900
*color10: #586e75

!! yellow dark/light
*color3: #b58900
*color11: #657b83

!! blue dark/light
*color4: #268bd2
*color12: #839496

!! magenta dark/light
*color5: #d33682
*color13: #6c71c4

!! cyan dark/light
*color6: #2aa198
*color14: #93a1a1

!! white dark/light
*color7: #eee8d5
*color15: #fdf6e3

'''
from . import fedorafab
from .fedorafab import run, sudo

__all__ = ['install_termandemacs',]

def install_termandemacs():
    setup_xterm()
    install_terminal()
    install_fonts()
    install_emacs()
    setup_emacs()


def install_emacs():
    """
    """
    sudo("dnf install -y %s " % 'emacs')

def setup_emacs():
    """
    """
    emacs_tmpl = '''
;; fonts etc
;; I set .Xresources to have an arrary of colours, which emacs picks up by
;; default, so I am not, for now, using an emacs theme.
(set-default-font "Droid Sans Mono-24")

;; Start up options
;; do not show the intro screen in split
(setq inhibit-startup-screen t)
;; start in full screen mode. I do not have a tiling WM, and I mostly work
;; on a laptop. Want a new screen, Alt-tab.
(add-to-list 'default-frame-alist '(fullscreen . maximized)) 
;; Only one window on startup
(add-hook 'emacs-startup-hook 'delete-other-windows t)

;; Future changes
;; https://www.emacswiki.org/emacs/PythonProgrammingInEmacs
; ropemacs, flycheck, pylint
;; all goals to get to a robust dev env.

;; Make PRIMARY selection (mouse highlight in terminal usually) 
;;; paste-able with SHIFT INSERT
;; C-W / C-Y still uses clipboard
(setq select-enable-primary `t)
;; (it used to be x-select-enable-primary but changed on emacs 25 and 
;; the internet has not caught up yet.)


    '''
    remote_path = '/home/pbrian/.emacs.d/init.el'
    fedorafab.replace_remote_file(remote_path, emacs_tmpl)
    
def setup_xterm():
    """xrdb is of course and X program so needs to display out to a DISPLAY. 
    I fake one, in the same env as the call is made
    I prob need to look at env var in fabric
    """
    remote_path = '/home/pbrian/.Xresources'
    fedorafab.replace_remote_file(remote_path, BASE_TMPL)
    run('export DISPLAY=:0;xrdb {0} > /dev/null;echo $DISPLAY'.format(remote_path))

def install_terminal():
    """
    Using uxrvt
    """
    pkgs = ['rxvt-unicode-256color',
            'xorg-x11-apps']
    for pkg in pkgs:
        sudo("dnf install -y %s " % pkg)

def setup_term():
    """We want to have the nice perl extensions
    """
    pass 
        
def install_fonts():
    """
    I want to install inconsolata or similar
    """
    
    sudo("yum install -y levien-inconsolata-fonts.noarch")
    sudo("yum install -y google-droid-sans-mono-fonts.noarch")
    sudo("fc-cache -fv") # refresh the cache of fonts    

# set up bash config
def setup_bash():
    """
    """
    #set emacs for most command line usage
    #export VISUAL="emacs"
    #export EDITOR="$VISUAL"
    #export GIT_EDITOR="$VISUAL" 
    pass


    
# install python3
# sudo apt-get install python3 python3-pip
# install python from apt ????
# from source, but ??? wheels first...
