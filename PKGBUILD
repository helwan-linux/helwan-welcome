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
	# تثبيت الرخصة
	install -dm755 "${pkgdir}${_licensedir}${pkgname}"
	install -m644 "${srcdir}/${_pkgname}/LICENSE" "${pkgdir}${_licensedir}${pkgname}/LICENSE"

	# نسخ مجلد usr بالكامل كما هو
	cp -r "${srcdir}/${_pkgname}/usr/"* "${pkgdir}/usr/"

	# نسخ ملفات الإعدادات الافتراضية (لو موجودة)
	if [ -d "${srcdir}/${_pkgname}/.config" ]; then
		install -dm755 "${pkgdir}/etc/skel/.config"
		cp -r "${srcdir}/${_pkgname}/.config/"* "${pkgdir}/etc/skel/.config/"
	fi
}
