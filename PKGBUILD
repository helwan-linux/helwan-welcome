# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>
pkgname=hel-welcome-app
_pkgname=hel-welcome-app
pkgver=4
pkgrel=00
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

    # تثبيت مجلد التطبيق بالكامل إلى /usr/share
    install -Dm755 -d "$pkgdir/usr/share/helwan-welcome-app"
    cp -r "${srcdir}/${_pkgname}/usr/share/helwan-welcome-app/" "$pkgdir/usr/share/"
    
  # تثبيت الملف التنفيذي (سكربت بايثون) في المسار الصحيح
  install -Dm755 "${srcdir}/${_pkgname}/usr/share/helwan-welcome-app/helwan-welcome-app.py" "$pkgdir/usr/bin/helwan-welcome-app"

  # إنشاء مجلد تطبيقات إذا لم يكن موجودًا
  install -dm755 "$pkgdir/usr/share/applications"

  # تثبيت ملف .desktop في المسار الصحيح
  install -Dm644 "${srcdir}/${_pkgname}/usr/share/applications/helwan-welcome-app.desktop" "$pkgdir/usr/share/applications/helwan-welcome-app.desktop"

  # إنشاء مجلد أيقونات التطبيقات القابلة للتطوير إذا لم يكن موجودًا
  install -dm755 "$pkgdir/usr/share/icons/hicolor/scalable/apps"
  install -dm755 "$pkgdir/usr/share/icons/hicolor/512x512/apps"

  # تثبيت ملفات الأيقونة في المسارات الصحيحة
  find "${srcdir}/${_pkgname}/usr/share/hicolor" -name "helwan-welcom.*" -print0 | while IFS= read -r -d $'\0' file; do
    if [[ "$(basename "$file")" == "helwan-welcom.svg" ]]; then
      install -Dm644 "$file" "$pkgdir/usr/share/icons/hicolor/scalable/apps/helwan-welcome.svg"
    elif [[ "$(basename "$file")" == "helwan-welcom.png" ]]; then
      install -Dm644 "$file" "$pkgdir/usr/share/icons/hicolor/512x512/apps/helwan-welcome.png"
    fi
  done

  # نسخ ملفات الترجمة إذا كانت موجودة
find "${srcdir}/${_pkgname}/usr/share/helwan-welcome-app/locales" -name "base.mo" -print0 | while IFS= read -r -d $'\0' file; do
  lang_dir=$(basename "$(dirname "$(dirname "$file")")")
  install -Dm644 "$file" "$pkgdir/usr/share/locale/$lang_dir/LC_MESSAGES/base.mo"
done

  # نسخ أي ملفات ترخيص أخرى بشكل صحيح
  install -dm755 "$pkgdir/usr/share/licenses/${pkgname}"
  install -Dm644 "${srcdir}/${_pkgname}/LICENSE" "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
}
