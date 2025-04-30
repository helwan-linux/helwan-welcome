# Maintainer: Saeed Badrelden <saeedbadrelden2021@example.com>
pkgname=helwan-welcome
pkgver=1.0 # أو أي إصدار مناسب
pkgrel=1
pkgdesc="A welcome application for Helwan Linux"
arch=('any')
url="https://github.com/helwan-linux/helwan-welcome"
license=('GPL3') # تأكد من أن هذا هو الترخيص الصحيح
depends=('python-tkinter' 'python-pillow' 'python-gettext')
makedepends=('git')
conflicts=()
replaces=()
backup=()

source=("git+https://github.com/helwan-linux/helwan-welcome.git#tag=v${pkgver}?depth=1") # استخدم التاج المناسب أو commit
sha256sums=('SKIP') # سيتم حسابه لاحقًا

pkgver() {
  cd "${pkgname}"
  printf "%s" "$(git describe --tags --always)"
}

build() {
  cd "${srcdir}/${pkgname}"
  python -m compileall .
}

package() {
  cd "${srcdir}/${pkgname}"
  install -Dm755 welcome.py "${pkgdir}/usr/bin/helwan-welcome"
  install -Dm644 sources/logo.png "${pkgdir}/usr/share/pixmaps/helwan-welcome.png"
  install -Dm644 helwan-welcome.desktop "${pkgdir}/usr/share/applications/helwan-welcome.desktop"

  # تثبيت ملفات الترجمة
  find locales -name "*.mo" -exec install -Dm644 {} "${pkgdir}/usr/share/locale/{}/LC_MESSAGES/base.mo" \;
}