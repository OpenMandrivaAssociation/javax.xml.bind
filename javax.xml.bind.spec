%define beta b180830.0359
Name: javax.xml.bind
Version: 2.4.0
Release: 0.%{beta}.1
Group: Development/Java
Summary: An implementation of the javax.xml.bind API
Source0: https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/%{version}-%{beta}/jaxb-api-%{version}-%{beta}-sources.jar
Source1: https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/%{version}-%{beta}/jaxb-api-%{version}-%{beta}.pom
License: BSD
BuildRequires: jdk-current
BuildRequires: javapackages-local
BuildRequires: javax.activation
BuildArch: noarch

%description
An implementation of the javax.xml.bind API

%prep
%autosetup -p1 -c %{name}-%{version}
# FIXME how does the version override stuff work properly?
# We can do the right thing manually, but that seems a little
# awkward...
mv -f META-INF/versions/9/javax/xml/bind/ModuleUtil.java javax/xml/bind/ModuleUtil.java
rm -rf META-INF/versions

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

find . -name "*.java" |xargs javac --add-modules=java.activation,java.desktop -p %{_javadir}
find javax -name "*.class" -o -name "*.properties" |xargs jar cf javax.xml.bind-%{version}.jar module-info.class META-INF
cp %{S:1} javax.xml.bind-%{version}.pom

%install
mkdir -p %{buildroot}%{_javadir} %{buildroot}%{_mavenpomdir}
cp javax.xml.bind-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap javax.xml.bind-%{version}.pom javax.xml.bind-%{version}.jar

%files -f .mfiles
%{_javadir}/*.jar
