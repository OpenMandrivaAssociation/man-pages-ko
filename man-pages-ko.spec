%define LNG ko
%define name man-pages-%LNG
%define version 20050219
%define release 13

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

LANG=%LNG DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_bindir}/mandb %_mandir/%LNG
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
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
#%_mandir/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 20050219-10mdv2011.0
+ Revision: 666373
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 20050219-9mdv2011.0
+ Revision: 609324
- rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 20050219-8mdv2011.0
+ Revision: 609306
- fix build
- fix typos
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 20050219-6mdv2009.1
+ Revision: 351581
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 20050219-5mdv2009.0
+ Revision: 223191
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 20050219-4mdv2008.1
+ Revision: 152966
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Jun 02 2007 Funda Wang <fwang@mandriva.org> 20050219-2mdv2008.0
+ Revision: 34679
- Fix conflict with man 1.6e

* Thu May 31 2007 Adam Williamson <awilliamson@mandriva.org> 20050219-1mdv2008.0
+ Revision: 33474
- rebuild for new era; drop /var/catman (wildly obsolete)
- new version 20050219


* Tue Feb 24 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.48-4mdk
- add conflict tag in order to force package ordering so that updates get
  performed smoother
- fix potential conflict with man (CFLO, not CFL)

* Sun Feb 15 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.48-3mdk
- fix conflict with latest man

* Thu May 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.48-2mdk
- fix conflict with rpm

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.48-1mdk
- new release

* Wed May 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-16mdk
- use new man-pages-LG template
    - don't rebuild whatis on install since
      - we've already build in package
      - cron will rebuild it nightly and so add other package french man pages
    - adapt to new man-pages-LG template
    - requires man => 1.5j-8mdk for new man-pages framework
    - remove old makewhatis.ko since default makewhatis is now able to parse
      non english man pages
    - use new std makewhatis to build whatis in spec and in cron entry 
    - whatis db goes into /var/cache/man (so enable ro /usr)
    - standard {Build,}Requires/buildroot/prereq/arc/provides/obsoletes

* Mon Mar 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-15mdk
- remove old pre-spec_helper comments
- 20010901 update
- license is now GPL
- fix description
- fix tarball without man-pages-ko directory
- add the url
- fix: all sections're filled now
- remove all comments warning than anybody was able to find where should
  come the updates
- fix %%clean to be forced

* Thu Mar 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-14mdk
- fix permission on /usr/share/man/id/*
- provides manpages-%%LANG
- don't overwrite crontab if user altered it

* Wed Mar 28 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-13mdk
- fix tmppath
- major update from debian
- fix makewhatis sp that it's works

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-12mdk
- BM

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-11mdk
- use mandir macro in order to be ok when switching to /usr/share/man as
  following FHS.

* Fri Mar 31 2000 Denis Havlik <denis@mandrakesoft.com> 1.1-10mdk
- convert to new group scheme
- convert books-ja.gif -> .xpm

* Fri Nov 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved makewhatis.ko from /usr/local/sbin to /usr/sbin

* Tue Jul 20 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- included some nice improvements from man-pages-pl

* Wed Jul 07 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- Adapted the rpm I had made to Mandrake style

