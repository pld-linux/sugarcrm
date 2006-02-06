# TODO
# - secure it
# - add other (all?) languages
# - language packs overwrite common files like jscalendar/calendar-setup_3.js,
#   which contain locality specifics like first_day_of_week
# - language packs have different license. subpackage them? separate specs?
%define		namesrc	SugarSuite
Summary:	Customer Relationship Management
Summary(pl):	Narzêdzie CRM
Name:		sugarcrm
Version:	4.0.1
Release:	0.4
License:	SugarCRM Public License
Group:		Applications/WWW
Source0:	http://www.sugarforge.org/frs/download.php/919/%{namesrc}-%{version}.zip
# Source0-md5:	bce40535bf664ec567889534dbc6ba2c
Source1:	%{name}.conf
Source10:	http://www.sugarforge.org/frs/download.php/967/SugarCRM-%{version}-LangPack-pl_PL-2006-02-04.zip
# Source10-md5:	2612dd0f2d63614f80e571678675492c
#Source11:	http://www.sugarforge.org/frs/download.php/326/%{namesrc}-%{version}-lang-es_es-20050817-2.zip
Source12:	http://www.sugarforge.org/frs/download.php/958/SugarCRM-%{version}-LangPack-fr_FR-2005-02-01.zip
# Source12-md5:	4413eb0ab37dceca318a71f6000d2283
Source13:	http://www.sugarforge.org/frs/download.php/849/SugarEnt-4.0-lang-ge_ge-2005-12-19.zip
# Source13-md5:	c1fd9063866e7e3be7fe5a4084e3c84e
Patch0:		%{name}-mysqlroot.patch
Patch1:		%{name}-smarty.patch
Patch2:		%{name}-pear.patch
URL:		http://www.sugarforge.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	Smarty >= 2.6.10-4
Requires:	php >= 3:4.3.0
Requires:	php-mysql
Requires:	php-pear-HTTP_WebDAV_Server
#Requires:	php-pear-Mail_IMAP - doesn't seem to be used
Requires:	php-xml
Requires:	php-curl
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
%setup -qc
cd SugarSuite-Full-%{version}
rm jscalendar/lang/calendar-pl.js # language zip contains better version
%{__unzip} -qq %{SOURCE10} -x manifest.php
rm -f jscalendar/{lang/calendar-fr.js,calendar-setup_3.js} # allow overwrite from fr_FR language
(cd ..; ln -s SugarSuite-Full-%{version} fr_FR_401; %{__unzip} -qq %{SOURCE12} -x manifest.php)
%{__unzip} -qq %{SOURCE13} -x manifest.php

# undos the sources
find -regex '.*\.\(php\|inc\|html\|txt\|js\)$' -print0 | xargs -0 sed -i -e 's,\r$,,'

rm -r include/Smarty
rm -r include/HTTP_WebDAV_Server
rm -r include/Mail_IMAP
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
cd SugarSuite-Full-%{version}
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cp -a */ $RPM_BUILD_ROOT%{_appdir}
cp -a *.php *.html $RPM_BUILD_ROOT%{_appdir}
cp -a robots.txt log4php.properties $RPM_BUILD_ROOT%{_appdir}

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
%doc SugarSuite-Full-%{version}/{INSTALLATION.txt,LICENSE,PATCH.txt,README.txt,UPGRADE.TXT}
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%dir %{_appdir}
%{_appdir}/ModuleInstall
%{_appdir}/XTemplate
%{_appdir}/examples
%{_appdir}/include
%{_appdir}/jscalendar
%{_appdir}/log4php
%{_appdir}/metadata
%{_appdir}/soap
%{_appdir}/themes
%{_appdir}/*.txt
%{_appdir}/*.html
%{_appdir}/*.php
%{_appdir}/log4php.properties
%exclude %{_appdir}/install
%exclude %{_appdir}/install.php

# must be writable: cache, custom, data, modules, config.php
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
