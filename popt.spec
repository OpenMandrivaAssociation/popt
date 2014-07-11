%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%bcond_without	uclibc

Summary:	C library for parsing command line parameters
Name:		popt
Epoch:		1
Version:	1.16
Release:	19
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
Patch0:		popt-1.16-pkgconfig-libdir.patch
Patch1:		popt-1.16-remove-dead-autofoo-crap.patch
Patch2:		popt-1.16-automake-1.13.patch
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
%apply_patches
autoreconf -fi

%build
CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure --enable-static --disable-rpath
%make
popd
%endif

mkdir -p system
pushd system
%configure --enable-static --disable-rpath
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

