---

title: "Configuration"
weight: 60
layout: "single"

menu:
  main:
    identifier: "configuration"
    parent: "technical-guide"

---
# Logging

Camunda Optimize provides logging facilities that are preconfigured to use
*INFO* logging level. Which provides minimal output of information in log files.
 This level can be adjusted using `environment-logback.xml` configuration file.

Even though one could potentially configure logging levels for all packages, it
is recommended to set logging levels for optimize system only using exact package
reference as follows:

```xml
<logger name="org.camunda.optimize" level="info" />
```

In general, all log levels provided by logback are supported. Optimize itself supports the following log levels:

* *info*: shows only errors and the most important information.
* *debug*: in addition to info writes information about scheduling process, alerting as well as import into the log file.
* *trace*: as debug but in addition writes all requests sent to Engine as well as all queries towards Elasticsearch in the log file.

# System configuration

All distributions of Camunda Optimize come with a predefined set of configuration options that can be overwritten by the user, based on current environment requirements. To do that, have a look into the folder named environment. There is one file called environment-config.yaml with values that override the defaults optimize properties.

Configuration file contains YAML object each field of which is containing
configuration values of one specific logical part of Camunda Optimize system.
You can see a sample configuration file with all possible configuration fields
and their default values [here](service-config.yaml).


In the following section you will find description and default values of separate fields
inside of main YAML object with their respective YAML Path.

{{< note title="Heads Up!" class="info" >}}
For changes in the configuration to take effect, you need to restart Optimize!
{{< /note >}}


## Authentication And Security

These values control internal mechanisms of Optimize related to authentication
of users against the system and lifetime of web session tokens.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>auth.token.lifeMin</td>
    <td>15</td>
    <td>
      Optimize uses token-based authentication to keep track of which users are
      logged in. Define the lifetime of the token in minutes.
    </td>
  </tr>
</table>

## Container

Settings related to embedded Jetty container, which serves Optimize application.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>container.host</td>
    <td>localhost</td>
    <td>
      A host name or IP address, to identify a specific network interface on
      which to listen.
    </td>
  </tr>
  <tr>
    <td>container.ports.http</td>
    <td>8090</td>
    <td>
      A port number that will be used by the embedded jetty server to process
      HTTP connections.
    </td>
  </tr>
  <tr>
    <td>container.ports.https</td>
    <td>8091</td>
    <td>
      A port number that will be used by the embedded jetty server to process
      secure HTTPS connections.
    </td>
  </tr>
  <tr>
    <td>container.keystore.location</td>
    <td>keystore.jks</td>
    <td>
      HTTPS requires an SSL Certificate. When you generate an SSL Certificate,
      you are creating a keystore file and a keystore password for use when the
      browser interface connects. Location of keystore file.
    </td>
  </tr>
  <tr>
    <td>container.keystore.password</td>
    <td>optimize</td>
    <td>
      Password of keystore file.
    </td>
  </tr>
  <tr>
    <td>container.status.connections.max</td>
    <td>10</td>
    <td>
      Maximum number of web socket connections accepted for status report.
    </td>
  </tr>
</table>

## Connection to Camunda BPM platform

Configuration for engines used to import data. Please note that you have to have
at least one engine configured at all times. You can configure multiple engines
to import data from. Each engine configuration should have unique alias associated
with it and represented by ```${engineAlias}```.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>engines.${engineAlias}.name</td>
    <td>default</td>
    <td>
      The name of the engine that will be used to import data.
    </td>
  </tr>
  <tr>
    <td>engines.${engineAlias}.rest</td>
    <td>http://localhost:8080/engine-rest</td>
    <td>
      A base URL that will be used for connections to the Camunda Engine REST API.
    </td>
  </tr>
  <tr>
    <td>engines.${engineAlias}.authentication.enabled</td>
    <td>false</td>
    <td>
      Toggles basic authentication on or off. When enabling basic
      authentication, please be aware that you also need to adjust the values
      of the user and password
    </td>
  </tr>
  <tr>
    <td>engines.${engineAlias}.authentication.user</td>
    <td></td>
    <td>
      When basic authentication is enabled, this user is used to authenticate
      against the engine.

      <p>Note: when enabled, it is required that the user has
      <em>read history</em> permission on the <em>process definition</em> resource
      to enable Optimize to import the engine data.
       </p>
    </td>
  </tr>
  <tr>
    <td>engines.${engineAlias}.authentication.password</td>
    <td></td>
    <td>
      When basic authentication is enabled, this password is used to
      authenticate against the engine.
    </td>
  </tr>
  <tr>
    <td>engines.${engineAlias}.webapps.endpoint</td>
    <td>http://localhost:8080/camunda</td>
    <td>
      Defines the endpoint where to find the camunda webapps.
	  This allows Optimize to directly link
      to the other Camunda Web Applications, e.g. to jump from
      Optimize directly to a dedicated process instance in Cockpit
    </td>
  </tr>
  <tr>
    <td>engines.${engineAlias}.webapps.enabled</td>
    <td>true</td>
    <td>
      Enables/disables linking to other Camunda Web Applications
    </td>
  </tr>
</table>

## Engine Common Settings

Settings used by Optimize, which are common among all configured engines, such as
REST API endpoint locations, timeouts, etc.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>engine-commons.connection.timeout</td>
    <td>0</td>
    <td>
      Maximum time in milliseconds without connection to the engine,
      Optimize should wait until a time out is triggered. A value of zero means to wait an infinite amount of time.
    </td>
  </tr>
  <tr>
    <td>engine-commons.procdef.resource</td>
    <td>/process-definition</td>
    <td>
      The engine endpoint to the process definition.
    </td>
  </tr>
  <tr>
    <td>engine-commons.procdef.xml</td>
    <td>/xml</td>
    <td>
      The engine endpoint to the process definition xml.
    </td>
  </tr>
  <tr>
    <td>engine-commons.read.timeout</td>
    <td>0</td>
    <td>
      Maximum time a request to the engine should last,
      before a timeout triggers. A value of zero means to wait an infinite amount of time.
    </td>
  </tr>
  <tr>
    <td>engine-commons.user.validation.resource</td>
    <td>/identity/verify</td>
    <td>
      The engine endpoint for the user validation.
    </td>
  </tr>
  <tr>
    <td>import.data.activity-instance.maxPageSize</td>
    <td>10000</td>
    <td>
      Overwrites the maximum page size for historic activity instance
      fetching.
    </td>
  </tr>
  <tr>
    <td>import.data.process-definition.elasticsearchType</td>
    <td>process-definition</td>
    <td>
      Name used to identify index for storing data of process definitions
      already imported to optimize
    </td>
  </tr>
  <tr>
    <td>import.data.process-definition-xml.maxPageSize</td>
    <td>2</td>
    <td>
      Overwrites the maximum page size for process definition xml model
      fetching. Should be a low value, as large models will lead to
      memory or timeout problems.
    </td>
  </tr>
  <tr>
    <td>import.data.process-instance.maxPageSize</td>
    <td>10000</td>
    <td>
      Overwrites the maximum page size for historic process instance
      fetching.
    </td>
  </tr>
  <tr>
    <td>import.data.process-instance.elasticsearchType</td>
    <td>process-instance</td>
    <td>
      Name used to identify index storing data of imported process instances
    </td>
  </tr>
  <tr>
    <td>import.data.variable.maxPageSize</td>
    <td>10000</td>
    <td>
      Overwrites the maximum page size for historic variable instance
      fetching.
    </td>
  </tr>
  <tr>
    <td>import.elasticsearchJobExecutorThreadCount</td>
    <td>2</td>
    <td>
      Number of threads being used to process the import jobs that
      are writing data to elasticsearch.
    </td>
  </tr>
  <tr>
    <td>import.elasticsearchJobExecutorQueueSize</td>
    <td>100</td>
    <td>
      Adjust the queue size of the import jobs that store data to elasticsearch.
      A too large value might cause memory problems.
    </td>
  </tr>
  <tr>
    <td>import.handler.backoff.interval</td>
    <td>5000</td>
    <td>
      Interval in milliseconds which is used for the backoff time calculation.
    </td>
  </tr>
  <tr>
    <td>import.handler.backoff.max</td>
    <td>15</td>
    <td>
      Once all pages are consumed, the import scheduler component will
      start scheduling fetching tasks in increasing periods of time,
      controlled by "backoff" counter.
    </td>
  </tr>
  <tr>
    <td>import.handler.backoff.isEnabled</td>
    <td>true</td>
    <td>
      Tells if the backoff is enabled of not.
    </td>
  </tr>
  <tr>
    <td>import.indexType</td>
    <td>import-index</td>
    <td>
      The name of the import index type.
    </td>
  </tr>
  <tr>
    <td>import.importIndexStorageIntervalInSec</td>
    <td>10</td>
    <td>
      States how often the import index should be stored to Elasticsearch.
    </td>
  </tr>
  <tr>
    <td>import.writer.numberOfRetries</td>
    <td>5</td>
    <td>
      Number of retries when there is a version conflict in Elasticsearch
      during the import.
    </td>
  </tr>
</table>


## Elasticsearch

Settings related to the elasticsearch.

### Connection and index settings

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>es.connection.timeout</td>
    <td>10000</td>
    <td>
      Maximum time without connection to Elasticsearch, Optimize should
      wait until a time out triggers.
    </td>
  </tr>
  <tr>
    <td>es.host</td>
    <td>localhost</td>
    <td>
      A hostname on which the Elasticsearch TCP listener is available.
    </td>
  </tr>
  <tr>
    <td>es.clusterName</td>
    <td>elasticsearch</td>
    <td>
      The name of the Elasticsearch cluster Optimize should connect with.
    </td>
  </tr>
  <tr>
    <td>es.ports.tcp</td>
    <td>9300</td>
    <td>
      A port number used by Elasticsearch to accept TCP connections.
    </td>
  </tr>
  <tr>
    <td>es.ports.http</td>
    <td>9200</td>
    <td>
      A port number used by Elasticsearch to accept HTTP connections.
    </td>
  </tr>
  <tr>
    <td>es.index</td>
    <td>optimize</td>
    <td>
      An index name used to create all Camunda Optimize types, shards, etc.
    </td>
  </tr>
  <tr>
    <td>es.sampler.interval</td>
    <td>5000</td>
    <td>
      Connection sampler interval set to the client
    </td>
  </tr>
  <tr>
    <td>es.scrollTimeout</td>
    <td>60000</td>
    <td>
      Maximum time a request to elasticsearch should last, before a timeout
      triggers.
    </td>
  </tr>
  <tr>
    <td>es.settings.index.number_of_replicas</td>
    <td>1</td>
    <td>
      How often should the data replicated in case of node failure.

      <p> Note: this property only applies the first time Optimize is started and
      the schema/mapping is deployed on Elasticsearch. If you want to take
      this property to take effect again, you need to delete all indexes (with it all data)
      and restart Optimize. </p>
    </td>
  </tr>
  <tr>
    <td>es.settings.index.number_of_shards</td>
    <td>5</td>
    <td>
      How many shards should be used in the cluster.

      <p>Note: this property only applies the first time Optimize is started and
      the schema/mapping is deployed on Elasticsearch. If you want to take
      this property to take effect again, you need to delete all indexes (with it all data)
      and restart Optimize. </p>
    </td>
  </tr>
  <tr>
    <td>es.settings.index.refresh_interval</td>
    <td>2s</td>
    <td>
      How long Elasticsearch waits until the documents are available
      for search. A positive value defines the duration in seconds.
      A value of -1 means that a refresh needs to be done manually.
    </td>
  </tr>
</table>

### Security settings

Define a secured connection to be able to communicate with an Elasticsearch instance secured with x-pack.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>es.security.username</td>
    <td>elastic</td>
    <td>
      The x-pack username that has the rights to start a transport connection
    </td>
  </tr>
  <tr>
    <td>es.security.password</td>
    <td>I-love-optimize</td>
    <td>
      The password of the x-pack user
    </td>
  </tr>
  <tr>
    <td>es.security.ssl.enabled</td>
    <td>false</td>
    <td>
      Used to enable or disable TLS/SSL for both the transport and http layer.
      Also defines if a secured connection is build up at all.
    </td>
  </tr>
  <tr>
    <td>es.security.ssl.key</td>
    <td>/path/to/client.key</td>
    <td>
      The path to the PEM encoded file containing the private key.
    </td>
  </tr>
  <tr>
    <td>es.security.ssl.certificate</td>
    <td>/path/to/client.crt</td>
    <td>
     The path to a PEM encoded file containing the certificate (or certificate chain)
     that will be presented to clients when they connect.
    </td>
  </tr>
  <tr>
    <td>es.security.ssl.certificate_authorities</td>
    <td>/path/to/ca.crt</td>
    <td>
		The path to the PEM encoded certificate file that should be trusted.
        Note: if you are using a public CA that is already trusted by the Java runtime,
        you do not need to set the certificate_authorities.
    </td>
  </tr>
  <tr>
    <td>es.security.ssl.verification_mode</td>
    <td>certificate</td>
    <td>
		Controls the verification of certificates. Valid values are <em>none</em>, <em>certificate</em>, and <em>full</em>.
        See the elasticsearch security setting <em>xpack.security.transport.ssl.verification_mode</em>
        for more information about the values.
    </td>
  </tr>
</table>


## Email

Setting for the email server to send email notifications, e.g. when an alert is triggered.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>email.enabled</td>
    <td>false</td>
    <td>
      A switch to control email sending process.
    </td>
  </tr>
  <tr>
    <td>email.username</td>
    <td></td>
    <td>
      Username of your smtp server.
    </td>
  </tr>
  <tr>
    <td>email.password</td>
    <td></td>
    <td>
      Corresponding password to the given user of your smtp server.
    </td>
  </tr>
  <tr>
    <td>email.address</td>
    <td></td>
    <td>
      Email address that can be used to send notifications.
    </td>
  </tr>
  <tr>
    <td>email.hostname</td>
    <td></td>
    <td>
      The smtp server name.
    </td>
  </tr>
  <tr>
    <td>email.port</td>
    <td>587</td>
    <td>
      The smtp server port. This one is also used as SSL port for the security connection.
    </td>
  </tr>
  <tr>
    <td>email.securityProtocol</td>
    <td>None</td>
    <td>
      States how the connection to the server should be secured.
      Possible values are 'NONE', 'STARTTLS' or 'SSL/TLS'.
    </td>
  </tr>
</table>

## History Cleanup Settings

Settings for automatic cleanup of historic process instances based on their end time.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>historyCleanup.enabled</td>
    <td>false</td>
    <td>
      Switch to activate the history cleanup. [true/false]
    </td>
  </tr>
  <tr>
    <td>historyCleanup.cronTrigger</td>
    <td>'0 1 * * *'</td>
    <td>
      Cron expression to schedule when the cleanup should be executed.
      As the cleanup can cause considerable load on the underlying elasticsearch database it is recommended to schedule it outside of office hours.
      <a href="https://en.wikipedia.org/wiki/Cron">https://en.wikipedia.org/wiki/Cron</a>
    </td>
  </tr>
  <tr>
    <td>historyCleanup.ttl</td>
    <td>'P2Y'</td>
    <td>
      Global time to live (ttl) period for process instance data since their end date, when passed the process instance will get cleaned up.
      The format of the string is ISO_8601 duration. The default value is 2 years. <br /><br />
      For details on the notation refer to: <a href="https://en.wikipedia.org/wiki/ISO_8601#Durations">https://en.wikipedia.org/wiki/ISO_8601#Durations</a> <br /><br />
      Note: The time component of the ISO_8601 duration is not supported. Only years (Y), months (M) and days (D) are.
    </td>
  </tr>
  <tr>
    <td>historyCleanup.mode</td>
    <td>'all'</td>
    <td>
      Global type of te cleanup to perform, possible values: <br /><br />
      'all' - delete everything related and including the process instance that passed the defined ttl<br /><br />
      'variables' - only delete variables of a process instance
    </td>
  </tr>
  <tr>
    <tr>
    <td>historyCleanup.perProcessDefinitionConfig</td>
    <td></td>
    <td>
      A List of process definition specific configuration parameters that will overwrite the global cleanup settings
      for the specific processDefinition identified by it's ${key}.
    </td>
  </tr>
  <tr>
    <tr>
    <td>historyCleanup.perProcessDefinitionConfig.${key}.ttl</td>
    <td></td>
    <td>
      Time to live to use for process instances of the process definition with the ${key}.
    </td>
  </tr>
  <tr>
    <tr>
    <td>historyCleanup.perProcessDefinitionConfig.${key}.mode</td>
    <td></td>
    <td>
      Cleanup mode to use for process instances of the process definition with the ${key}.
    </td>
  </tr>
</table>


## Other

Settings of plugin subsystem serialization format, variable import, camunda endpoint.

<table class="table table-striped">
  <tr>
    <th>YAML Path</th>
    <th>Default Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>plugin.variableImport.basePackages</td>
    <td></td>
    <td>
      Look in the given base package list for variable import adaption plugins.
      If empty, the import is not influenced.
    </td>
  </tr>
  <tr>
    <td>plugin.authenticationExtractor.basePackages</td>
    <td></td>
    <td>
      Looks in the given base package list for authentication extractor plugins.
      If empty, the standard Optimize authentication mechanism is used.
    </td>
  </tr>
  <tr>
    <td>plugin.engineRestFilter.basePackages</td>
    <td></td>
    <td>
      Look in the given base package list for engine rest filter plugins.
      If empty, the REST calls are not influenced.
    </td>
  </tr>
  <tr>
    <td>serialization.engineDateFormat</td>
    <td>yyyy-MM-dd'T'HH:mm:ss.SSSZ</td>
    <td>
      Define a custom date format that should be used
      (should be the same as in the engine)
      please not that engine prior to 7.8 use yyyy-MM-dd'T'HH:mm:ss as default
      date format
    </td>
  </tr>
  <tr>
    <td>serialization.optimizeDateFormat</td>
    <td>yyyy-MM-dd'T'HH:mm:ss.SSSZ</td>
    <td>
      The date format that is used in Optimize internally
    </td>
  </tr>
  <tr>
    <td>export.csv.limit</td>
    <td>1000</td>
    <td>
      Maximum number of records returned by CSV export
    </td>
  </tr>
  <tr>
    <td>export.csv.offset</td>
    <td>0</td>
    <td>
      Position of first record which will be exported in CSV
    </td>
  </tr>
</table>
