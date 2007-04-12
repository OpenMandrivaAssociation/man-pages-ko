%define LANG ko

Summary: Korean(Hangul) Man Pages
Name: man-pages-%LANG
Version: 1.48
Release: 4mdk
License: GPL
Group: System/Internationalization
URL: http://man.kldp.org/
Source: man-pages-%LANG-%version.tar.bz2
Icon: books-%LANG.xpm
Buildroot: %_tmppath/%name-root
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG, man => 1.5j-8mdk
Prereq: sed grep man
Autoreqprov: false
BuildArchitectures: noarch
Obsoletes: man-%LANG, manpages-%LANG
Provides: man-%LANG, manpages-%LANG
Conflicts: man < 1.5m2

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
mkdir -p $RPM_BUILD_ROOT/var/catman/%LANG/cat{1,2,3,4,5,6,7,8,9,n}

for i in man?;do
        cp -adpvrf $i $RPM_BUILD_ROOT/%_mandir/%LANG/
done


# those files conflict whith rpm package:
rm $RPM_BUILD_ROOT/%_mandir/%LANG/man8/rpm{2cpio,}.8

# those files conflict whith man package:
rm $RPM_BUILD_ROOT/%_mandir/%LANG/man{1/man.1,5/man.config.5}

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory /%_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
       rm -rf /var/catman/%LANG
   fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
/%_mandir/%LANG/man*
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron

