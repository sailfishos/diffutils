#specfile originally created for Fedora, modified for Moblin Linux
%define _name diffutils
Summary: A GNU collection of diff utilities
Name: gnu-%{_name}
# NOTE: diffutils changed to GPLv3 from version 2.9 thus the old version is used.
Version: 2.8.1+git1
Release: 0
License: GPLv2+
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source: diffutils-2.8.1.tar.gz
Source1: cmp.1
Source2: diff.1
Source3: diff3.1
Source4: sdiff.1
Patch0: diffutils-2.8.4-i18n.patch
Patch1: diffutils-2.8.1-badc.patch
Patch2: diffutils-sdiff.patch
Patch3: diffutils-2.8.1-null.patch
Patch4: diffutils-aarch64.patch
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
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description doc
%{summary}.

%prep
%autosetup -p1 -n diffutils-2.8.1

%build
%configure

# Remove -fcommon after package updated to a new enough version.
# Used for allowing uninitialized global variables in a common block.
make PR_PROGRAM=%{_bindir}/pr CFLAGS="-fcommon $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

( cd $RPM_BUILD_ROOT
  gzip -9nf .%{_infodir}/diff*
  mkdir -p .%{_mandir}/man1
  for manpage in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}
  do
    install -m 0644 ${manpage} .%{_mandir}/man1
  done
)

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
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
%defattr(-,root,root)
%{_bindir}/*

%files doc
%defattr(-,root,root)
%doc NEWS README
%doc %{_mandir}/*/*
%doc %{_infodir}/diff.info*gz
