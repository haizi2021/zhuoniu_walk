# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile


-optimizationpasses 5
-dontskipnonpubliclibraryclasses
-dontskipnonpubliclibraryclassmembers
-dontpreverify
-dontoptimize
-verbose
-ignorewarning
-keepattributes Exceptions,SourceFile,LineNumberTable

-flattenpackagehierarchy 'com.daily.horoscope'
-allowaccessmodification

-dontwarn butterknife.internal.*
-dontwarn com.google.common.*
-dontwarn com.makeramen.*

-keep public class * extends android.app.Activity
-keep public class * extends android.app.Application
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver
-keep public class * extends android.content.ContentProvider
-keep public class * extends android.app.backup.BackupAgentHelper
-keep public class * extends android.preference.Preference
-keep public class * extends android.view.View
-keep public class * extends android.graphics.drawable.Drawable

-keepclasseswithmembers class * {
    public <init>(android.content.Context, android.util.AttributeSet);
}

-keepclasseswithmembers class * {
    public <init>(android.content.Context, android.util.AttributeSet, int);
}

-keep class * implements java.io.Serializable {
  public *;
}

-keepnames class com.photolab.camera.preference.MultiProcessSharedPreferences$* {
    public <fields>;
    public <methods>;
}

#<!--使用JNI类不混淆-->
-keepclasseswithmembernames class * {native <methods>;}

#Android查询与清理系统缓存相关aidl  不混淆
-keep class android.content.pm.** {*;}

#守护进程
-keep class com.superpro.daemon.NativeDaemonBase{*;}
-keep class com.superpro.daemon.nativ.NativeDaemonAPI21{*;}
-keep class com.superpro.daemon.DaemonApplication{*;}
-keep class com.superpro.daemon.BootCompleteReceiver{*;}