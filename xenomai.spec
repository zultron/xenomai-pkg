%global _includedir	/usr/include/xenomai/

# Undefine _FORTIFY_SOURCE cflag; breaks (at least) regression tests
# http://www.xenomai.org/pipermail/xenomai/2013-January/027341.html
# http://www.xenomai.org/pipermail/xenomai/2013-January/027342.html
%global __global_cflags %{__global_cflags} -Wp,-U_FORTIFY_SOURCE

Summary: Real-time development framework
Name: xenomai
Version: 2.6.2.1
Release: 1%{?dist}
License: GPL
Group: System Tools
Source0: http://download.gna.org/xenomai/stable/xenomai-%{version}.tar.bz2
Source1: README.developers
Source2: xenomai.init
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
Requires: xenomai = %{version}-%{release}
Requires: gcc
Requires: pkgconfig

%description devel

Xenomai is a real-time development framework cooperating with the
Linux kernel, in order to provide a pervasive, interface-agnostic,
hard real-time support to user-space applications, seamlessly
integrated into the GNU/Linux environment.

Developers should read %{_docdir}/%{name}-devel-%{version} for
important information about packaging Xenomai-enabled applications.

%prep
%setup -q

%build
%configure \
    --enable-x86-tsc \
    --enable-dlopen-skins \
    --with-testdir=%{_libdir}/xenomai
# this is very broken on el6
#    --enable-dox-doc \

# prepare patch
bash scripts/prepare-patch.sh x86

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

# include warning about _FORTIFY_SOURCE for developers
# hopefully this can be removed when upstream fixes the problem
cp %{SOURCE1} $RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

# copy examples
cp -a examples \
   $RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
cp ksrc/nucleus/udev/*.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
cp %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/xenomai

# install patches
mkdir -p $RPM_BUILD_ROOT%{_usrsrc}/xenomai
for i in ksrc/arch/x86/patches/*ipipe-*.patch; do
    PATCHNAME=$(basename $i)
    cp $i $RPM_BUILD_ROOT%{_usrsrc}/xenomai/$PATCHNAME
    cat xenomai_all.patch >> $RPM_BUILD_ROOT%{_usrsrc}/xenomai/$PATCHNAME
done

%clean
rm -fr $RPM_BUILD_ROOT

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/chkconfig --del xenomai &> /dev/null || :
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add xenomai &> /dev/null || :
fi

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
%{_initrddir}/xenomai

%files devel
%defattr(-, root, root)
%doc %{_docdir}/%{name}-devel-%{version}
%{_libdir}/lib*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_usrsrc}/xenomai


%changelog
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


