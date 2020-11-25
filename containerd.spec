%global goipath github.com/containerd/containerd
%global debug_package %{nil}
Version:        1.2.0
Name:           containerd
Release:        102
Summary:        An industry-standard container runtime
License:        ASL 2.0
URL:            https://containerd.io
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  golang glibc-static make btrfs-progs-devel

%description
containerd is an industry-standard container runtime with an emphasis on
simplicity, robustness and portability.  It is available as a daemon for Linux
and Windows, which can manage the complete container lifecycle of its host
system: image transfer and storage, container execution and supervision,
low-level storage and network attachments, etc.

%prep
%setup -c -n containerd

%build
./apply-patch

GO_BUILD_PATH=$PWD/_build
install -m 0755 -vd $(dirname $GO_BUILD_PATH/src/%{goipath})
ln -fs $PWD $GO_BUILD_PATH/src/%{goipath}
cd $GO_BUILD_PATH/src/%{goipath}
export GOPATH=$GO_BUILD_PATH:%{gopath}
export BUILDTAGS="no_btrfs no_cri"
make

%install
install -d $RPM_BUILD_ROOT/%{_bindir}
install -p -m 755 bin/containerd $RPM_BUILD_ROOT/%{_bindir}/containerd
install -p -m 755 bin/containerd-shim $RPM_BUILD_ROOT/%{_bindir}/containerd-shim

%files
%{_bindir}/containerd
%{_bindir}/containerd-shim

%changelog
