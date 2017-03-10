%{?_javapackages_macros:%_javapackages_macros}

Summary:	A 100% pure-Java implementation of the MySpell spell checker
Name:		jmyspell-core
Version:	1.0.0
Release:	1
License:	LGPLv2.1
Group:		Development/Java
URL:		https://kenai.com/projects/jmyspell
Source0:	https://kenai.com/projects/jmyspell/downloads/download/JMySpell%20beta%202/jmyspell-core-src.zip
BuildArch:	noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

%description
JMySpell is a spell-checker for Java applications, capable of seamlessly
incorporating the existing OpenOffice.org dictionaries. Based on MySpell
(but written in 100% Java).

This allows us to use the old dictionaries from OpenOffice.org in Java
applications, whether they're J2SE applications or J2EE web applications.

Since at the moment there is only one 100% Java Open-Source spell checker
(Jazzy), and the inclusion of dictionaries is difficult, the objective of
this project is to fill this gap.

This package contains the JMySpell core library.

%files -f .mfiles

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -c %{name}-%{version}
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Remove parent
%pom_remove_parent

# Fix version
%pom_xpath_replace pom:project/pom:version "<version>%{version}</version>"

# Fix plugin missing version warnings
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-compiler-plugin']]" "<version>any</version>"

# Bundle
%pom_xpath_replace "pom:project/pom:packaging" "<packaging>bundle</packaging>" .

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -- -Dproject.build.sourceEncoding=ISO-8859-1

%install
%mvn_install

