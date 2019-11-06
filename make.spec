Name:		make
Epoch: 		1
Version:	4.2.1
Release:        11
Summary:	A tool which controls the generation of executables and non-source files of a program
License:	GPLv3+
URL:		http://www.gnu.org/software/make/
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2

Patch0:         make-4.0-newlines.patch
Patch1:         make-4.0-noclock_gettime.patch
Patch2:         make-4.0-weird-shell.patch
Patch3:         make-4.2-getcwd.patch
Patch4:         make-4.2-j8k.patch
Patch5:         make-4.2.1-glob-fix-2.patch
Patch6:         make-4.2.1-glob-fix.patch
Patch7:         make-4.2.1-glob-fix-3.patch
Patch8:         make-4.2.1-test-driver.patch

Patch6000:      src-makeint.h-Use-pid_t-to-store-PIDs-of-int.patch
Patch6001:      Queue-failed-fork-etc.-to-be-handled-like-any-other-.patch
Patch6002:      src-job.c-reap_children-Fix-inverted-win-lose-messag.patch
Patch6003:      SV-54233-Preserve-higher-command_state-values-on-als.patch
Patch6004:      src-main.c-main-Set-jobserver-permissions-before-re-.patch
Patch6005:      main.c-main-SV-48274-Allow-j-in-makefile-MAKEFLAGS-v.patch

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
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
#rm -f tests/scripts/features/parallelism.orig

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
/usr/bin/env LANG=C make check && true

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
* Wed Oct 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:4.2.1-11
- Package init
