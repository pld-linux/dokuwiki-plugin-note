%define		subver	2020-06-28
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		note
%define		php_min_version 5.3.0
Summary:	DokuWiki note plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/LarsGit223/dokuwiki_note/archive/%{subver}/%{plugin}-%{subver}.tar.gz
# Source0-md5:	e73bc174b2893af0eb6c9076bba95828
URL:		https://www.dokuwiki.org/plugin:note
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	rpmbuild(find_lang) >= 1.41
Requires:	dokuwiki >= 20090214
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%description
This plugin allows you to create nice notes in your DokuWiki pages.

%prep
%setup -qc
mv dokuwiki_note-*/{.??*,*} .
rm .gitignore

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{COPYING,README.md,CHANGES.md}

%find_lang %{name}.lang --with-dokuwiki

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md CHANGES.md
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/images
