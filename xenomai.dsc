#                                                                 -*-conf-*-
Format: 1.0
Source: xenomai
Binary: xenomai-runtime, xenomai-kernel-source, libxenomai1,
 libxenomai-dev, xenomai-doc
Architecture: amd64 arm armeb armel i386 powerpc armhf all
Version: 2.6.3-0.1mk~wheezy1
Maintainer: John Morris <john@zultron.com>
Homepage: http://www.xenomai.org/
Standards-Version: 3.9.3
Build-Depends: debhelper (>= 8), findutils (>= 4.2.28), autotools-dev,
 autoconf, automake, libtool
Package-List: 
 libxenomai-dev deb libdevel extra
 libxenomai1 deb libs extra
 xenomai-doc deb doc extra
 xenomai-kernel-source deb kernel extra
 xenomai-runtime deb devel extra
Files: 
 9f83c39cfb10535df6bf51702714e716 22289867 xenomai-2.6.3.tar.bz2
Debtransform-Tar: xenomai-2.6.3.tar.bz2
