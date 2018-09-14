Name:           ansible-asb-modules
Version:        0.4.0
Release:        1%{?dist}
Summary:        Ansible role containing Ansible Service Broker modules
License:        ASL 2.0
URL:            https://github.com/ansibleplaybookbundle/%{name}
Source0:        https://github.com/ansibleplaybookbundle/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires: ansible >= 2.3.0.0

%description
%{summary}

%prep
%autosetup -p1

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/ansible/roles/ansibleplaybookbundle.asb-modules
mv * %{buildroot}%{_sysconfdir}/ansible/roles/ansibleplaybookbundle.asb-modules

%check

%files
%{_sysconfdir}/ansible/roles/ansibleplaybookbundle.asb-modules

%changelog
* Tue Jul 24 2018 David Zager <david.j.zager@gmail.com> 0.3.1-1
- Bump release (#21) (dzager@redhat.com)
- Update releasers (#20) (dzager@redhat.com)

* Mon Jul 23 2018 David Zager <david.j.zager@gmail.com> 0.2.2-1
- get/set state module implementation (#15) (pgough@redhat.com)

* Wed Apr 25 2018 David Zager <david.j.zager@gmail.com> 0.2.1-1
- Lock asb-brew releaser to 3.10 branch (#18) (dzager@redhat.com)
- Bump release (#17) (dzager@redhat.com)
- Bug 1569220 - Add dashboard_url ansible module (#16) (dymurray@redhat.com)
- Initialize annotations if empty (#14) (dzager@redhat.com)

* Thu Feb 22 2018 David Zager <david.j.zager@gmail.com> 0.1.2-1
- last_operation module (#9) (maleck13@users.noreply.github.com)
- Add basic doc to help contributers to add and test new modules (#10)
  (maleck13@users.noreply.github.com)

* Mon Dec 04 2017 Jason Montleon <jmontleo@redhat.com> 0.1.1-1
- Create secret for bind credentials (#8) (david.j.zager@gmail.com)
- bump release (#7) (jmrodri@gmail.com)

* Thu Nov 02 2017 Jason Montleon <jmontleo@redhat.com> 0.0.2-1
- new package built with tito

* Fri May 12 2017 Chris Chase <cchase@redhat.com> - 0.0.1-1
- initial package
