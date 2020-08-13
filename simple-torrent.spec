%define debug_package %{nil}

%define  uid   cloud
%define  gid   cloud
%define  nuid  974
%define  ngid  972



Name:     simple-torrent
Version:  1.2.11
Release:  2%{?dist}
Summary:  Bittorrent Client Written in GoLang
Epoch:    1
Packager: Eliezer Croitoru <eliezer@ngtech.co.il>
Vendor:   NgTech Ltd
License:  AGPLv3
Group:    System Environment/Daemons
URL:      https://github.com/idcm/simple-torrent/tags
Source0:  https://github.com/idcm/simple-torrent/archive/1.2.11.tar.gz
Source1:  cloud.service
Source2:  cloud.sysconfig
Source3:  example_config.yaml

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:     golang
BuildRequires:     git
BuildRequires:     go-bindata
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd



%description
Simple-torrent an opensource Bittorrent client written in GoLang.

%prep
%setup -q -n %{name}-%{version}

%build
GITVER=$(git describe --tags)
go build -o %{name} -ldflags "-s -w -X main.VERSION=$GITVER"


%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}

# install binary
install -p -D -m 0755 %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/%{name}

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/cloud.service

# install configuration
install -p -D -m 0644 \
   %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/%{name}/%{name}.yaml

install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/sysconfig/simple-torrent

%clean
rm -rf %{buildroot}

%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -s /sbin/nologin -u %{nuid} -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -s /sbin/nologin -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi

%post
%systemd_post cloud.service

%preun
%systemd_preun cloud.service

%postun
%systemd_postun_with_restart cloud.service
userdel %{uid}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/simple-torrent
%config(noreplace) %{_sysconfdir}/%{name}
%{_unitdir}/cloud.service

%changelog
* Tue Jan 07 2020 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 2.0.0 Stable.
