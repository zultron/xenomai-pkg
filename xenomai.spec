%global _includedir	/usr/include/xenomai/

Summary: Real-time development framework
Name: xenomai
Version: 2.6.3
Release: 4%{?dist}
License: GPL
Group: System Tools
Source0: http://download.gna.org/xenomai/stable/xenomai-%{version}.tar.bz2
Source1: README.developers
Source2: xenomai.init
Source3: xenomai.systemd
Source4: xenomai.default
Source5: xenomai-gid-ctl
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gcc doxygen make tetex texlive-latex
URL: http://xenomai.org/

%description

Xenomai is a real-time development framework cooperating with the
Linux kernel, in order to provide a pervasive, interface-agnostic,
hard real-time support to user-space applications, seamlessly
integrated into the GNU/Linux environment.


%package devel
Summary: Libraries, includes, etc. to develop Xenomai applications
Group: Development/Libraries
Requires: gcc
Requires: pkgconfig
Requires: xenomai = %{version}-%{release}

%description devel

Xenomai is a real-time development framework cooperating with the
Linux kernel, in order to provide a pervasive, interface-agnostic,
hard real-time support to user-space applications, seamlessly
integrated into the GNU/Linux environment.

%prep
%setup -q

%build
%configure \
    --enable-x86-tsc \
    --with-testdir=%{_libdir}/xenomai
# this is very broken on el6
#    --enable-dox-doc \

# fix doxygen file
(cd doc/doxygen && doxygen -u Doxyfile-common)

make
#make %{_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}

make install-user DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# all docs currently going into -devel pkg
mv $RPM_BUILD_ROOT%{_docdir}/%{name} \
    $RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

# copy examples
cp -a examples \
   $RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
cp ksrc/nucleus/udev/*.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

# init/unit scripts
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/default
cp %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/default/xenomai
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}
%if 0%{?fedora} >= 18
# systemd
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/xenomai.service
%else
# chkconfig
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/xenomai
%endif

# install sources to patch kernel
mkdir -p $RPM_BUILD_ROOT%{_usrsrc}/xenomai
cp -a ksrc include scripts $RPM_BUILD_ROOT%{_usrsrc}/xenomai/


%clean
rm -fr $RPM_BUILD_ROOT

%preun
%if 0%{?fedora} >= 18
  %systemd_preun xenomai.service
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/chkconfig --del xenomai &> /dev/null || :
fi
%endif

%post
/sbin/ldconfig
%if 0%{?fedora} >= 18
  %systemd_post xenomai.service
%else
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add xenomai &> /dev/null || :
fi
%endif

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc %{_mandir}/man1/*.gz
%{_libdir}/lib*.so.*
%{_libdir}/lib*.so
%{_libdir}/posix.wrappers
%{_libdir}/xenomai
%{_bindir}/*
%{_sbindir}/*
%{_sysconfdir}/udev/rules.d/*
%if 0%{?fedora} >= 18
%{_unitdir}/xenomai.service
%else
%{_initrddir}/xenomai
%endif
%config(noreplace) %{_sysconfdir}/default/xenomai

%files devel
%defattr(-, root, root)
%doc %{_docdir}/%{name}-devel-%{version}
%{_libdir}/lib*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_usrsrc}/xenomai


%changelog
* Sun Jan  5 2014 John Morris <john@zultron.com> - 2.6.3-5
- Update system initialization scripts:
  - Add systemd unit for Fedora 17+
  - Add xenomai-gid-ctl script and default file
  - Update sysv init to use gid-ctl script
  - Update %%post/%%preun scripts

* Mon Dec 23 2013 John Morris <john@zultron.com> - 2.6.3-4
- Don't disable FORTIFY_SOURCE; fixed with 2.6.3

* Sun Dec 22 2013 John Morris <john@zultron.com> - 2.6.3-3
- Fix xenomai service start/stop ordering

* Fri Dec 20 2013 John Morris <john@zultron.com> - 2.6.3-2
- Fix -devel pkg dependency

* Fri Dec  6 2013 John Morris <john@zultron.com> - 2.6.3-1
- New upstream release
- Upstream removed prepare-patch script; follow Debian example
  for -devel package

* Sun Nov 17 2013 John Morris <john@zultron.com> - 2.6.2.1-2
- Remove Requires: xenomai from -devel pkg

* Thu Jan 17 2013 John Morris <john@zultron.com> - 2.6.2.1-1
- Update to 2.6.2.1, the 2.6.2 re-release
- Use 'make install-user' to avoid /dev packaging problems
- Remove %%pre script to creat /dev entries; udev works fine

* Thu Jan 10 2013 John Morris <john@zultron.com> - 2.6.2-0.el6
- Update to v2.6.2
- Add xenomai patch to -devel pkg
- Move whole docdir to -devel pkg (really needs to be split up)
- Add examples directory to docdir
- Fix testdir location
- Root out %%makeinstall ugliness
- Disable broken doxygen
- Undefine _FORTIFY_SOURCE in compile, and add README.developers
- Add init script
- Formatting fixes

* Wed Nov  8 2012 John Morris <john@zultron.com> - 2.6.0-5.el6
- Fix syntax error in %%pre script

* Wed Nov  7 2012 John Morris <john@zultron.com> - 2.6.0-4.el6
- Add --enable-dlopen-skins flag to ./configure

* Mon Nov  5 2012 John Morris <john@zultron.com> - 2.6.0-3.el6
- fix make install problems:
-   add patch to prevent /dev node creation
-   create needed /dev entries in %%pre script
-   install udev rules files

* Sat Nov  3 2012 John Morris <john@zultron.com> - 2.6.0-2.el6
- inherit RPM with no changelog, no credits from mirrors.ysn.ru
- fix make install problems:  set make install variables on command line
- fix up %%docs


