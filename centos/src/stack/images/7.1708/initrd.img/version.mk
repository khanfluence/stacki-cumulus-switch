ORDER			= 99
PKGROOT			= /opt/stack/images
OVERLAY.PKGS = \
	glibc-common
OVERLAY.UPDATE.PKGS	= \
	foundation-python \
	ludicrous-speed \
	stack-command \
	stack-pylib \
	foundation-python-Flask \
		foundation-python-itsdangerous \
		foundation-python-Werkzeug \
		foundation-python-click \
		foundation-python-MarkupSafe \
		foundation-python-Jinja2 \
	foundation-python-PyMySQL \
	foundation-python-configparser \
	foundation-python-python-daemon \
		foundation-python-lockfile \
	foundation-python-requests \
		foundation-python-urllib3 \
		foundation-python-chardet \
		foundation-python-certifi \
		foundation-python-idna

