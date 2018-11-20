---

title: "Optimize Plugin System"
weight: 20

menu:
  main:
    name: "Plugins & Customization"
    identifier: "plugin-system"
    parent: "import-guide"
    pre: "Explains the principle of plugins in Optimize and how they can be added."

---

Optimize allows you adapt the import to decide which kind of data should be analyzed and to tackle technical issues.

Currently, we support:

* [Variable Import Customization](#variable-import-customization)
* [Single Sign On](#single-sign-on)
* [Engine Rest Filter](#engine-rest-filter)

Have a look at the [Optimize Examples Repository](https://github.com/camunda/camunda-optimize-examples) to see some use cases for the plugin system and how plugins can be implemented and used.

## Setup your environment

First, add the Optimize plugin to your project via maven:

```xml
<dependency>
  <groupId>org.camunda.optimize</groupId>
  <artifactId>plugin</artifactId>
  <version>{{< currentVersionAlias >}}</version>
</dependency>
```

To tell maven where to find the plugin environment, add the following repository to your project:

```xml
<repositories>
  <repository>
    <id>camunda-bpm-nexus</id>
    <name>camunda-bpm-nexus</name>
    <url>
      https://app.camunda.com/nexus/content/repositories/camunda-optimize
    </url>
  </repository>
</repositories>
```

Please note: to make this work, you need to add your nexus credentials and the server to your `settings.xml`.

## Variable Import Customization

This feature enables you to enrich or filter the variable import, e.g., if variables in Camunda contain only ids to variables in another database and you would like resolve those values to the actual values.

The Optimize plugin system contains the following interface:

```java
public interface VariableImportAdapter {

  List<PluginVariableDto> adaptVariables(List<PluginVariableDto> variables);
}
```

Implement this to adjust the variables to be imported. Given is a list of variables that would be imported if no further action is performed. The returned list is the customized list with the enriched/filtered variables that will be imported. To create new variable instances, you can use the PluginVariableDto class as data transfer object (dto), which is also contained in the plugin system. 

Please note that:

* all dto class members need to be set in order, otherwise the variable is ignored, as this may lead to problems during data analysis.
* the data from the engine is imported in batches. In particular you don't get all the variables in one go, but the method is rather called once per batch. For instance, if you have 100 000 variables in total and the batch size is 10 000 then the plugin function will be called 10 times.

Next, package your plugin into a jar file and then add the jar file to the _plugin_ folder of your Optimize directory. Finally, add the name of the base package of your custom VariableImportAdapter to the environment-config.yaml file:

```yaml
plugin:
  variableImport:
    #Look in the given base package list for variable import adaption plugins.
    #If empty, the import is not influenced.
    basePackages: []
```

The following shows an example of a customization of the variable import in the package ```optimize.plugin```, where every string variable is assigned the value 'foo':

```java
package optimize.plugin;

import org.camunda.optimize.plugin.importing.variable.PluginVariableDto;
import org.camunda.optimize.plugin.importing.variable.VariableImportAdapter;

import java.util.List;

  public class MyCustomVariableImportAdapter implements VariableImportAdapter {

  @Override
  public List<PluginVariableDto> adaptVariables(List<PluginVariableDto> list) {
    for (PluginVariableDto pluginVariableDto : list) {
      if(pluginVariableDto.getType().toLowerCase().equals("string")) {
        pluginVariableDto.setValue("foo");
      }
    }
    return list;
  }

}
```

Now when 'MyCustomVariableImportAdapter', packaged as a jar file, is added to the _plugin_ folder, we just have to add the following property to the _environment-config.yaml_ file to make the plugin work:

```yaml
plugin:
  variableImport:
    #Look in the given base package list for variable import adaption plugins.
    #If empty, the import is not influenced.
    basePackages: ['optimize.plugin']
```

If you still don't fully understand how the variable import customization works in detail, try to have a look at the [Optimize Examples Repository](https://github.com/camunda/camunda-optimize-examples#getting-started-with-variable-import-plugins).

## Single Sign On 

This feature allows you to register your own hook into the Optimize authentication system such that you can
integrate Optimize with your single sign on system. This allows you to skip the log in via the Optimize interface.

For that, the Optimize plugin system provides the following interface:
```java
public interface AuthenticationExtractor {
  
  AuthenticationResult extractAuthenticatedUser(HttpServletRequest servletRequest);
}
```

Implement this interface to extract your custom auth header from the JAX-RS servlet request, which is represented by ```servletRequest```.
With the given request you are able to extract your information both from the request header and from the request cookies.

The following example extracts a header with the name `user` and if the header exists the user name from the header is authenticated:
```java
package com.example.optimize.security.authentication;

import org.camunda.optimize.plugin.security.authentication.AuthenticationExtractor;
import org.camunda.optimize.plugin.security.authentication.AuthenticationResult;

import javax.servlet.http.HttpServletRequest;

public class AutomaticallySignInUserFromHeaderPlugin implements AuthenticationExtractor {

  @Override
  public AuthenticationResult extractAuthenticatedUser(HttpServletRequest servletRequest) {
    String userToAuthenticate = servletRequest.getHeader("user");
    AuthenticationResult result = new AuthenticationResult();
    result.setAuthenticatedUser(userToAuthenticate);
    result.setAuthenticated(userToAuthenticate != null);
    return result;
  }
}
```

As for the Variable Import Customization, you have to package your plugin in a jar, add it to the _plugin_ folder and make Optimize find it by adding the following configuration to _environment-config.yaml_:

```yaml
plugin:
  authenticationExtractor:
    # Looks in the given base package list for authentication extractor plugins.
    # If empty, the standard Optimize authentication mechanism is used.
    basePackages: ['com.example.optimize.security.authentication']
```

## Engine Rest Filter

This feature allows you to register your own filter that is called for every REST call to one of the configured process engines.
For that, the Optimize plugin system provides the following interface:
```java
public interface EngineRestFilter {
  
  void filter(ClientRequestContext requestContext, String engineAlias, String engineName) throws IOException;
}
```

Implement this interface to adjust the JAX-RS client request, which is represented by ```requestContext```, sent to the process engine's REST API.
If the modification depends on the process engine, you can analyze the value of ```engineAlias``` and/or ```engineName``` to decide what adjustment is needed.

The following example shows a filter that simply adds a custom header to every REST call:
```java
package com.example.optimize.enginerestplugin;

import java.io.IOException;
import javax.ws.rs.client.ClientRequestContext;

public class AddCustomTokenFilter implements EngineRestFilter {

  @Override
  public void filter(ClientRequestContext requestContext, String engineAlias, String engineName) throws IOException {
    requestContext.getHeaders().add("Custom-Token", "SomeCustomToken");
  }

}
```

As for the Variable Import Customization, you have to package your plugin in a jar, add it to the _plugin_ folder and make Optimize find it by adding the following configuration to _environment-config.yaml_:

```yaml
plugin:
  engineRestFilter:
    #Look in the given base package list for engine rest filter plugins.
    #If empty, the REST calls are not influenced.
    basePackages: ['com.example.optimize.enginerestplugin']
```