#specfile originally created for Fedora, modified for Moblin Linux
Summary: A GNU collection of diff utilities
Name: diffutils
# NOTE: diffutils changed to GPLv3 from version 2.9 thus the old version is used.
Version: 2.8.1
Release: 21
License: GPLv2+
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.gz
Source1: cmp.1
Source2: diff.1
Source3: diff3.1
Source4: sdiff.1
Patch0: diffutils-2.8.4-i18n.patch
Patch1: diffutils-2.8.1-badc.patch
Patch2: diffutils-sdiff.patch
Patch3: diffutils-2.8.1-null.patch
Patch4: diffutils-aarch64.patch

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
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description doc
%{summary}.

%prep
%setup -q
%patch0 -p1 -b .i18n
%patch1 -p1 -b .badc
%patch2 -p1 -b .sdiff
%patch3 -p1
%patch4 -p1

%build
%configure
make PR_PROGRAM=%{_bindir}/pr

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
%find_lang %{name}

%post doc
[ -e %{_infodir}/diff.info.gz ] && /sbin/install-info %{_infodir}/diff.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."
exit 0

%preun doc
if [ $1 = 0 ]; then
    [ -e %{_infodir}/diff.info.gz ] && /sbin/install-info --delete %{_infodir}/diff.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."
fi
exit 0

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*

%files doc
%defattr(-,root,root)
%doc NEWS README
%doc %{_mandir}/*/*
%doc %{_infodir}/diff.info*gz

