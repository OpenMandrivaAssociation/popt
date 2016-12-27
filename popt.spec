%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

# popt is built as a static library - can't have compiler specific bits
# (such as LLVM bytecode or GIMPLE representations) inside the .o files
%define _disable_lto 1

# (tpg) optimize it a bit
%global optflags -O3

Summary:	C library for parsing command line parameters
Name:		popt
Epoch:		1
Version:	1.16
Release:	26
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		popt-1.16-pkgconfig-libdir.patch
Patch1:		popt-1.16-remove-dead-autofoo-crap.patch
Patch2:		popt-1.16-automake-1.13.patch
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

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
%configure --enable-static --disable-rpath
%make

%install
%makeinstall_std
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libpopt.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libpopt.so.%{major}.* %{buildroot}%{_libdir}/libpopt.so

%find_lang %{name}

%files -n %{libname}
/%{_lib}/libpopt.so.%{major}*

%files -n %{devname}
%{_includedir}/popt.h
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/libpopt.a
%{_libdir}/libpopt.so
%{_mandir}/man3/popt.3*

%files data -f %{name}.lang
