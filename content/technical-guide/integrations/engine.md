---
title: 'Camunda BPM Engine'
weight: 10
integrationversion: '1.1.1'

menu:
  main:
    identifier: 'camunda-engine'
    parent: 'integrations'
    Pre: 'This page describes how you integrate the Camunda BPM Engine with Cawemo.'
---

This plugin offers a link between a Camunda BPM Process Engine and a Cawemo instance. It syncs all deployed process definitions to the configured Cawemo account. The synced diagrams will be added to a special project with the name as configured in the plugin.

# Installation

_Note:_ If you're using Camunda BPM's stand-alone application servers skip this section and download the dependency as 
a JAR as described below.

The latest version of this plugin is {{< integrationVersion >}} and can be installed either as a Maven dependency or as 
a JAR file.

## As Maven dependency

The simplest way to install this plugin is by adding a dependency to your pom.xml:

```xml
<dependency>
  <groupId>org.camunda.bpm</groupId>
  <artifactId>cawemo-engine-plugin</artifactId>
  <version>{{< integrationVersion >}}</version>
</dependency>
```

## As JAR

Alternatively, you can also add the JAR to your classpath. To get the JAR, you should:

1. Go to [Camunda Nexus](https://app.camunda.com/nexus) and login with your credentials.
2. Go to [Browse/camunda-bpm-ee/org/camunda-bpm/cawemo-engine-plugin](https://app.camunda.com/nexus/#browse/browse:camunda-bpm-ee:org%2Fcamunda%2Fbpm%2Fcawemo-engine-plugin%2F{{< integrationVersion >}}%2Fcawemo-engine-plugin-{{< integrationVersion >}}.jar)
3. Download `cawemo-engine-plugin-{{< integrationVersion >}}.jar`

{{<img src="../nexus-repo.png">}}

Or use
[this link](https://app.camunda.com/nexus/repository/camunda-bpm-ee/org/camunda/bpm/cawemo-engine-plugin/{{< integrationVersion >}}/cawemo-engine-plugin-{{< integrationVersion >}}.jar)
that will prompt you to download if you are already logged in with the right credentials.

# Configuration

## 1. Generate an API key via Cawemo

Log in to your target Cawemo instance as the owner of your organization and create an API key from your organization settings.

{{<img src="../org-setting.png">}}

## 2. Extend your Camunda Process Engine configuration

Add the following section to your process engine configuration and replace the placeholders with actual values (see
below for the location of the configuration depending on your application server):

```xml
<plugin>
    <class>org.camunda.cawemo.plugin.CawemoEnginePlugin</class>
    <properties>
        <property name="cawemoUrl">${CAWEMO_URL}</property>
        <property name="organizationId">${ORGANIZATION_ID}</property>
        <property name="apiKey">${API_KEY}</property>
        <property name="projectName">${PROJECT_NAME}</property>
        <property name="authMode">BASIC|QUERY_PARAM</property>
        <property name="customBasicAuth">false|true</property>
    </properties>
</plugin>
```

### Parameters explained

- `cawemoUrl`: Your target Cawemo instance, e. g. https://cawemo.com

  Please keep in mind that if you're using an old version of Java 7 you might have to adapt the `https.protocols` system
  property to make the connection work with web servers that are using TLS later than 1.0, see
  [this blog entry](https://blogs.oracle.com/java-platform-group/diagnosing-tls,-ssl,-and-https).

- `organizationId`: The organizationId for the pushed diagrams.

- `apiKey`: A valid API key associated with your organizationId, created as described above.

- `projectName`: The name of the engine the pushed diagrams should be linked to. This property affects the name of the
  project in which the diagrams will be stored, e. g. "projectName Deployments".

      If you're running Camunda BPM in a cluster setup this property's value should be the same on all nodes.

- The `authMode` configuration parameter determines how the Cawemo Engine Plugin authenticates with the target Cawemo
  instance:

  - `BASIC` lets the plugin use basic access authentication via an `Authorization` header field passed with each request.
  - When choosing `QUERY_PARAM` the engine plugin appends the required credentials as query parameter to the request URL.

    It is strongly advised to use the `BASIC` option and only use query parameter authentication as a fallback solution.

- `customBasicAuth` lets you add a basic auth header on top of the query parameter authentication. Cannot be combined
  with the `BASIC` option of `authMode`. If you set this option to `true` you'll have to specify a user via a parameter
  named `customBasicAuthUser` and a password via `customBasicAuthPassword`.

## 3. Specifics for supported stand-alone application servers/Spring Boot

### JBoss AS/Wildfly

Open the `standalone.xml` of your application server, look for the `<plugins>` section and add the configuration stated
above.

Additionally, you have to add the plugin as a module. For this, copy the JAR to
`$SERVER_HOME/modules/org/camunda/bpm/cawemo-engine-plugin/main` and add a file called `module.xml` with the following
content to the same folder:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<module xmlns="urn:jboss:module:1.0" name="org.camunda.bpm.cawemo-engine-plugin">
  <resources>
    <resource-root path="cawemo-engine-plugin-{{< integrationVersion >}}.jar" />
  </resources>

  <dependencies>
    <module name="org.camunda.bpm.camunda-engine" />
    <module name="org.camunda.bpm.model.camunda-bpmn-model" />
    <module name="org.camunda.commons.camunda-commons-logging" />
  </dependencies>
</module>
```

As a last step you have to register the plugin. For this, add the following line to
`$SERVER_HOME/modules/org/camunda/bpm/camunda-engine-plugins/main/module.xml` inside the `<dependencies>` tag:

```xml
<module name="org.camunda.bpm.cawemo-engine-plugin" export="true" />
```

_Attention:_ If you're using the pre-packaged JBoss/Wildfly distribution there are two `modules` folders. The correct
one is located below `$CAMUNDA_HOME/server/$SERVER_VERSION/`.

For general information about the JBoss/Wildfly configuration see the
[Camunda BPM documentation](https://docs.camunda.org/manual/7.11/user-guide/runtime-container-integration/jboss/).

### Tomcat, IBM WebSphere & Oracle WebLogic

Open the `bpm-platform.xml` of the application server instance your Process Engine is running on, look for the
`<plugins>` section and add the configuration stated above.

Additionally, you have to copy the plugin JAR to `$SERVER_HOME/lib`.

_Attention:_ If you're using the pre-packaged Tomcat distribution there are two `lib` folders. The correct one is
located below `$CAMUNDA_HOME/server/$SERVER_VERSION/`.

For general information about the configuration via BPM Platform Deployment Descriptors see
[Camunda BPM documentation](https://docs.camunda.org/manual/7.11/reference/deployment-descriptors/).

### Spring Boot

If you're using Java configuration you have to register the engine plugin as a bean:

```java
@Bean
@Order(Ordering.DEFAULT_ORDER + 1)
public static ProcessEnginePlugin cawemoEnginePlugin() {
  CawemoEnginePlugin plugin = new CawemoEnginePlugin();
  plugin.setCawemoUrl(${CAWEMO_URL});
  plugin.setOrganizationId(${ORGANIZATION_ID});
  plugin.setApiKey(${API_KEY});
  plugin.setProjectName(${PROJECT_NAME});
  plugin.setAuthMode("BASIC"|"QUERY_PARAM");
  plugin.setCustomBasicAuth(false|true);

  return plugin;
}
```

If you're using Spring XML config, open the XML file and add the configuration stated above.

If you want to install the plugin via a JAR you can use it's `-Dloader.path` option (see
[the Spring Boot documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/executable-jar.html#executable-jar-launching)).

For general information about the configuration via Spring XML see the
[Camunda BPM documentation](https://docs.camunda.org/manual/7.11/user-guide/spring-framework-integration/configuration/#configure-a-process-engine-plugin).

# Compatibility

<table class="table table-striped">
 <tr>
   <th>Cawemo</th>
   <th>Cawemo Engine Plugin</th>
   <th>Camunda BPM Engine</th>
 </tr>
  <tr>
    <td>1.5</td>
    <td>1.1.x</td>
    <td>7.12.x - 7.14.x</td>
  </tr>  
  <tr>
    <td>1.4</td>
    <td>1.1.x</td>
    <td>7.11.x - 7.14.x</td>
 </tr>
 <tr>
    <td>1.3</td>
    <td>1.1.x</td>
    <td>7.10.x - 7.13.x</td>
 </tr>
 <tr>
    <td>1.2</td>
    <td>1.1.x</td>
    <td>7.10.x - 7.13.x</td>
 </tr>
 <tr>
   <td>1.1</td>
   <td>1.1.x</td>
   <td>7.9.x - 7.12.x</td>
 </tr>
  <tr>
    <td>1.0</td>
    <td>1.0</td>
    <td>7.9.x - 7.12.x</td>
  </tr>
</table>

# Note

This plugin might have an impact on a process engine's performance when you're synchronizing process definitions
possessing a lot of versions that are not available on Cawemo as milestones yet. For each of these missing versions
the plugin performs a ProcessDefinitionQuery causing the definition to be loaded into the engine's cache and potentially
replacing others which should preferably be retained in the cache.
