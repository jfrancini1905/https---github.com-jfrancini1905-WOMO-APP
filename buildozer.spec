[app]
# (bool) Indicate whether to use Android App Bundle (AAB) format (True) or APK (False)
android.use_aab = True

# (str) Title of your application
title = WoMo App

# (str) Package name
package.name = com.ausflug.WoMo

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ausflug

# (str) Source code directory (where the main.py file lives)
source.dir = .

# (list) Source file extensions to include in the package (let empty to include all)
source.include_exts = py,png,jpg,kv,atlas

# (str) python-for-android version to use (e.g., 'master')
p4a.version = master

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) Directories to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (str) Application version
version = 1.0.0

# (list) Application dependencies (comma separated)
requirements = python3,kivy

# (str) Presplash of the application (path to image)
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application (path to image)
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations (portrait, landscape, etc.)
orientation = portrait

#
# OSX Specific
#
osx.python_version = 3
osx.kivy_version = 1.9.1

#
# Android specific
#
fullscreen = 0

# (list) Permissions required for Android
# android.permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE

# (int) Target Android API level
#android.api = 31

# (int) Minimum API level your app supports
#android.minapi = 21

# (bool) Use private storage or not
#android.private_storage = True

# (str) Android SDK path (if empty, it will be automatically downloaded)
android.sdk_path =

# (bool) Automatically accept SDK license agreements
#android.accept_sdk_license = True

# (str) Android entry point (the activity to run)
android.entrypoint = org.kivy.android.PythonActivity

# (list) Additional permissions (like write external storage if needed)
#android.permissions = android.permission.WRITE_EXTERNAL_STORAGE

# (list) Android architectures to build for (arm64-v8a, armeabi-v7a, etc.)
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
#android.numeric_version = 1

# (bool) Enable auto backup feature (Android API >= 23)
android.allow_backup = True

# (str) Packaging format for release (AAB or APK)
android.release_artifact = aab

# (str) Packaging format for debug builds (APK)
android.debug_artifact = apk



#
# iOS specific
#
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the code (for iOS)
ios.codesign.allowed = false

# (str) The path to a custom kivy-ios folder if you have one
#ios.kivy_ios_dir = ../kivy-ios

# (bool) Whether or not to skip the byte compilation for Python files
#android.no-byte-compile-python = False

# (bool) Enable AndroidX support (if using dependencies that require it)
# android.enable_androidx = True

# (list) Android dependencies to add (e.g., Firebase or other Android libraries)
#android.gradle_dependencies =

# (list) Java files to include in the Android project (can be a directory of Java files)
#android.add_src =

# (list) List of additional Java .jar files to add to the Android project
#android.add_jars = foo.jar, bar.jar

# (list) Gradle repositories to use if needed
#android.add_gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"

# (list) Add packaging options if needed to avoid conflicts
#android.add_packaging_options = "exclude 'META-INF/*.kotlin_module'"

# (bool) Indicate whether the screen should stay on during app usage
#android.wakelock = False

# (str) Additional adb arguments if necessary (e.g., use a different adb server)
#android.adb_args = -H host.docker.internal

# (str) If using any additional libraries, specify their paths here
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so

# (list) Android application metadata (key=value format)
#android.meta_data =

# (list) Android library projects to add
#android.library_references =

# (list) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Enable a custom backup rule (see Android backup documentation)
#android.backup_rules =

#
# Buildozer specific settings
#
log_level = 2
warn_on_root = 1

# (str) Path to build artifact storage (build outputs)
#build_dir = ./.buildozer

# (str) Path to build output (e.g., APK or AAB files)
#bin_dir = ./bin

