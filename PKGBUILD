# Maintainer: Saeed Badrelden <saeedbadrelden2021@example.com>
pkgname=helwan-welcome
pkgver=1.0
pkgrel=1
pkgdesc="A welcome application for Helwan Linux"
arch=('any')
url="https://github.com/helwan-linux/helwan-welcome"
license=('GPL3')
depends=('python-tkinter' 'python-pillow' 'python-gettext')
makedepends=('git')

source=("git+https://github.com/helwan-linux/helwan-welcome.git#tag=v${pkgver}?depth=1")
sha256sums=('SKIP')

build() {
  cd "${srcdir}/${pkgname}"
  python -m compileall .
}

package() {
  cd "${srcdir}/${pkgname}"
  install -Dm755 welcome.py "${pkgdir}/usr/bin/helwan-welcome"
  install -Dm644 sources/logo.png "${pkgdir}/usr/share/pixmaps/helwan-welcome.png"
  install -Dm644 helwan-welcome.desktop "${pkgdir}/usr/share/applications/helwan-welcome.desktop"

  # Install translation files
  find locales -name "*.mo" | while read -r mo_file; do
    lang_dir=$(dirname "${mo_file}" | sed 's|locales/||')
    install -Dm644 "${mo_file}" "${pkgdir}/usr/share/locale/${lang_dir}/LC_MESSAGES/helwan-welcome.mo"
  done

  # Move the desktop entry to autostart for automatic startup
  install -Dm644 "${srcdir}/${pkgname}/helwan-welcome.desktop" "${pkgdir}/home/$USER/.config/autostart/helwan-welcome.desktop"
}
