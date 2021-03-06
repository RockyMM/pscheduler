#
# RPM Spec for pScheduler Sleep Tool
#

%define short	sleep
Name:		pscheduler-tool-%{short}
Version:	1.0
Release:	0.1.rc1%{?dist}

Summary:	Sleep tool class for pScheduler
BuildArch:	noarch
License:	Apache 2.0
Group:		Unspecified

Source0:	%{short}-%{version}.tar.gz

Provides:	%{name} = %{version}-%{release}

Requires:	pscheduler-server
Requires:	python-pscheduler
Requires:	pscheduler-test-idle

BuildRequires:	pscheduler-rpm


%description
Sleep tool class for pScheduler


%prep
%setup -q -n %{short}-%{version}


%define dest %{_pscheduler_tool_libexec}/%{short}

%build
make \
     DESTDIR=$RPM_BUILD_ROOT/%{dest} \
     DOCDIR=$RPM_BUILD_ROOT/%{_pscheduler_tool_doc} \
     install



%post
pscheduler internal warmboot

%postun
pscheduler internal warmboot


%files
%defattr(-,root,root,-)
%{dest}
%{_pscheduler_tool_doc}/*
