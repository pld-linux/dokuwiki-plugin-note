%define		plugin		note
Summary:	DokuWiki note plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	20090615
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://gauret.free.fr/fichiers/dokuwiki/dokuwiki-%{plugin}-%{version}.tgz
# Source0-md5:	9121176dcb0c83ebd1d9008e949191ec
URL:		http://www.dokuwiki.org/plugin:note
BuildRequires:	rpmbuild(macros) >= 1.520
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
mv %{plugin}/* .
rm %{plugin}/.gitignore

version=$(awk '/date/{print $2}' info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/images
