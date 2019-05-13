%define beta b180830.0359
Name: javax.xml.bind
Version: 2.4.0
Release: 0.%{beta}.2
Group: Development/Java
Summary: An implementation of the javax.xml.bind API
Source0: https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/%{version}-%{beta}/jaxb-api-%{version}-%{beta}-sources.jar
Source1: https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/%{version}-%{beta}/jaxb-api-%{version}-%{beta}.pom
License: BSD
BuildRequires: jdk-current
BuildRequires: javapackages-local
BuildRequires: jmod(java.activation)
BuildRequires: jmod(java.desktop)
BuildArch: noarch

%description
An implementation of the javax.xml.bind API

%package javadoc
Summary: Javadoc documentation for javax.xml.bind
Group: Development/Java

%description javadoc
Javadoc documentation for javax.xml.bind

%prep
%autosetup -p1 -c %{name}-%{version}
# FIXME how does the version override stuff work properly?
# We can do the right thing manually, but that seems a little
# awkward...
mv -f META-INF/versions/9/javax/xml/bind/ModuleUtil.java javax/xml/bind/ModuleUtil.java
rm -rf META-INF/versions
# Fix javadoc for HTML5
find . -name "*.java" |xargs sed -i -e 's,<a name=,<a id=,g'
# @apiNote and @implNote seem to be gone in OpenJDK 12?
sed -i -e 's,@apiNote,,g;s,@implNote,,g' javax/xml/bind/JAXBContext.java

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

find . -name "*.java" |xargs javac --add-modules=java.activation,java.desktop -p %{_javadir}/modules
find javax -name "*.class" -o -name "*.properties" |xargs jar cf javax.xml.bind-%{version}.jar module-info.class META-INF
javadoc -d docs -sourcepath . --add-modules=java.activation --module-path=$(ls %{_javadir}/javax.activation-*.jar) javax.xml.bind
cp %{S:1} javax.xml.bind-%{version}.pom

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp javax.xml.bind-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap javax.xml.bind-%{version}.pom javax.xml.bind-%{version}.jar
mv %{buildroot}%{_javadir}/*.jar %{buildroot}%{_javadir}/modules
ln -s modules/javax.xml.bind-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/javax.xml.bind-%{version}.jar %{buildroot}%{_javadir}/javax.xml.bind.jar
cp -a docs %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%{_javadir}/*.jar
%{_javadir}/modules/*.jar

%files javadoc
%{_javadocdir}/%{name}
