# We install firefox, directly from Mozilla (not from snap)
RUN     \
        echo "Install Firefox from Mozilla" >&2               \
        && apt-get update                                     \
        && add-apt-repository ppa:mozillateam/ppa             \
        && printf '\nPackage: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority:          1001\n' > /etc/apt/preferences.d/mozilla-firefox                     \
        && printf 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:              ${distro_codename}";' > /etc/apt/apt.conf.d/51unattended-upgrades-firefox \
        && apt-get update                                     \
        && apt-get install -y firefox --no-install-recommends \
        && apt-get clean                                      \
        && apt-get autoremove -y                              \
        && rm -rf /tmp/* /var/tmp/*                           \
        && rm -rf /var/lib/apt/lists/* /var/cache/apt/*       \
        && echo "Install Firefox from Mozilla OK" >&2


