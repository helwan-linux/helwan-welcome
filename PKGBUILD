# Maintainer: Saeed Badrelden <saeedbadrelden2021@example.com>
pkgname=helwan-welcome
pkgver=1.0
pkgrel=1
pkgdesc="A welcome application for Helwan Linux"
arch=('any')
url="https://github.com/helwan-linux/helwan-welcome"
license=('GPL3')
depends=('python' 'python-pyqt5' 'python-pillow')
makedepends=('git' 'gettext')

source=("git+https://github.com/helwan-linux/helwan-welcome.git?depth=1")
sha256sums=('SKIP')

prepare() {
  cd "${srcdir}/${pkgname}"
  # إزالة CRLF لو موجود
  find . -type f -exec sed -i 's/\r$//' {} +
}

build() {
  cd "${srcdir}/${pkgname}"
  python -m compileall .
}

package() {
  cd "${srcdir}/${pkgname}"

  # تثبيت ملف البرنامج الرئيسي
  install -Dm755 welcome.py "${pkgdir}/usr/bin/helwan-welcome"

  # تثبيت الشعار
  install -Dm644 sources/logo.png "${pkgdir}/usr/share/pixmaps/helwan-welcome.png"

  # تثبيت ملف التطبيق .desktop
  install -Dm644 helwan-welcome.desktop "${pkgdir}/usr/share/applications/helwan-welcome.desktop"

  # تثبيت ملفات الترجمة (دومين اسمه helwan-welcome)
  find locales -name "*.mo" | while read -r mo_file; do
    lang_dir=$(dirname "${mo_file}" | sed 's|locales/||')
    install -Dm644 "${mo_file}" "${pkgdir}/usr/share/locale/${lang_dir}/LC_MESSAGES/helwan-welcome.mo"
  done

  # إضافة التطبيق إلى autostart لكل المستخدمين
  install -Dm644 helwan-welcome.desktop "${pkgdir}/etc/xdg/autostart/helwan-welcome.desktop"
}

