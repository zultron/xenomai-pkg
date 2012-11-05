%define dist .el6

%define _includedir	/usr/include/xenomai/

Summary: Real-time development framework
Name: xenomai
Version: 2.6.0
Release: 3%{?dist}
License: GPL
Group: System Tools
Source: http://download.gna.org/xenomai/stable/xenomai-%{version}.tar.bz2
# Stop make install from creating device nodes in /dev
Patch0:    xenomai-2.6.0-install_fixes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gcc doxygen make tetex texlive-latex
URL: http://xenomai.org/

%description
Xenomai is a real-time development framework cooperating with the Linux kernel,
in order to provide a pervasive, interface-agnostic, hard real-time support
to user-space applications, seamlessly integrated into the GNU/Linux environment.


%package devel
Summary: Libraries, includes, etc. to develop Xenomai applications
Group: Development/Libraries
Requires: xenomai = %{version}-%{release}
Requires: gcc
Requires: pkgconfig

%description devel
Xenomai is a real-time development framework cooperating with the Linux kernel,
in order to provide a pervasive, interface-agnostic, hard real-time support
to user-space applications, seamlessly integrated into the GNU/Linux environment.

%prep
%setup -q
%patch0 -p1 -z .install_fixes

%build
%configure \
    --enable-x86-tsc \
    --enable-dox-doc

# fix doxygen file
(cd $RPM_BUILD_DIR/xenomai-%{version}/doc/doxygen && doxygen -u Doxyfile-common)
make
#make %{_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}

%makeinstall \
        testdir=$RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

cp $RPM_BUILD_DIR/xenomai-%{version}/src/testsuite/xeno-test/xeno-test-run $RPM_BUILD_ROOT%{_bindir}/
mv $RPM_BUILD_ROOT%{_docdir}/%{name} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
cp ksrc/nucleus/udev/*.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d


%clean
rm -fr $RPM_BUILD_DIR

%pre
# create device nodes removed from make install
for ent in `seq 0 31`; do
    test -e /dev/rtp${ent} || mknod -m 0666 /dev/rtp${ent} c 150 ${ent}
fi
test -e /dev/rtheap || mknod -m 666 /dev/rtheap c 10 254

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc %{_mandir}/man1/*.gz
%{_datadir}/xenomai/*
%{_libdir}/lib*.so.*
%{_libdir}/lib*.so
%{_libdir}/posix.wrappers
%{_bindir}/*
%{_sbindir}/*

%files devel
%defattr(-, root, root)
%doc examples
%doc %{_datadir}/doc/xenomai-%{version}/html
%doc %{_datadir}/doc/xenomai-%{version}/pdf
%doc %{_datadir}/doc/xenomai-%{version}/txt
%{_libdir}/lib*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Nov  5 2012 John Morris <john@zultron.com> - 2.6.0-3.el6
- fix make install problems:
-   add patch to prevent /dev node creation
-   create needed /dev entries in %%pre script

* Sat Nov  3 2012 John Morris <john@zultron.com> - 2.6.0-2.el6
- inherit RPM with no %%changelog, no credits from mirrors.ysn.ru
- fix make install problems:  set make install variables on command line
- fix up %%docs


