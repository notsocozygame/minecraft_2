[app]
title = Minecraft 2 Java Edition
package.name = minecraft2
package.domain = com.notsocozygames

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1
requirements = python3,kivy,ursina

orientation = landscape
fullscreen = 1

android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
