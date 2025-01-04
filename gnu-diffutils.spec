#specfile originally created for Fedora, modified for Moblin Linux
%define _name diffutils
Summary: A GNU collection of diff utilities
Name: gnu-%{_name}
# NOTE: diffutils changed to GPLv3 from version 2.9 thus the old version is used.
Version: 3.10
Release: 0
License: GPLv3+
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source: diffutils-3.10.tar.xz
Source1: cmp.1
Source2: diff.1
Source3: diff3.1
Source4: sdiff.1
Provides: %{_name} = 2.8.1+git1
Obsoletes: %{_name} < 2.8.1+git1

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

%package doc
Summary:         Documentation for diff utilities
Requires: %{name} = %{version}
Provides: %{_name}-doc = 2.8.1+git1
Obsoletes: %{_name}-doc < 2.8.1+git1

%description doc
%{summary}.

%prep
%autosetup -p1 -n diffutils-3.10

%build
%configure

%make_build

%install
%make_install

( cd $RPM_BUILD_ROOT
  gzip -9nf .%{_infodir}/diff*
  mkdir -p .%{_mandir}/man1
  for manpage in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}
  do
    install -m 0644 ${manpage} .%{_mandir}/man1
  done
)

rm -Rf $RPM_BUILD_ROOT%{_infodir}
%find_lang %{_name}

%post doc
[ -e %{_infodir}/diff.info.gz ] && /sbin/install-info %{_infodir}/diff.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."
exit 0

%preun doc
if [ $1 = 0 ]; then
    [ -e %{_infodir}/diff.info.gz ] && /sbin/install-info --delete %{_infodir}/diff.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."
fi
exit 0

%files -f %{_name}.lang
%{_bindir}/*

%files doc
%doc NEWS README
%doc %{_mandir}/*/*
