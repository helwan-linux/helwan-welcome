# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>
pkgname=hel-welcome-app
_pkgname=hel-welcome-app
_licensedir='/usr/share/licenses/'
pkgver=2
pkgrel=04
pkgdesc="Welcome application for helwanlinux"
arch=('any')
url="https://github.com/helwan-linux/helwan-welcome"
license=('GPL3')
conflicts=('helwan-welcome-app')
makedepends=('git')
depends=('python-pyqt5' 'gettext' 'libwnck3' 'arandr')
provides=("${pkgname}")
install='readme.install'
options=(!strip !emptydirs)
source=(${_pkgname}::"git+${url}")
sha256sums=('SKIP')

package() {
	install -dm755 "${pkgdir}${_licensedir}${pkgname}"
	install -m644 "${srcdir}/${_pkgname}/LICENSE" "${pkgdir}${_licensedir}${pkgname}/LICENSE"

	# إنشاء مجلد لتطبيق الترحيب
	install -dm755 "${pkgdir}/usr/share/${pkgname}"

	# نسخ كل ملفات بايثون لمجلد التطبيق
	cp -r "${srcdir}/${_pkgname}/*.py" "${pkgdir}/usr/share/${pkgname}/"

	# إنشاء مجلد للموارد (sources) ونسخه
	install -dm755 "${pkgdir}/usr/share/${pkgname}/sources"
	cp -r "${srcdir}/${_pkgname}/sources/"* "${pkgdir}/usr/share/${pkgname}/sources/"

	# إنشاء مجلد للترجمات (locales) ونسخه
	install -dm755 "${pkgdir}/usr/share/${pkgname}/locales"
	cp -r "${srcdir}/${_pkgname}/locales/"* "${pkgdir}/usr/share/${pkgname}/locales/"

	# نسخ ملف التشغيل الرئيسي (main.py) لوحده عشان نتأكد إنه موجود
	install -Dm644 "${srcdir}/${_pkgname}/main.py" "${pkgdir}/usr/share/${pkgname}/main.py"

	# نسخ ملف .desktop للمكان الصح
	install -Dm644 "${srcdir}/${_pkgname}/helwan_welcome.desktop" "${pkgdir}/usr/share/applications/helwan_welcome.desktop"

	# إضافة سكريبت لتشغيل التطبيق في /usr/bin
	install -Dm755 /dev/stdin "${pkgdir}/usr/bin/hel-welcome-app" << EOF
#!/bin/bash
exec python3 /usr/share/${pkgname}/main.py
EOF

	# نسخ ملفات الإعدادات الافتراضية (لو موجودة)
	if [ -d "${srcdir}/${_pkgname}/.config" ]; then
		install -dm755 "${pkgdir}/etc/skel/.config"
		cp -r "${srcdir}/${_pkgname}/.config/"* "${pkgdir}/etc/skel/.config/"
	fi
}
