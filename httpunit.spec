# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

Name:           httpunit
Version:        1.7
Release:        %mkrel 0.0.7
Epoch:          0
Summary:        Automated web site testing toolkit
License:        MIT
Source0:        http://download.sourceforge.net/httpunit/httpunit-%{version}.zip
Patch0:         %{name}.build.patch
Patch1:         %{name}-JavaScript-NotAFunctionException.patch
Patch2:         %{name}-servlettest.patch
URL:            http://httpunit.sourceforge.net/
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  nekohtml
BuildRequires:  jtidy
BuildRequires:  locales-en
BuildRequires:  junit >= 0:3.8
BuildRequires:  servlet24
BuildRequires:  javamail >= 0:1.3
BuildRequires:  jaf >= 0:1.0.2
BuildRequires:  rhino
BuildRequires:  %{__unzip}
Requires:       junit >= 0:3.8
Requires:       jpackage-utils
Requires:       servlet24
Requires:       jaxp_parser_impl
# As of 1.5, requires either nekohtml or jtidy, and prefers nekohtml.
Requires:       nekohtml
Requires:       rhino
Group:          Development/Java
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%description
HttpUnit emulates the relevant portions of browser behavior, including form
submission, JavaScript, basic http authentication, cookies and automatic page
redirection, and allows Java test code to examine returned pages either as
text, an XML DOM, or containers of forms, tables, and links.
A companion framework, ServletUnit is included in the package.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}

%package        doc
Summary:        Documentation for %{name}
Group:          Development/Java
Requires:       %{name}-javadoc

%description    doc
Documentation for %{name}

%package        demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.


%prep
%setup -q
# to create the test and examples jar
%patch0 -p0
# patch to work with rhino 1.5
%patch1 -p0 -b .sav
# add META-INF
%patch2 -p0
#%{__unzip} -qd META-INF lib/httpunit.jar "*.dtd" # 1.6 dist zip is borked
# remove all binary libs and javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf doc/api
ln -s \
  %{_javadir}/junit.jar \
  %{_javadir}/jtidy.jar \
  %{_javadir}/nekohtml.jar \
  %{_javadir}/servletapi5.jar \
  %{_javadir}/js.jar \
  %{_javadir}/xerces-j2.jar \
  jars


%build
export LC_ALL=ISO-8859-1
export CLASSPATH=$(build-classpath jaf javamail)
%{ant} -Dbuild.compiler=modern -Dbuild.sysclasspath=last \
  jar javadocs test servlettest testjar examplesjar

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

# Jar versioning
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; \
 do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# Javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Avoid having api in doc
rm -rf doc/api

# Fix link between doc and javadoc
pushd doc
ln -sf %{_javadocdir}/%{name}-%{version} api
popd

# Demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p lib/%{name}-test.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-test-%{version}.jar
cp -p lib/%{name}-examples.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-examples-%{version}.jar

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%files doc
%defattr(0644,root,root,0755)
%doc doc/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7-0.0.4mdv2011.0
+ Revision: 605885
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7-0.0.3mdv2010.1
+ Revision: 522851
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.7-0.0.2mdv2010.0
+ Revision: 425190
- rebuild

* Thu Apr 09 2009 Funda Wang <fwang@mandriva.org> 0:1.7-0.0.1mdv2009.1
+ Revision: 365346
- rediff build patch

* Tue Jun 17 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.7-0.0.1mdv2009.0
+ Revision: 221468
- new version 1.7 and disable gcj_support

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:1.6.2-1.1.3mdv2009.0
+ Revision: 140755
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.6.2-1.1.3mdv2008.1
+ Revision: 120891
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.6.2-1.1.2mdv2008.0
+ Revision: 87389
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:1.6.2-1.1.1mdv2008.0
+ Revision: 47863
- Import httpunit




* Wed Feb 14 2007 Permaine Cheung <pcheung@redhat.com> - 0:1.6.2-1jpp.1
- Fixed buildroot, release
- Renamed manual subpackage to doc subpackage as per fedora packaging guideline
- Got rid of Vendor and Distribution tags.

* Mon May 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.6.2-1jpp
- Upgrade to 1.6.2
- First JPP-1.7 release

* Sat Nov 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6-1jpp
- Update to 1.6.
- Require Servlet API 2.3, ServletUnit doesn't work with 2.4.
- Fix classpath construction during build; now works also with classpathx-mail.
- Apply upstream patch to build with Java 1.5 (built with 1.4.2 though).
- Patch to fix class path in servlet tests during build.

* Wed Sep 22 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.5.4-3jpp
- Patched JavaScript.java to not handle  NotAFunctionException,
  as in Rhino-1.5-R5 this now is deprecated, not thrown any more
  and extends Error; also not to handle PropertyException not thrown
  any more in that try block 

* Wed Aug 25 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.5.4-2jpp
- Build with ant-1.6.2

* Thu Aug 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.5.4-1jpp
- Update to 1.5.4.
- Save .spec in UTF-8.

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.5.3-2jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.5.3-1jpp
- Update to 1.5.3 and JPackage 1.5.
- Include non-versioned javadoc symlink.

* Tue Mar  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.5.2-1jpp
- Update to 1.5.2.
- Run unit tests during build.

* Wed Dec 18 2002 Ville Skyttä <ville.skytta at iki.fi> - 1.5.1-1jpp
- Update to 1.5.1.

* Mon Nov  4 2002 Ville Skyttä <ville.skytta at iki.fi> 1.5-1jpp
- Update to 1.5.

* Thu Oct  3 2002 Ville Skyttä <ville.skytta at iki.fi> 1.4.6-1jpp
- Update to 1.4.6.

* Fri Sep  6 2002 Ville Skyttä <ville.skytta at iki.fi> 1.4.5-0.cvs20020906.1jpp
- Update to 1.4.5 (CVS 2002-09-06, CVS version needed since we have JUnit 3.8).
- Add requirements.
- Add rhino and xerces to build requirements.
- Fix/add Distribution, License, Vendor tags.
- Use sed instead of bash2 extension when symlinking jars during build.
- s/Copyright/License/

* Tue Jul 16 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.4.1-1jpp
- first jpp release
