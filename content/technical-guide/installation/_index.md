---

title: "Installation"
weight: 50
layout: "single"

menu:
  main:
    identifier: "installation"
    parent: "technical-guide"

---

# Installation Guide

This document describes the installation process of the Camunda Optimize distribution, as well as various configuration possibilities available after initial installation.

Before proceeding with the installation, please read the article about [supported environments]({{< ref "/introduction/supported-environments.md" >}}).

## Prerequisites

Before installing Optimize, make sure you have a JRE (Java Runtime Environment), or better, a JDK
(Java Development Kit) installed. It is required to install Java version 8.

[Download JDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)

## Full Distribution with Elasticsearch

The Optimize full distribution comes with an Elasticsearch instance. The supplied Elasticsearch server is not customized or tuned by Camunda in any manner. It is intended to make the process of trying out Optimize as easy as possible. The only requirement in addition to the full distribution itself is a running engine (ideally on localhost).

To install the full distribution containing Elasticsearch, please download the archive with the latest version from the [download page](/enterprise/download/#camunda-optimize) and extract it to the desired folder. After that, start Optimize by running the script `optimize-demo.sh` on Linux and Mac or `optimize-demo.bat` on Windows.

The script ensures that a local version of Elasticsearch is started and waits until it is up running. Then it starts Optimize, ensures it is running and opens automatically a tab in a browser to make it very convenient for you to try out Optimize.

## Standalone Distribution without Elasticsearch

This distribution is intended to be used in production. To install it, first [download](https://docs.camunda.org/enterprise/download/#camunda-optimize) the standalone archive, which contains all the required files to startup Camunda Optimize without Elasticsearch. After that [configure the Elasticsearch connection](#elasticsearch-configuration) to connect to your pre-installed Elasticsearch instance and [configure the Camunda BPM Platform connection](#camunda-bpm-configuration) to connect Optimize to your running engine. You can then start your Optimize instance by running the script `optimize-startup.sh` on Linux and Mac:
```bash
./optimize-startup.sh
```
or `optimize-startup.bat`on Windows:
```batch
.\optimize-startup.bat
```

## Usage

You can start using Optimize right away by opening the following URL in your browser: [http://localhost:8090](http://localhost:8090)

Then you can use the users from the Camunda Platform to login to Optimize. For details on how to configure the user access, please consult the [user access management]({{< ref "/technical-guide/user-management/_index.md" >}}) section.

Before you can fully utilize all features of Optimize, you need to wait until all data has been imported. A green circle in the footer indicates, when the import is finished.

## Configuration

All distributions of Optimize come with a predefined set of configuration options that can be overwritten by the user, based on current environment requirements. To do that, have a look into the folder named `environment`. There are two files, one called `environment-config.yaml` with values that override the default Optimize properties and another called `environment-logback.xml`, which sets the logging configuration.

You can see all supported values and read about logging configuration [here]({{< ref "/technical-guide/configuration/_index.md" >}}).

### Optimize Container Configuration

The following YAML Paths correspond to settings available in the environment configuration.

* container.ports.http - A port number that is used by the embedded jetty server to process HTTP connections
```
Default value: `8090`
```

* container.host - You can configure a host either by host name or IP address, to identify a specific network interface on which to listen
```
Default value: `0.0.0.0`
```

### Elasticsearch configuration

You can customize the Elasticsearch connection settings used by Optimize by changing the following properties:

* es.host - A hostname on which the Elasticsearch TCP listener is available
```
Default value: `localhost`
```

* es.clusterName - The name of the Elasticsearch cluster Optimize should connect with.
```
Default value: `elasticsearch`
```

* es.ports.tcp - A port number used by Elasticsearch to accept TCP connections
```
Default value: `9300`
```

### Camunda BPM configuration

To perform an import and provide the full set of features, Optimize requires connection to the REST API of the Camunda engine, which can be configured using the following properties.

* engines.${engineAlias}.rest - A base URL that will be used for connections to the Camunda Engine REST API
```
Default value: `http://localhost:8080/engine-rest`
```

* engines.${engineAlias}.name - The name of the engine that will be used to import data
```
Default value: `default`
```

## Import of the dataset

By default, Optimize comes without any data available. To start using all the features of the system, you have to perform a data import from the Camunda BPM Platform. This process is triggered automatically on start.

If you are interested in the details of the import, please refer to the dedicated [import overview section]({{< ref "/technical-guide/import/import-overview.md" >}}).

# Hardware Resources

According to the tests with different datasets described on [import overview page]({{< ref "/technical-guide/import/import-overview.md#import-performance-overview" >}}) we can recommend
to carefully choose hardware resources that are allocated to the server with Optimize.

{{< note title="Heads Up!" class="warning" >}}
Exact hardware requirements highly depend on a number of factors such as: size of the data,
network speed, current load on the engine and its underlying database. Therefore we cannot
guarantee that following requirements will exactly match every case.
{{< /note >}}

We recommend following minimum hardware for data sets:

* Small Size Of Data
  * 2 CPU Cores
  * 512MB RAM for Camunda Optimize
  * 2 GB RAM for Elasticsearch

* Medium Size Of Data
  * 3 CPU Cores
  * 4GB RAM for Camunda Optimize
  * 3 GB RAM for Elasticsearch

* Large Size Of Data
  * 4 CPU Cores
  * 8GB RAM for Camunda Optimize
  * 4 GB RAM for Elasticsearch

Please be aware, that Optimize is using data structures, that are different from data stored
by engine in relational database. The final amount of space on the hard drive required by Optimize will
depend on your replication settings, but as a rule of thumb you could expect Optimize to use 30% of the space that
your relational database is using.

# Recommended Additional Configurations

## Adjust engine heap size

Sending huge process definition diagrams via Rest-API might cause the engine to crash, because of the limited heap size. Thus, it is recommended to increase the heap size of the engine to at least 1 gigabyte or preferably more, e.g., by adding the following java command line property when starting the engine:
```bash
-Xmx2048m
```
