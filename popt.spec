%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define devel_name %mklibname %{name} -d

Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:	%mkrel 1
Epoch:		1
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
Patch0:		popt-1.16-pkgconfig-libdir.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package -n	%{lib_name}
Summary:	Main %{name} library
Group:		System/Libraries
Requires:	%{name}-data = %{epoch}:%{version}
Provides:	%{name} = %{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	%{devel_name}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{lib_name} = %{epoch}:%{version}
Requires:	%{lib_name} >= 1:1.15-8
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	libpopt-devel = %{epoch}:%{version}-%{release}

%description -n	%{devel_name} 
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
rm -rf %{buildroot}
%makeinstall_std
mkdir -p %{buildroot}/%{_lib}
pushd %{buildroot}/%{_libdir}/
mv lib%{name}.so.%{lib_major}* %{buildroot}/%{_lib}
ln -sf ../../%{_lib}/lib%{name}.so.%{lib_major}.* lib%{name}.so
popd
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%doc README CHANGES
/%{_lib}/lib%{name}.so.%{lib_major}*

%files -n %{devel_name}
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/lib%{name}*a
%{_libdir}/lib%{name}.so
%{_mandir}/man3/popt.*

%files -n %{name}-data -f %{name}.lang
%defattr(-,root,root)
