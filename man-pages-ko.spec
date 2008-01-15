%define LANG ko
%define name man-pages-%LANG
%define version 20050219
%define release %mkrel 3

Summary: Korean(Hangul) Man Pages
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System/Internationalization
URL: http://man.kldp.org/
Source: man-pages-%LANG-%version.tar.bz2
Buildroot: %_tmppath/%name-root
BuildRequires: man => 1.6
Requires: locales-%LANG, man => 1.6
Autoreqprov: false
BuildArchitectures: noarch

%description
Korean translation of the official manpages from LDP and
another useful manpages from various packages.
They're maintained by the Korean Manpage Project
<http://man.kldp.org>.

%prep
%setup -c %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/%LANG/

for i in man?;do
        cp -adpvrf $i $RPM_BUILD_ROOT/%_mandir/%LANG/
done


# those files conflict whith rpm package:
rm $RPM_BUILD_ROOT/%_mandir/%LANG/man8/rpm{2cpio,}.8

# those files conflict whith man package:
rm $RPM_BUILD_ROOT/%_mandir/%LANG/man{1/man.1,1/whatis.1,5/man.config.5}

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
/%_mandir/%LANG/man*
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron
