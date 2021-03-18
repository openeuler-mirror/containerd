%global goipath github.com/containerd/containerd
%global debug_package %{nil}
Version:        1.2.0
Name:           containerd
Release:        108
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
