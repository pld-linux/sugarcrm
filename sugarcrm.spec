# TODO
# - secure it
# - subpackages?
%define	_beta	b
%define	_rel	17
Summary:	Customer Relationship Management
Summary(pl):	Narzêdzie CRM
Name:		sugarcrm
Version:	3.0.1
Release:	0.%{_beta}.%{_rel}
License:	SugarCRM Public License
Group:		Applications/WWW
Source0:	http://www.sugarforge.org/frs/download.php/242/SugarSuite-Full-%{version}%{_beta}.zip
# Source0-md5:	8f161b5c43209f0cb9273a724bbd6989
Source1:	%{name}.conf
Source10:	http://www.sugarforge.org/frs/download.php/360/SugarSuite-%{version}-lang-pl_pl-iso-beta-2005-06-29.zip
# Source10-md5:	568f125bf87f5595bb50dd78ede824d3
Source11:	http://www.sugarforge.org/frs/download.php/326/SugarSuite-3.0x-lang-es_es-20050817-2.zip
# Source11-md5:	dd7811b78660facefd4573a9c3d24dc3
Source12:	http://www.sugarforge.org/frs/download.php/243/SugarSuite-3.0.1b-lang-fr_FR-2005-07-05.zip
# Source12-md5:	4ca7c64e99d41262b3d7606a632ae232
Source13:	http://www.sugarforge.org/frs/download.php/239/sugarCRM_301_deutsch.zip
# Source13-md5:	9f0c00ef8272917b6131c355b5467352
Patch0:		%{name}-mysqlroot.patch
URL:		http://www.sugarforge.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php >= 3:4.2.0
Requires:	php-mysql
Requires:	php-xml
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# symlinked from appdir
%define		_noautocompressdoc	LICENSE

%description
SugarCRM is a suite of business automation tools for managing your
marketing, sales and customer service operations. From leads to
contacts, opportunities to cases, the Sugar Suite helps you track and
gain insight into your customers.

%description -l pl
SugarCRM to zestaw narzêdzi automatyki biznesowej do zarz±dzania
operacjami marketingu, sprzeda¿y i obs³ugi klientów. Od wprowadzenia
do kontraktów, od okazji do spraw Sugar Suite pomaga ¶ledziæ i mieæ
wgl±d w swoich klientów.

%package setup
Summary:	SugarCRM setup package
Summary(pl):	Pakiet instalacyjny SugarCRM
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial SugarCRM installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl
Ten pakiet nale¿y zainstalowaæ do skonfigurowania pocz±tkowej
instalacji SugarCRM. Nastêpnie nale¿y go odinstalowaæ, poniewa¿
trzymanie plików instalacyjnych mo¿e byæ niebezpieczne.

%prep
%setup -q -n SugarSuite-Full-%{version}%{_beta} -a 10 -a 11 -a 12 -a 13
# undos the sources
find -regex '.*\.\(php\|inc\|html\|txt\|js\)$' -print0 | xargs -0 sed -i -e 's,\r$,,'

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

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

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

%triggerpostun -- %{name} < 3.0.1-0.b.17
# rescue app config
if [ -f /etc/sugarcrm/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /etc/sugarcrm/config.php.rpmsave %{_sysconfdir}/config.php
fi

if [ -f /etc/sugarcrm/sugarcrm.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/sugarcrm/sugarcrm.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/sugarcrm/sugarcrm.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/sugarcrm/sugarcrm.conf.rpmsave
fi

if [ -L /etc/apache/conf.d/99_sugarcrm.conf ]; then
	rm -f /etc/apache/conf.d/99_sugarcrm.conf
	/usr/sbin/webapp register apache %{_webapp}
	%service -q apache reload
fi
if [ -L /etc/httpd/httpd.conf/99_sugarcrm.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_sugarcrm.conf
	/usr/sbin/webapp register httpd %{_webapp}
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc INSTALLATION.txt LICENSE PATCH.txt README.txt UPGRADE.TXT
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
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
