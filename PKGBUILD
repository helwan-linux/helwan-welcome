# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>
pkgname=helwan-welcome-app
_pkgname=helwan-welcome-app
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

	# نسخ جميع ملفات بايثون إلى مجلد التطبيق
	cp -r "${srcdir}/${_pkgname}/*.py" "${pkgdir}/usr/share/${pkgname}/"

	# إنشاء مجلد للموارد (sources) ونسخها
	install -dm755 "${pkgdir}/usr/share/${pkgname}/sources"
	cp -r "${srcdir}/${_pkgname}/sources/"* "${pkgdir}/usr/share/${pkgname}/sources/"

	# إنشاء مجلد للترجمات (locales) ونسخها
	install -dm755 "${pkgdir}/usr/share/${pkgname}/locales"
	cp -r "${srcdir}/${_pkgname}/locales/"* "${pkgdir}/usr/share/${pkgname}/locales/"

	# نسخ ملف التشغيل الرئيسي (main.py) بشكل منفصل للتأكد من وجوده
	install -Dm644 "${srcdir}/${_pkgname}/main.py" "${pkgdir}/usr/share/${pkgname}/main.py"

	# نسخ ملف .desktop إلى المكان الصحيح
	install -Dm644 "${srcdir}/${_pkgname}/helwan_welcome.desktop" "${pkgdir}/usr/share/applications/helwan_welcome.desktop"

	# نسخ ملفات الإعدادات الافتراضية (إذا كانت موجودة)
	if [ -d "${srcdir}/${_pkgname}/.config" ]; then
		install -dm755 "${pkgdir}/etc/skel/.config"
		cp -r "${srcdir}/${_pkgname}/.config/"* "${pkgdir}/etc/skel/.config/"
	fi
}
