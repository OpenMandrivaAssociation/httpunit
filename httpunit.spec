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

Name:		httpunit
Epoch:		0
Version:	1.7
Release:	0.0.9
Summary:	Automated web site testing toolkit
License:	MIT
Group:		Development/Java
Url:		http://httpunit.sourceforge.net/
Source0:	http://download.sourceforge.net/httpunit/httpunit-%{version}.zip
Patch0:		%{name}.build.patch
Patch1:		%{name}-JavaScript-NotAFunctionException.patch
Patch2:		%{name}-servlettest.patch

BuildRequires:	ant >= 0:1.6
BuildRequires:	jaf >= 0:1.0.2
BuildRequires:	javamail >= 0:1.3
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	jtidy
BuildRequires:	junit >= 0:3.8
BuildRequires:	locales-en
BuildRequires:	nekohtml
BuildRequires:	rhino
BuildRequires:	servlet24
BuildRequires:	unzip
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
BuildRequires:	java-devel
%endif
Requires:	jaxp_parser_impl
Requires:	jpackage-utils
Requires:	junit >= 0:3.8
# As of 1.5, requires either nekohtml or jtidy, and prefers nekohtml.
Requires:	nekohtml
Requires:	rhino
Requires:	servlet24

%description
HttpUnit emulates the relevant portions of browser behavior, including form
submission, JavaScript, basic http authentication, cookies and automatic page
redirection, and allows Java test code to examine returned pages either as
text, an XML DOM, or containers of forms, tables, and links.
A companion framework, ServletUnit is included in the package.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
Javadoc for %{name}

%package        doc
Summary:	Documentation for %{name}
Group:		Development/Java
Requires:	%{name}-javadoc

%description    doc
Documentation for %{name}

%package        demo
Summary:	Demo for %{name}
Group:		Development/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}

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
mkdir -p %{buildroot}%{_javadir}
cp -p lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

# Jar versioning
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; \
 do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# Javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr doc/api/* %{buildroot}%{_javadocdir}/%{name}

# Avoid having api in doc
rm -rf doc/api

# Fix link between doc and javadoc
pushd doc
ln -sf %{_javadocdir}/%{name}-%{version} api
popd

# Demo
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -p examples/* %{buildroot}%{_datadir}/%{name}
cp -p lib/%{name}-test.jar \
  %{buildroot}%{_datadir}/%{name}/%{name}-test-%{version}.jar
cp -p lib/%{name}-examples.jar \
  %{buildroot}%{_datadir}/%{name}/%{name}-examples-%{version}.jar

%gcj_compile

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%{_javadir}/*
%{gcj_files}

%files javadoc
%{_javadocdir}/%{name}

%files doc
%doc doc/*

%files demo
%{_datadir}/%{name}

