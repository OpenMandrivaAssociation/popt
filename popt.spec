%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:	4
Epoch:		1
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
Patch0:		popt-1.16-pkgconfig-libdir.patch
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
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	%{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	libpopt-devel = %{EVRD}

%description -n	%{devname} 
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package -n	%{name}-data
Summary:	Data files for %{name}
Group:		System/Libraries

%description -n	popt-data
This package contains popt data files like locales.

%prep
%setup -q
%patch0 -p1 -b .pkglib64~
autoreconf -f

%build
%configure2_5x	--disable-rpath

%make

%install
%makeinstall_std
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/lib%{name}.so.%{major}* %{buildroot}/%{_lib}
ln -sf /%{_lib}/lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

%find_lang %{name}

%files -n %{libname}
%doc README CHANGES
/%{_lib}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/lib%{name}*a
%{_libdir}/lib%{name}.so
%{_mandir}/man3/popt.*

%files -n %{name}-data -f %{name}.lang
