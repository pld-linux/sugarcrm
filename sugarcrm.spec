# TODO
# - secure it
Summary:	Customer Relationship Management
Name:		sugarcrm
Version:	3.0.1
%define	_beta	b
%define	_rel	15
Release:	%{_beta}.%{_rel}
Epoch:		0
License:	SugarCRM Public License
Group:		Applications/WWW
Source0:	http://www.sugarforge.org/frs/download.php/242/SugarSuite-Full-%{version}%{_beta}.zip
# Source0-md5:	8f161b5c43209f0cb9273a724bbd6989
Source1:	%{name}.conf
Patch0:		%{name}-mysqlroot.patch
URL:		http://www.sugarforge.org/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires:	apache >= 1.3.33-2
Requires:	php >= 3:4.2.0
Requires:	php-mysql
Requires:	php-xml
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_appdir %{_datadir}/%{name}
%define	_sysconfdir /etc/%{name}

# symlinked from appdir
%define _noautocompressdoc LICENSE

# nothing to strip/chrpath/compress
%define	no_install_post_strip 1
%define	no_install_post_chrpath 1
%define	no_install_post_compress_modules 1

%description
SugarCRM is a suite of business automation tools for managing your
marketing, sales and customer service operations. From leads to
contacts, opportunities to cases, the Sugar Suite helps you track and
gain insight into your customers.

%package setup
Summary:	SugarCRM setup package
Group:		Applications/WWW
PreReq:		%{name} = %{epoch}:%{version}-%{release}

%description setup
Install this package to configure initial SugarCRM installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%prep
%setup -q -n SugarSuite-Full-%{version}%{_beta}
# undos the sources
find -regex '.*\.\(php\|inc\|html\|txt\|js\)$' -print0 | xargs -0 sed -i -e 's,
$,,'

%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cp -a */ $RPM_BUILD_ROOT%{_appdir}
cp -a *.php *.html $RPM_BUILD_ROOT%{_appdir}
cp -a robots.txt $RPM_BUILD_ROOT%{_appdir}

cp -a LICENSE.txt $RPM_BUILD_ROOT%{_appdir}
ln -sf %{_appdir}/LICENSE.txt LICENSE

ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.php
install config.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post setup
chmod 660 %{_sysconfdir}/config.php
chown root:http %{_sysconfdir}/config.php

%postun setup
if [ "$1" = "0" ]; then
	chmod 640 %{_sysconfdir}/config.php
	chown root:http %{_sysconfdir}/config.php
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc INSTALLATION.txt LICENSE PATCH.txt README.txt UPGRADE.TXT
%attr(710,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%dir %{_appdir}
%{_appdir}/XTemplate
%{_appdir}/examples
%{_appdir}/include
%{_appdir}/jscalendar
%{_appdir}/log4php
%{_appdir}/metadata
%{_appdir}/soap
%{_appdir}/themes
%{_appdir}/upgrade
%{_appdir}/*.txt
%{_appdir}/*.html
%{_appdir}/[!i]*.php
%{_appdir}/index.php

%defattr(644,root,http,775)
%{_appdir}/cache
%{_appdir}/custom
%defattr(664,root,http,775)
%{_appdir}/modules
%{_appdir}/data

%files setup
%defattr(644,root,root,755)
%{_appdir}/install
%{_appdir}/install.php
