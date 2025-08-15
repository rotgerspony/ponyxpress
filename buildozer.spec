
[app]
title = PonyXpress
package.name = ponyxpress
package.domain = org.ponyxpress
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,android
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.minapi = 21
android.sdk = 30
android.ndk = 21b
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
