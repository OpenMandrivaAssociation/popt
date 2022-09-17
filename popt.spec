# popt is used by gstreamer, gstreamer is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define dev32name %mklib32name %{name} -d

#define beta rc1

# popt is built as a static library - can't have compiler specific bits
# (such as LLVM bytecode or GIMPLE representations) inside the .o files
%define _disable_lto 1

Summary:	C library for parsing command line parameters
Name:		popt
Epoch:		1
Version:	1.19
Release:	1
License:	MIT
Group:		System/Libraries
Url:		https://rpm.org/
Source0:	http://ftp.rpm.org/popt/releases/%{?beta:testing/}%{!?beta:popt-%(echo %{version}|cut -d. -f1).x/}popt-%{version}%{?beta:-%{beta}}.tar.gz
Source1:	%{name}.rpmlintrc
BuildRequires:	gettext

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
Provides:	%{name} = %{EVRD}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	%{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
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

%if %{with compat32}
%package -n	%{lib32name}
Summary:	Main %{name} library (32-bit)
Group:		System/Libraries
Requires:	%{name}-data = %{EVRD}
BuildRequires:	libc6

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	%{dev32name}
Summary:	Development headers and libraries for %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n	%{dev32name}
This package contains the header files and libraries needed for
developing programs using the %{name} library.
%endif

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:-%{beta}}
export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 --enable-static --disable-rpath
cd ..
%endif

mkdir build
cd build
%configure --enable-static --disable-rpath

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%find_lang %{name}

%files -n %{libname}
%{_libdir}/libpopt.so.%{major}*

%files -n %{devname}
%{_includedir}/popt.h
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/libpopt.a
%{_libdir}/libpopt.so
%{_mandir}/man3/popt.3*

%files data -f %{name}.lang

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libpopt.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/popt.pc
%{_prefix}/lib/libpopt.a
%{_prefix}/lib/libpopt.so
%endif
