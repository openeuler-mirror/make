Name:		make
Epoch: 		1
Version:	4.3
Release:        3
Summary:	A tool which controls the generation of executables and non-source files of a program
License:	GPLv3+
URL:		http://www.gnu.org/software/make/
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Patch0:         make-4.3-weird-shell.patch
Patch1:         make-4.3-j8k.patch
%ifarch riscv64
Patch50001:     fix-57962.patch
%endif

BuildRequires:	gcc git autoconf automake procps
BuildRequires:	guile-devel perl-interpreter make
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
GNU Make is a tool which controls the generation of executables and other
non-source files of a program from the program's source files.

Make gets its knowledge of how to build your program from a file called
the makefile, which lists each of the non-source files and how to compute
it from other files. When you write a program, you should write a makefile
for it, so that it is possible to use Make to build and install the program.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
touch configure aclocal.m4 Makefile.in

%configure --with-guile
%make_build

%install
%make_install
ln -sf make %{buildroot}/%{_bindir}/gmake
ln -sf make.1 %{buildroot}/%{_mandir}/man1/gmake.1
rm -f %{buildroot}/%{_infodir}/dir

%find_lang %name

%check
# check will fail if running the test with -j2
# http://savannah.gnu.org/bugs/?func=detailitem&item_id=53152
if [ "%{_smp_mflags}" = "-j2" ]; then
    echo "test will fail with make -j2 check"
else
/usr/bin/env LANG=C make check
fi

%post
if [ -f %{_infodir}/make.info.gz ]; then
    /sbin/install-info %{_infodir}/make.info.gz %{_infodir}/dir --entry="* Make: (make). The GNU make utility." || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/make.info.gz ]; then
        /sbin/install-info --delete %{_infodir}/make.info.gz %{_infodir}/dir --entry="* Make: (make). The GNU make utility." || :
    fi
fi

%files -f %{name}.lang
%license COPYING AUTHORS
%doc README
%{_bindir}/*
%{_includedir}/*

%files devel
%{_includedir}/*

%files help
%doc NEWS 
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Thu Mar 24 2022 jingwiw <ixoote@gmail.com> - 1:4.3-3
- fix bug #57962

* Tue Sep 8 2020 wangchen <wangchen137@huawei.com> - 1:4.3-2
- Modify the URL of Source0

* Tue Jul 28 2020 wangchen <wangchen137@huawei.com> - 1:4.3-1
- Update to 4.3

* Mon Feb 24 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:4.2.1-15
- Revise requires of make-devel

* Tue Feb 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:4.2.1-14
- Avoid the build failure of test suite that caused by -j2

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:4.2.1-13
- Resolve compile problems.

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:4.2.1-12
- Delete redundant files

* Wed Oct 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:4.2.1-11
- Package init
