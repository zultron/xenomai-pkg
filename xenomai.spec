%define dist .el6

%define _includedir	/usr/include/xenomai/

Summary: Real-time development framework
Name: xenomai
Version: 2.6.0
Release: 2%{?dist}
License: GPL
Group: System Tools
Source: http://download.gna.org/xenomai/stable/xenomai-%{version}.tar.bz2
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

%build
%configure \
    --enable-x86-tsc \
    --enable-dox-doc

# fix doxygen file
(cd $RPM_BUILD_DIR/xenomai-%{version}/doc/doxygen && doxygen -u Doxyfile-common)
make
#make %{_smp_mflags}

%install
rm -fr %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_includedir}

%makeinstall \
        testdir=$RPM_BUILD_ROOT%{_bindir} \
        sudo=
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cp -r $RPM_BUILD_DIR/xenomai-%{version}/examples $RPM_BUILD_ROOT%{_datadir}/doc/xenomai/
cp $RPM_BUILD_DIR/xenomai-%{version}/src/testsuite/xeno-test/xeno-test-run $RPM_BUILD_ROOT%{_bindir}/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xenomai/ $RPM_BUILD_ROOT%{_datadir}/doc/xenomai-%{version}

%clean
rm -fr %{buildroot}

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
%{_datadir}/doc/xenomai-%{version}/examples/*
%{_datadir}/doc/xenomai-%{version}/html/*
%{_datadir}/doc/xenomai-%{version}/pdf/*
%{_datadir}/doc/xenomai-%{version}/txt/*
%{_libdir}/lib*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Nov  3 2012 John Morris <john@zultron.com> - 2.6.0-2.el6
- set make install variables on command line to fix errors
-   $testdir, $sudo

