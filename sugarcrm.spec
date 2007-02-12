# TODO
# - secure it
# - add other (all?) languages
# - language packs overwrite common files like jscalendar/calendar-setup_3.js,
#   which contain locality specifics like first_day_of_week
# - make these locale files as symlinks?:
#    echo '<script type="text/javascript" src="jscalendar/lang/calendar-en.js"></script>';
#    echo '<script type="text/javascript" src="jscalendar/calendar-setup_3.js"></script>';
# - language packs have different license. subpackage them? separate specs?
%define		namesrc	SugarSuite
%include	/usr/lib/rpm/macros.php
Summary:	Customer Relationship Management
Summary(pl.UTF-8):   Narzędzie CRM
Name:		sugarcrm
Version:	4.0.1
Release:	0.14
License:	SugarCRM Public License
Group:		Applications/WWW
Source0:	http://www.sugarforge.org/frs/download.php/919/%{namesrc}-%{version}.zip
# Source0-md5:	bce40535bf664ec567889534dbc6ba2c
Source1:	%{name}.conf
# polish
Source10:	http://www.sugarforge.org/frs/download.php/1111/SugarCRM-%{version}c-LangPack-pl_PL-2006-03-16.zip
# Source10-md5:	74fcbe135fcf9b3091d8461066ca4ba2
# spanish
Source11:	http://www.sugarforge.org/frs/download.php/1097/%{namesrc}-%{version}d-lang-es_es-20060308.zip
# Source11-md5:	9e3beb6e97186b8e0983ec411cda92a7
Source12:	http://www.sugarforge.org/frs/download.php/1136/SugarCRM-%{version}e-LangPack-fr_FR-2005-03-22.zip
# Source12-md5:	65a782e199f534d22a162453b7ed19c2
Source13:	http://www.sugarforge.org/frs/download.php/849/SugarEnt-4.0-lang-ge_ge-2005-12-19.zip
# Source13-md5:	c1fd9063866e7e3be7fe5a4084e3c84e
# russian
Source14:	http://www.sugarforge.org/frs/download.php/805/SugarRus.zip
# Source14-md5:	c3f3212f7b4f23de113b864ddcce993b
# spanish-latin
Source15:	http://www.sugarforge.org/frs/download.php/1084/SugarOpen-%{version}c-lang-sp_ve.zip
# Source15-md5:	8355b8d5b3b7ebd52b0c807aaea8e71e
# czech
Source16:	http://www.sugarforge.org/frs/download.php/1125/BETA_cz_%{version}e.zip
# Source16-md5:	ac622f8b76075cecefd8973097afd901
# italiano utf
Source17:	http://www.sugarforge.org/frs/download.php/1066/it_it_%{version}c.utf.langpack.zip
# Source17-md5:	0dd47f0fa48547d9dcdfa9f9f7671aa2
Patch0:		%{name}-mysqlroot.patch
Patch1:		%{name}-smarty.patch
Patch2:		%{name}-pear.patch
Patch3:		%{name}-setup.patch
Patch4:		%{name}-email_utf-8.patch
URL:		http://www.sugarforge.org/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
Requires:	Smarty >= 2.6.10-4
Requires:	php(curl)
Requires:	php(mysql)
Requires:	php(xml)
Requires:	webapps
Requires:	webserver(php) >= 4.2.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# symlinked from appdir
%define		_noautocompressdoc	LICENSE
%define		_noautoreq	'pear(/etc/webapps/.*)' 'pear([a-z/.].*.php)' 'pear(CustomFieldsTable.php)' 'pear(CustomFieldsTableSchema.php)' 'pear(DBHelper.php)' 'pear(DBManager.php)' 'pear(FieldsMetaData.php)' 'pear(ModuleInstall/ModuleInstaller.php)' 'pear(MysqlHelper.php)' 'pear(MysqlManager.php)' 'pear(XTemplate/xtpl.php)'

%description
SugarCRM is a suite of business automation tools for managing your
marketing, sales and customer service operations. From leads to
contacts, opportunities to cases, the Sugar Suite helps you track and
gain insight into your customers.

%description -l pl.UTF-8
SugarCRM to zestaw narzędzi automatyki biznesowej do zarządzania
operacjami marketingu, sprzedaży i obsługi klientów. Od wprowadzenia
do kontraktów, od okazji do spraw Sugar Suite pomaga śledzić i mieć
wgląd w swoich klientów.

%package setup
Summary:	SugarCRM setup package
Summary(pl.UTF-8):   Pakiet instalacyjny SugarCRM
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial SugarCRM installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować do skonfigurowania początkowej
instalacji SugarCRM. Następnie należy go odinstalować, ponieważ
trzymanie plików instalacyjnych może być niebezpieczne.

%prep
%setup -qc
cd SugarSuite-Full-%{version}

# polish
rm jscalendar/lang/calendar-pl.js # language zip contains better version
%{__unzip} -qq %{SOURCE10} -x manifest.php

# spanish
rm jscalendar/{lang/calendar-es.js,calendar-setup_3.js} # allow overwrite from es_ES language
%{__unzip} -qq %{SOURCE11} -x manifest.php

# french
rm jscalendar/{lang/calendar-fr.js,calendar-setup_3.js} # allow overwrite from fr_FR language
(cd ..; ln -s SugarSuite-Full-%{version} fr_FR_401; %{__unzip} -qq %{SOURCE12} -x manifest.php)

# german
%{__unzip} -qq %{SOURCE13} -x manifest.php

# russian
(cd ..; ln -s SugarSuite-Full-%{version} SugarRus; %{__unzip} -qq %{SOURCE14} -x SugarRus/manifest.php)

# spanish-latin
%{__unzip} -qq %{SOURCE15} -x manifest.php

# czech
(cd ..; ln -s SugarSuite-Full-%{version} cs_cz; %{__unzip} -qq %{SOURCE16} -x cs_cz/manifest.php)

# italiano utf
mv index.php{,.orig}
rm jscalendar/lang/calendar-it.js
rm jscalendar/calendar-setup_3.js
rm include/phpmailer/language/phpmailer.lang-it.php
%{__unzip} -qq %{SOURCE17} -x manifest.php
mv -f index.php{.orig,}

# undos the sources
find -regex '.*\.\(php\|inc\|html\|txt\|js\|properties\)$' -print0 | xargs -0 sed -i -e 's,\r$,,'

rm -r include/Smarty
rm -r include/HTTP_WebDAV_Server
rm -r include/Mail_IMAP
rm -r include/Net_URL
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

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
