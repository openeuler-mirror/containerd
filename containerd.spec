%global goipath github.com/containerd/containerd
%global debug_package %{nil}
Version:        1.6.22
Name:           containerd
Release:        7
Summary:        An industry-standard container runtime
License:        ASL 2.0
URL:            https://containerd.io
Source0:        https://github.com/containerd/containerd/archive/v1.6.22.zip
Source1:        patch.tar.gz
Source2:        apply-patch
Source3:        series.conf
Source4:        git-commit
Source5:        gen-commit.sh
Source6:        containerd.service
Source7:        config.toml

BuildRequires:  golang glibc-static make btrfs-progs-devel git

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
echo %{VERSION}.%{RELEASE} > containerd_version
bash ./apply-patch

GO_BUILD_PATH=$PWD/_build
install -m 0755 -vd $(dirname $GO_BUILD_PATH/src/%{goipath})
ln -fs $PWD $GO_BUILD_PATH/src/%{goipath}
cd $GO_BUILD_PATH/src/%{goipath}
export GO111MODULE=off
export GOPATH=$GO_BUILD_PATH:%{gopath}
export BUILDTAGS="no_btrfs no_cri"
make

%install
install -d $RPM_BUILD_ROOT/%{_bindir}
install -p -m 755 bin/* $RPM_BUILD_ROOT/%{_bindir}/
install -D -p -m 0644 %{S:6} %{buildroot}%{_unitdir}/containerd.service
install -D -p -m 0644 %{S:7} %{buildroot}%{_sysconfdir}/containerd/config.toml

%post
%systemd_post containerd.service

%preun
%systemd_preun containerd.service

%postun
%systemd_postun_with_restart containerd.service

%files
%{_bindir}/*
%{_unitdir}/containerd.service
%dir %{_sysconfdir}/containerd
%config(noreplace) %{_sysconfdir}/containerd/config.toml
%exclude %{_bindir}/containerd-stress

%changelog
* Fri Feb 23 2024 zhongjiawei<zhongjiawei1@huawei.com> - 1.6.22-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:disable Transparent HugePage for shim process if SHIM_DISABLE_THP is set

* Thu Dec 21 2023 zhongjiawei<zhongjiawei1@huawei.com> - 1.6.22-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix misssing closed fifo

* Wed Nov 08 2023 zhongjiawei<zhongjiawei1@huawei.com> - 1.6.22-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:update vendor net/http package to fix CVE-2023-39325

* Thu Oct 19 2023 zhongjiawei<zhongjiawei1@huawei.com> - 1.6.22-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix some bugs after version upgrade

* Tue Sep 19 2023 zhongjiawei<zhongjiawei1@huawei.com> - 1.6.22-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync some patches

* Fri Sep 8 2023 zhongjiawei<zhongjiawei1@huawei.com> - 1.6.22-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add patch for 1.6.22

* Wed Aug 2 2023 vegbir<yangjiaqi16@huawei.com> - 1.6.22-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:upgrade to contained 1.6.22

* Fri July 21 2023 vegbir<yangjiaqi16@huawei.com> - 1.6.21-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:upgrade to contained 1.6.21

* Mon May 15 2023 zhangzhihui<zhangzhihui@xfusion.com> - 1.6.20-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add other binaries to support high version.

* Fri Apr 21 2023 xulei<xulei@xfusion.com> - 1.6.20-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add check in spec

* Wed Apr 19 2023 xulei<xulei@xfusion.com> - 1.6.20-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:update to 1.6.20

* Mon Feb 27 2023 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-309
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2023-25153 and CVE-2023-25173

* Thu Dec 16 2022 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-308
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix k8s build fail without import context

* Tue Dec 13 2022 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-307
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: Fix goroutine leak in Exec

* Wed Nov 16 2022 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-306
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: add ctr binary into package

* Wed Nov 16 2022 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-305
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix version number wrong

* Thu Sep 22 2022 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-304
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: bugfix and add CGO security build option

* Mon Jul 4 2022 zhongjiawei<zhongjiawei1@huawei.com> - 1.2.0-303
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: Limit the response size of ExecSync to fix CVE-2022-31030

* Wed Jun 22 2022 zhangsong234<zhangsong34@huawei.com> - 1.2.0-302
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:put get pid lock after set process exited to avoid deadlock

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
