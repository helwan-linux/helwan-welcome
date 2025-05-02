# Maintainer: Erik Dubois <erik.dubois@gmail.com>
pkgname=helwan-welcome-app
_pkgname=helwan-welcome-app
_destname1="/etc/skel/.config/"
_destname2="/usr/"
#_licensedir="/usr/share/arcolinux/licenses/"
pkgver=1.1
pkgrel=01
pkgdesc="Welcome application for helwanlinux"
arch=('any')
url="https://github.com/helwan-linux/helwan-welcome"
license=('GPL3')
makedepends=('git')
depends=('python-pyqt5' 'gettext' 'libwnck3' 'arandr')
provides=("${pkgname}")
install='readme.install'
options=(!strip !emptydirs)
source=(${_pkgname}::"git+${url}")
sha256sums=('SKIP')
package() {
	install -dm755 ${pkgdir}${_licensedir}${_pkgname}
	install -m644  ${srcdir}/${_pkgname}/LICENSE ${pkgdir}${_licensedir}${_pkgname}
	mkdir -p "${pkgdir}${_destname1}"
	cp -r "${srcdir}/${_pkgname}/${_destname1}/"* "${pkgdir}${_destname1}"
	mkdir -p "${pkgdir}${_destname2}"
	cp -r "${srcdir}/${_pkgname}/${_destname2}/"* "${pkgdir}${_destname2}"
}
