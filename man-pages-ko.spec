%define LNG ko
%define name man-pages-%LNG
%define version 20050219
%define release %mkrel 10

Summary: Korean(Hangul) Man Pages
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System/Internationalization
URL: http://man.kldp.org/
Source: man-pages-%LNG-%version.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.6
Requires: locales-%LNG, man => 1.6
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
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/%LNG/

for i in man?;do
        cp -adpvrf $i %{buildroot}/%_mandir/%LNG/
done


# those files conflict whith rpm package:
rm %{buildroot}/%_mandir/%LNG/man8/rpm{2cpio,}.8

# those files conflict whith man package:
rm %{buildroot}/%_mandir/%LNG/man{1/man.1,1/whatis.1,5/man.config.5}

LANG=%LNG DESTDIR=%{buildroot} %{_sbindir}/makewhatis %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_sbindir}/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%_mandir/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
