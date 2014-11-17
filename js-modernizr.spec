# TODO:
# - minify
%define		pkgname	modernizr
Summary:	JavaScript library allowing you to use CSS3 & HTML5 while maintaining control over unsupported browsers
Name:		js-%{pkgname}
Version:	2.8.3
Release:	0.1
License:	BSD and MIT
Group:		Applications/WWW
Source0:	https://github.com/Modernizr/Modernizr/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5be0fb2dd7e291e30cb5abe79bbadccf
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://modernizr.com/
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
JavaScript library to detect HTML5 and CSS3 features in the user's
browser Modernizr is a JavaScript library allowing you to use HTML5 &
CSS3 while maintaining control over unsupported browsers.

Modernizr tests which native CSS3 and HTML5 features are available in
the current user agent and makes the results available to you in two
ways, as properties on a global `Modernizr` object, and as classes on
the `<html>` element. This information allows you to progressively
enhance your pages with a granular level of control over the
experience.

%prep
%setup -qn Modernizr-%{version}
%undos -f js

%build
cat feature-detects/*.js > feature-detects.js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -p feature-detects.js $RPM_BUILD_ROOT%{_appdir}
cp -p modernizr.js $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/modernizr.js
%{_appdir}/feature-detects.js
