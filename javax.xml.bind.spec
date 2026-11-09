Name:		javax.xml.bind
Version:	2.4.0
Release:	1
Summary:	Java API for XML Binding
Group:		Development/Java
# Dual license: CDDL 1.1 or GPL-2.0 with the Classpath exception.
License:	CDDL or GPLv2 with exceptions
URL:		https://javaee.github.io/jaxb-v2/
# Maven coordinate javax.xml.bind:jaxb-api:2.4.0-b180830.0359.
# The sources jar contains Java sources only.
Source0:	https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/2.4.0-b180830.0359/jaxb-api-2.4.0-b180830.0359-sources.jar

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	mvn(javax.activation:javax.activation-api)

%description
JAXB API, the javax.xml.bind types. XStream's Base64JAXBCodec calls
DatatypeConverter. This is the 2.4.0-b180830.0359 API, built with
sysjar. The previous package targeted the old javapackages layout and
does not compile on the current JDK.

%prep
%setup -q -c -T -n jaxb-api-%{version}
jar xf %{SOURCE0}

%build
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH=$JAVA_HOME/bin:$PATH
# module-info requires java.activation, which the current JDK does not
# ship. Activation types come from javax-activation instead.
# META-INF/versions/9 repeats ModuleUtil for the multi-release jar.
find . -name '*.java' ! -name module-info.java ! -path './META-INF/*' > sources.list
mkdir -p classes
javac --release 8 -encoding UTF-8 -Xlint:-options -d classes @sources.list
find javax -name '*.properties' | while read -r prop; do
	mkdir -p "classes/$(dirname "$prop")"
	cp "$prop" "classes/$prop"
done
jar cf %{name}.jar -C classes .
cat > %{name}.pom <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>javax.xml.bind</groupId>
  <artifactId>jaxb-api</artifactId>
  <version>2.4.0.b180830.0359</version>
  <name>JAXB API</name>
  <description>Java API for XML Binding.</description>
  <url>https://javaee.github.io/jaxb-v2/</url>
  <licenses>
    <license>
      <name>CDDL 1.1 or GPL-2.0 with the Classpath exception</name>
      <url>https://oss.oracle.com/licenses/CDDL+GPL-1.1</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>javax.activation</groupId>
      <artifactId>javax.activation-api</artifactId>
      <version>1.2.0</version>
    </dependency>
  </dependencies>
</project>
EOF

%check
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH=$JAVA_HOME/bin:$PATH
mkdir -p check
cat > check/Smoke.java <<'END'
import javax.xml.bind.DatatypeConverter;
public class Smoke {
	public static void main(String[] args) {
		if (!DatatypeConverter.parseBoolean("1")) {
			throw new AssertionError("parseBoolean");
		}
		byte[] raw = DatatypeConverter.parseBase64Binary("Z3JhZGxl");
		if (raw.length != 6 || raw[0] != 'g') {
			throw new AssertionError("parseBase64Binary");
		}
		System.out.println("ok");
	}
}
END
javac --release 8 -encoding UTF-8 -Xlint:-options -cp %{name}.jar -d check check/Smoke.java
test "$(java -cp check:%{name}.jar Smoke)" = ok

%install
sysjar install --buildroot %{buildroot} \
	--artifact %{name}.pom:%{name}.jar \
	--file-name %{name} \
	--filelist .mfiles

%files -f .mfiles
%doc META-INF/LICENSE.txt
