#
# Conditional build:
%bcond_without	qt3		# don't build qt3 input module
%bcond_without	qt4		# don't build qt4 input module
#
Summary:	SCIM Bridge GTK+ IM module
Summary(pl.UTF-8):	Moduł IM GTK+ SCIM Bridge
Name:		scim-bridge
Version:	0.4.16
Release:	1
License:	GPL v2+ or LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
# Source0-md5:	0011b178c4a0d2b0de26e7a14545323c
Patch0:		%{name}-fix-gdm.patch
Patch1:		%{name}-hotkey-help.patch
Patch2:		%{name}-bz461373.patch
Patch3:		%{name}-EOF.patch
Patch4:		%{name}-fix-gtk-key-snooper.patch
Patch5:		%{name}-fixes-null-imengine.patch
Patch6:		%{name}-ac.patch
Patch7:		%{name}-qt3.patch
URL:		http://www.scim-im.org/projects/scim_bridge
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gdk-pixbuf2-devel >= 2.4.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pango-devel >= 1:1.1.0
%{?with_qt3:BuildRequires:	qt-devel >= 3.3}
BuildRequires:	scim-devel >= 1.4.6
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	qt4-qmake >= 4
%endif
Requires:	scim >= 1.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SCIM Bridge is a C implementation of a GTK+ IM module for SCIM.

%description -l pl.UTF-8
SCIM Bridge to implementacja w C modułu IM GTK+ dla SCIM-a.

%package gtk2
Summary:	SCIM Bridge GTK+ 2.x IM module
Summary(pl.UTF-8):	Moduł IM GTK+ 2.x SCIM Bridge
Group:		Libraries
Requires(post,postun):	gtk+2
# need %{_bindir}/scim-bridge
Requires:	%{name} = %{version}-%{release}

%description gtk2
This package provides the SCIM Bridge GTK+ 2.x input method module.

%description gtk2 -l pl.UTF-8
Ten pakiet udostępnia moduł metody wprowadzania znaków GTK+ 2.x SCIM
Bridge.

%package qt
Summary:	SCIM Bridge Qt 4.x IM module
Summary(pl.UTF-8):	Moduł IM Qt 4.x SCIM Bridge
Group:		Libraries
# need %{_bindir}/scim-bridge
Requires:	%{name} = %{version}-%{release}
Requires:	QtGui >= 4

%description qt
This package provides the SCIM Bridge Qt 4.x input method module.

%description qt -l pl.UTF-8
Ten pakiet udostępnia moduł metody wprowadzania znaków Qt 4.x SCIM
Bridge.

%package qt3
Summary:	SCIM Bridge Qt 3.x IM module
Summary(pl.UTF-8):	Moduł IM Qt 3.x SCIM Bridge
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt >= 3.3

%description qt3
This package provides the SCIM Bridge Qt 3.x input method module.

%description qt3 -l pl.UTF-8
Ten pakiet udostępnia moduł metody wprowadzania znaków Qt 3.x SCIM
Bridge.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p0
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-documents \
	%{!?with_qt3:--disable-qt3-immodule} \
	%{!?with_qt4:--disable-qt4-immodule}

%{__make} \
	qt3moduledir=%{_libdir}/qt/plugins-mt/inputmethods

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	qt3moduledir=%{_libdir}/qt/plugins-mt/inputmethods

%{__rm} $RPM_BUILD_ROOT/%{_libdir}/gtk-2.0/*/immodules/*.{la,a}
%{?with_qt3:%{__rm} $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/inputmethods/*.{la,a}}
%{?with_qt4:%{__rm} $RPM_BUILD_ROOT%{_libdir}/qt4/plugins/inputmethods/*.{la,a}}

%clean
rm -rf $RPM_BUILD_ROOT

%post gtk2
%if "%{_lib}" == "lib64"
%{_bindir}/gtk-query-immodules-2.0-64 > %{_sysconfdir}/gtk64-2.0/gtk.immodules
%else
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%postun gtk2
%if "%{_lib}" == "lib64"
%{_bindir}/gtk-query-immodules-2.0-64 > %{_sysconfdir}/gtk64-2.0/gtk.immodules
%else
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog doc/{developer,user}
%attr(755,root,root) %{_bindir}/scim-bridge

%files gtk2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gtk-2.0/*/immodules/im-scim-bridge.so

%if %{with qt4}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/inputmethods/im-scim-bridge.so
%endif

%if %{with qt3}
%files qt3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt/plugins-mt/inputmethods/im-scim-bridge.so
%endif
