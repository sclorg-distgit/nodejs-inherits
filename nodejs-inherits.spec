%{?scl:%scl_package nodejs-inherits}
%{!?scl:%global pkg_name %{name}}
%{?nodejs_find_provides_and_requires}

Name:       %{?scl_prefix}nodejs-inherits
Version:    2.0.0
Release:    13%{?dist}
Summary:    A tiny simple way to do classic inheritance in js
License:    WTFPL
Group:      Development/Libraries
URL:        https://github.com/isaacs/inherits
Source0:    http://registry.npmjs.org/inherits/-/inherits-%{version}.tgz
Source1:    https://raw.github.com/isaacs/inherits/112807f2670160b6e3bafdf39e395c10ae7d0fac/LICENSE
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch

BuildRequires:  %{?scl_prefix}nodejs-devel

%description
%{summary}.

%prep
%setup -q -n package

#copy the license into %%{_builddir} so it works with %%doc
cp -p %{SOURCE1} LICENSE

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/inherits
cp -pr inherits.js package.json %{buildroot}%{nodejs_sitelib}/inherits

%nodejs_symlink_deps

ln -sf inherits %{buildroot}%{nodejs_sitelib}/inherits@2

%clean
rm -rf %{buildroot}

# there have been reports that the symlinks are messed up when upgrading
# from older versions, so let's make sure everything's copacetic
%triggerun -- nodejs-inherits < 2.0.0-4
ln -sf inherits@2 %{nodejs_sitelib}/inherits
%{__python} <<EOF
import json, os, sys

for moddir in os.listdir('%{nodejs_sitelib}'):
    if os.path.isdir(moddir):
        md = json.load(open(os.path.join(moddir, 'package.json')))
        
        if 'dependencies' in md and 'inherits' in md['dependencies']:
            if isinstance(md['dependencies'], dict) and '1' in md['dependencies']['inherits']:
                src = os.path.join('%{nodejs_sitelib}', 'inherits@1')
            else:
                src = os.path.join('%{nodejs_sitelib}', 'inherits@2')
               
            dest = os.path.join('%{nodejs_sitelib}', moddir, 'node_modules/inherits')
            
            if not os.path.realpath(dest) == src:
                try:
                    os.unlink(dest)
                except OSError:
                    pass
                    
                try:
                    os.symlink(src, dest)
                except OSError, e:
                    sys.stderr.write(e + '\n')
EOF

# rpm blows up if you try to replace a dir with a symlink or vice-versa
#%pretrans -p <lua>
#if posix.stat("%{nodejs_sitelib}/inherits", "type") == "directory" then
#    os.rename('%{nodejs_sitelib}/inherits', '%{nodejs_sitelib}/inherits@2')
#end

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/inherits@2
%{nodejs_sitelib}/inherits
%doc README.md LICENSE

%changelog
* Tue Feb 09 2016 Tomas Hrcka <thrcka@redhat.com> - 2.0.0-13
- Sync build versions for clean ugrade path

* Fri Oct 23 2015 Zuzana Svetlikova <zsvetlik@redhat.com> - 2.0.0-10
- Switched symlink and commented out %%pretrans scriptlet (RHBZ#1273117)

* Thu Oct 15 2015 Zuzana Svetlikova <zsvetlik@redhat.com> - 2.0.0-9
- Rebuilt

* Wed Oct 14 2015 Zuzana Svetlikova <zsvetlik@redhat.com> - 2.0.0-8
- Fix bad indentation in python script

* Fri Oct 09 2015 Zuzana Svetlikova <zsvetlik@redhat.com> - 2.0.0-7
- Enable multiversioning (BZ#1268882)

* Wed Mar 05 2014 Tomas Hrcka <thrcka@redhat.com> - 2.0.0-6
- Disable multiversion inherits

* Thu Oct 17 2013 Tomas Hrcka <thrcka@redhat.com> - 2.0.0-5
- replace provides and requires with macro

* Fri Aug 16 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-4
- add some post-install hackery to work around potential RPM bug resulting in
  symlinks still pointing to their old locations on upgrade (RHBZ#997978)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-3
- only run the hack when we really need to

* Sat Jul 06 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-2
- use lua for pretrans

* Sun Jun 23 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-1
- new upstream release 2.0.0
- include license file
- follow the mutiple version spec

* Sun Jun 23 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-9
- restrict to compatible arches

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-8
- add macro for EPEL6 dependency generation

* Thu Apr 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.0-8
- Add support for software collections

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-6
- add missing build section

* Thu Jan 03 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-5
- correct license tag (thanks to Robin Lee)

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-4
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-3
- guard Requires for F17 automatic depedency generation

* Sat Feb 11 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-2
- switch to automatically generated provides/requires

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-1
- initial package
