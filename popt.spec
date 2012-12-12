%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%bcond_without	uclibc

Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:	8
Epoch:		1
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
Patch0:		popt-1.16-pkgconfig-libdir.patch
Patch1:		popt-1.16-remove-dead-autofoo-crap.patch
BuildRequires:	gettext
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-16
%endif

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package -n	%{libname}
Summary:	Main %{name} library
Group:		System/Libraries
Requires:	%{name}-data = %{EVRD}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	uclibc-%{libname}
Summary:	Main %{name} library (uClibc linked)
Group:		System/Libraries
Requires:	%{name}-data = %{EVRD}

%description -n uclibc-%{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	%{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname} 
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package	data
Summary:	Data files for %{name}
Group:		System/Libraries
BuildArch:	noarch

%description	data
This package contains popt data files like locales.

%prep
%setup -q
%patch0 -p1 -b .pkglib64~
%patch1 -p1 -b .autocrap~
autoreconf -f

%build
CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
		--disable-rpath
%make
popd
%endif

mkdir -p system
pushd system
%configure2_5x	--disable-rpath
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
mkdir -p %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libpopt.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -srf %{buildroot}%{uclibc_root}/%{_lib}/libpopt.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libpopt.so

rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
%endif

%makeinstall_std -C system
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libpopt.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libpopt.so.%{major}.* %{buildroot}%{_libdir}/libpopt.so

%find_lang %{name}

%files -n %{libname}
%doc README CHANGES
/%{_lib}/libpopt.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%doc README CHANGES
%{uclibc_root}/%{_lib}/libpopt.so.%{major}*
%endif

%files -n %{devname}
%{_includedir}/popt.h
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/libpopt.a
%{_libdir}/libpopt.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpopt.a
%{uclibc_root}%{_libdir}/libpopt.so
%endif
%{_mandir}/man3/popt.3*

%files data -f %{name}.lang

%changelog
* Wed Dec 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.16-8
- rebuild on ABF

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.16-7
+ Revision: 820560
- fix dep on uclibc linked library for real

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.16-6
+ Revision: 820460
- fix missing epoch in dependency issue

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.16-5
+ Revision: 820387
- cleanups
- do uclibc build
- make popt-data package noarch

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.16-4
+ Revision: 782613
- drop excessive provides
- use %%{EVRD} macro
- apply some cosmetics

* Mon Dec 05 2011 Zé <ze@mandriva.org> 1.16-3
+ Revision: 737838
- clean defattr, BR, clean setion and mkrel
- needs gettext
- clean dub require

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.16-2
+ Revision: 667804
- mass rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - ship CHANGES with docs

* Mon Dec 13 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.16-1mdv2011.0
+ Revision: 620656
- new release: 1.16
- only install dynamic library under /%%{_lib}, keep the rest in %%{_libdir}

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.15-10mdv2011.0
+ Revision: 607190
- rebuild

* Tue Feb 16 2010 Funda Wang <fwang@mandriva.org> 1.15-9mdv2010.1
+ Revision: 506724
- hard require libpackage release to prevent inexistent target

* Tue Feb 16 2010 Frederic Crozat <fcrozat@mandriva.com> 1.15-8mdv2010.1
+ Revision: 506600
- Move library to /lib(64), fixes Mdv bug #57649 (done in Fedora since 2007)

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.15-7mdv2010.0
+ Revision: 425086
- rebuild

* Sun Jun 28 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.15-6mdv2010.0
+ Revision: 390234
- disable rpath
- fix muxture of tabs and spaces

* Fri Jun 26 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.15-5mdv2010.0
+ Revision: 389422
- add missing Provides: in devel package

* Thu Jun 25 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.15-4mdv2010.0
+ Revision: 389007
- Add missing provides (neeeded by drakconf)

* Wed Jun 24 2009 Funda Wang <fwang@mandriva.org> 1.15-3mdv2010.0
+ Revision: 388832
- fix requires on epoch

* Wed Jun 24 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.15-2mdv2010.0
+ Revision: 388822
- Set epoch since libpopt0 from rpm 4.4 had an epoch set to 1

* Mon Jun 15 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.15-1mdv2010.0
+ Revision: 386017
- import popt
