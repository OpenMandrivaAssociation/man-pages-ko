%define LNG ko

Summary:	Korean(Hangul) Man Pages
Name:		man-pages-%{LNG}
Version:	20050219
Release:	17
License:	GPLv2
Group:		System/Internationalization
Url:		http://man.kldp.org/
Source0:	man-pages-%{LNG}-%{version}.tar.bz2
BuildArch:	noarch
BuildRequires:	man
Requires:	locales-%{LNG}
Requires:	man
Autoreqprov:	false

%description
Korean translation of the official manpages from LDP and
another useful manpages from various packages.
They're maintained by the Korean Manpage Project
<http://man.kldp.org>.

%prep
%setup -c %{name}-%{version}

%build

%install
mkdir -p %{buildroot}/%{_mandir}/%{LNG}/

for i in man?;do
        cp -adpvrf $i %{buildroot}/%{_mandir}/%{LNG}/
done

# those files conflict whith rpm package:
rm %{buildroot}/%{_mandir}/%{LNG}/man8/rpm{2cpio,}.8

# those files conflict whith man package:
rm %{buildroot}/%{_mandir}/%{LNG}/man{1/man.1,1/whatis.1,5/man.config.5}

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%{_mandir}/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}

touch %{buildroot}/var/cache/man/%{LNG}/whatis

%post
%create_ghostfile /var/cache/man/%{LNG}/whatis root root 644

%files
%dir %{_mandir}/%{LNG}
%dir /var/cache/man/%{LNG}
%ghost %config(noreplace) /var/cache/man/%{LNG}/whatis
%{_mandir}/%{LNG}/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
#%{_mandir}/%{LNG}/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

