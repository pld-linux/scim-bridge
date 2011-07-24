#
# Conditional build:
%bcond_with	qt3		# don't build qt3 input module
%bcond_without	qt4		# don't build qt4 input module
#
Summary:	SCIM Bridge Gtk IM module
Name:		scim-bridge
Version:	0.4.16
Release:	0.1
License:	GPLv2+ or LGPLv2+
Group:		Libraries
URL:		http://www.scim-im.org/projects/scim_bridge
Source0:	http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
# Source0-md5:	0011b178c4a0d2b0de26e7a14545323c
Patch0:		%{name}-fix-gdm.patch
Patch1:		%{name}-hotkey-help.patch
Patch2:		%{name}-bz461373.patch
Patch3:		%{name}-EOF.patch
Patch4:		%{name}-fix-gtk-key-snooper.patch
Patch5:		%{name}-fixes-null-imengine.patch
Patch6:		%{name}-ac.patch
%{?with_qt3:BuildRequires:	qt-devel}
%if %{with qt4}
BuildRequires:	qt4-qmake
BuildRequires:	QtGui-devel
%endif
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	scim-devel >= 1.4.6
Requires:	scim >= 1.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SCIM Bridge is a C implementation of a Gtk IM module for SCIM.

%package gtk2
Summary:	SCIM Bridge Gtk+2 IM module
Group:		Libraries
Requires(post):	gtk+2
Requires(postun):	gtk+2
# need %{_bindir}/scim-bridge
Requires:	%{name} = %{version}-%{release}

%description gtk2
This package provides the SCIM Bridge GTK+2 input method module.

%package qt
Summary:	SCIM Bridge Qt IM module
Group:		Libraries
# need %{_bindir}/scim-bridge
Requires:	%{name} = %{version}-%{release}

%description qt
This package provides the SCIM Bridge Qt input method module.

%package qt3
Summary:	SCIM Bridge Qt3 IM module
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description qt3
This package provides the SCIM Bridge Qt3 input method module.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--%{?with_qt3:en}%{!?with_qt3:dis}able-qt3-immodule \
	--%{?with_qt4:en}%{!?with_qt4:dis}able-qt4-immodule \
	--disable-documents

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/%{_libdir}/gtk-2.0/*/immodules/*.{la,a}
%{?with_qt3:%{__rm} $RPM_BUILD_ROOT%{_libdir}/qt-3.3/plugins/*/*.{la,a}}
%{?with_qt4:%{__rm} $RPM_BUILD_ROOT%{_libdir}/qt4/plugins/*/*.{la,a}}

%clean
rm -rf $RPM_BUILD_ROOT

%post gtk2
%if "%{_lib}" != "lib"
%{_bindir}/gtk-query-immodules-2.0-64 > %{_sysconfdir}/gtk64-2.0/gtk.immodules
%else
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%postun gtk2
%if "%{_lib}" != "lib"
%{_bindir}/gtk-query-immodules-2.0-64 > %{_sysconfdir}/gtk64-2.0/gtk.immodules
%else
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING doc
%attr(755,root,root) %{_bindir}/scim-bridge

%files gtk2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gtk-2.0/*/immodules/im-scim-bridge.so

%if %{with qt4}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/inputmethods/*.so
%endif

%if %{with qt3}
%files qt3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt-3.3/plugins/inputmethods/*.so
%endif
