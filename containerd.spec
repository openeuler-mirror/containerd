%global goipath github.com/containerd/containerd
%global debug_package %{nil}
Version:        1.2.0
Name:           containerd
Release:        301
Summary:        An industry-standard container runtime
License:        ASL 2.0
URL:            https://containerd.io
Source0:        https://github.com/containerd/containerd/archive/v1.2.0.zip
Source1:        patch.tar.gz
Source2:        apply-patch
Source3:        series.conf
Source4:        git-commit
Source5:        gen-commit.sh

BuildRequires:  golang glibc-static make btrfs-progs-devel

%description
containerd is an industry-standard container runtime with an emphasis on
simplicity, robustness and portability.  It is available as a daemon for Linux
and Windows, which can manage the complete container lifecycle of its host
system: image transfer and storage, container execution and supervision,
low-level storage and network attachments, etc.

%prep
cp %{SOURCE0} .
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .

%build
bash ./apply-patch

GO_BUILD_PATH=$PWD/_build
install -m 0755 -vd $(dirname $GO_BUILD_PATH/src/%{goipath})
ln -fs $PWD $GO_BUILD_PATH/src/%{goipath}
cd $GO_BUILD_PATH/src/%{goipath}
export GO111MODULE=off
export GOPATH=$GO_BUILD_PATH:%{gopath}
export BUILDTAGS="no_btrfs no_cri"
make
strip ./bin/containerd ./bin/containerd-shim

%install
install -d $RPM_BUILD_ROOT/%{_bindir}
install -p -m 755 bin/containerd $RPM_BUILD_ROOT/%{_bindir}/containerd
install -p -m 755 bin/containerd-shim $RPM_BUILD_ROOT/%{_bindir}/containerd-shim

%files
%{_bindir}/containerd
%{_bindir}/containerd-shim

%changelog
* Tue May 10 2022 Vanient<xiadanni1@huawei.com> - 1.2.0-301
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Use fs.RootPath when mounting volumes for bundle dir to fix CVE-2022-23648

* Sat Jan 22 2022 songyanting<songyanting@huawei.com> - 1.2.0-300
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync bugfix, include
       1. add check in spec
       2. kill container init process if runc start returns error
       3. fix containerd-shim residual when kill containerd durin
       4. fix deadlock on commit error
       5. backport upstream & ttrpc patches
       6. fix exec event missing due to pid reuse
       7. fix dm left when pause container and kill shim
       8. add CGO security build options
       9. fix start container failed with id exists
      10. drop opt package
      11. fix race access for mobySubscribed
      12. improve log for debugging
      13. reduce permission for bundle dir
      14. fix publish command wait block forever

* Mon Jan 10 2022 xiadanni<xiadanni1@huawei.com> - 1.2.0-109
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:disable go module build

* Thu Mar 18 2021 xiadanni<xiadanni1@huawei.com> - 1.2.0-108
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:compile option compliance

* Thu Mar 18 2021 xiadanni<xiadanni1@huawei.com> - 1.2.0-107
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync bugfix, include
       1. check task list to avoid unnecessary cleanup.
       2. fix dead loop
       3. cleanup dangling shim by brand new context
       4. fix potential panic for task in unknown state

* Fri Dec 11 2020 yangyanchao <yangyanchao6@huawei.com> 1.2.0-106
- Type:requirement
- ID:NA
- CVE:NA
- SUG:restart
- DESC:containerd:vendor:add some symbol to support riscv
