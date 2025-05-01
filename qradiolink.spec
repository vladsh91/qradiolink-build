# Have SOURCE_DATE_EPOCH value set
%global source_date_epoch_from_changelog 1
# Ensure no file timestamps are later than SOURCE_DATE_EPOCH
%global clamp_mtime_to_source_date_epoch 1
# Force build timestamp to SOURCE_DATE_EPOCH
%global use_source_date_epoch_as_buildtime 1

%define realver 0.9.1-3
Name:           qradiolink
Version:        0.9.1.3
Release:        a535333
Summary:        SDR TX/RX
License:        GPL-3.0
Group:          Productivity/Hamradio/Other
URL:            http://qradiolink.org
#Git-Clone:     https://github.com/kantooon/qradiolink.git
Source:         https://github.com/kantooon/%{name}/archive/%{realver}.tar.gz#/%{name}-%{realver}.tar.gz
Patch1:         qradiolink-spdlog-use-external-fmt.patch
Patch2:         qradiolink-add-missing-include.patch
Patch3:         qradiolink-fix-return-in-nonvoid-functions.patch
BuildRequires:  boost-devel
BuildRequires:  gcc-c++
BuildRequires:  gnuradio-devel
BuildRequires:  uhd-devel
BuildRequires:  libftdi-devel
BuildRequires:  gsm-devel
BuildRequires:  libjpeg-devel
BuildRequires:  pkgconfig(LimeSuite)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(SoapySDR)
BuildRequires:  pkgconfig
BuildRequires:  qwt6-qt5-devel
BuildRequires:  gr-osmosdr-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(codec2)
BuildRequires:  pkgconfig(libconfig++)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  cppzmq-devel
BuildRequires:  pkgconfig(opus)
BuildRequires:  protobuf-devel
BuildRequires:  pkgconfig(speex)
BuildRequires:  spdlog-devel
BuildRequires:  log4cpp-devel
BuildRequires:  rpmfusion-free-release
BuildRequires:  speexdsp-devel
BuildRequires:  gmp-devel

%description
QRadioLink is a GUI for a collection of GNURadio modems, built for
hobbyists, tinkerers and radio enthusiasts, which allows experimenting
with SDR hardware using different digital and analog modes.

It can also be used as a SDR transceiver for amateur radio.

%prep
%setup -q -n %{name}-%{realver}
# %patch 1 -p1
# %patch 2 -p1
# %patch 3 -p1

%build
mkdir build
cd src/ext
ln -s /usr/lib64/libftdi1.so %{_builddir}/qradiolink-%{realver}/libftdi.so
protoc --cpp_out=. Mumble.proto
protoc --cpp_out=. QRadioLink.proto

export LDFLAGS="-L%{_builddir}/qradiolink-%{realver}/"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS -I /usr/include/libftdi1/ -Wno-deprecated-declarations -Wno-unused-variable -Wno-maybe-uninitialized -Wno-int-in-bool-context -Wno-unused-result -Wno-type-limits -Wno-sign-compare -Wno-unused-parameter"
%qmake_qt5 %{_builddir}/qradiolink-%{realver}

export LDFLAGS="-L%{_builddir}/qradiolink-%{realver}/"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS -I /usr/include/libftdi1/ -Wno-deprecated-declarations -Wno-unused-variable -Wno-maybe-uninitialized -Wno-int-in-bool-context -Wno-unused-result -Wno-type-limits -Wno-sign-compare -Wno-unused-parameter"
%make_build

%install
install -d %{buildroot}/%{_bindir}
install -m0755 %{_builddir}/qradiolink-%{realver}/src/ext/qradiolink %{buildroot}/%{_bindir}
install -Dm0644 src/res/logo.png %{buildroot}/%{_datadir}/pixmaps/%{name}.png

%files
%license LICENSE LICENSE.LGPL3 LICENSE.MIT
%doc AUTHORS README.md docs/CONFIGURE
%{_bindir}/qradiolink
%{_datadir}/pixmaps/%{name}.png

%changelog
* Thu May 1 2025 vladsh91@hotmail.com - 0.9.1.3
- Completed package
