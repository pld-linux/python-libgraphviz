Summary:	Python 2 binding for graphviz
Summary(pl.UTF-8):	Wiązania Pythona 2 dla graphviza
Name:		python-libgraphviz
Version:	2.47.2
Release:	7
License:	EPL v1.0
Group:		Libraries
#Source0Download: https://graphviz.org/download/source/
Source0:	https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/%{version}/graphviz-%{version}.tar.xz
# Source0-md5:	4b60526ed7a6a43dfb23b5c175286cd8
Patch14:	python-paths.patch
Patch17:	cppflags.patch
URL:		http://www.graphviz.org/
BuildRequires:	ann-devel
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	bison >= 3.0
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flex >= 2.5.2
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gawk
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-tools
BuildRequires:	ghostscript-devel
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	gts-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libltdl-devel >= 2:2.2
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pango-devel >= 1:1.14.9
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.021
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 1.3
BuildRequires:	swig-python >= 1.3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	graphviz-libs >= %{version}
Obsoletes:	graphviz-python < 2.26.3-1
Obsoletes:	python-graphviz < 2.44.1-10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 binding for graphviz.

%description -l pl.UTF-8
Wiązania Pythona 2 dla graphviza.

%prep
%setup -q -n graphviz-%{version}
%patch14 -p1
%patch17 -p1

%{__sed} -i -e '1s,/usr/bin/python$,%{__python},' tclpkg/gv/demo/modgraph.py

%build
touch config/config.rpath
%{__libtoolize} --ltdl
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

CPPFLAGS="%{rpmcppflags}"
export CPPFLAGS

%configure \
%ifarch %{x8664} aarch64 ppc64 sparc64 s390x
	LIBPOSTFIX="64" \
%endif
%ifarch x32
	LIBPOSTFIX="x32" \
%endif
	ac_cv_lib_criterion_main=no \
	--disable-go \
	--disable-guile \
	--disable-java \
	--disable-ltdl-install \
	--disable-lua \
	--disable-ocaml \
	--disable-perl \
	--disable-php \
	--disable-python \
	--disable-python3 \
	--disable-r \
	--disable-ruby \
	--disable-sharp \
	--disable-tcl \
	--disable-silent-rules \
	--disable-static \
	--without-devil \
	--without-ghostscript \
	--without-ipsepcola \
	--without-lasi \
	--without-libgd \
	--without-poppler \
	--without-qt \
	--without-rsvg \
	--without-smyrna \
	--without-visio \
	--without-webp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_mandir}/man3/gv.3python $RPM_BUILD_ROOT%{_mandir}/man3/gv_python2.3

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/graphviz
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/graphviz/lib*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/graphviz/python2/*.la
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/lib*.pc
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/graphviz/{demo,doc,graphs,gvpr,lefty}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{cdt,cgraph,expr,gvc,gvpr,pack,pathplan,xdot}.3
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man7/graphviz.7

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/graphviz/python2
%attr(755,root,root) %{_libdir}/graphviz/python2/libgv_python2.so
%attr(755,root,root) %{_libdir}/graphviz/python2/_gv.so
%{_libdir}/graphviz/python2/gv.py
%attr(755,root,root) %{py_sitedir}/_gv.so
%{py_sitedir}/gv.py
%{_mandir}/man3/gv_python2.3*
