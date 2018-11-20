---

title: "Multiple Engines"
weight: 20

menu:
  main:
    name: "Multiple Engines"
    identifier: "multiple-engines"
    parent: "import-guide"
    pre: "Shows how to set up different multiple engine scenarios with Optimize."

---

There are two possible setups where multiple engines can be used:

* [Multiple engines with a shared database](#multiple-engines-with-a-shared-database)
* [Multiple engines with a distributed database](#multiple-engines-with-a-distributed-database)

Please check which scenario corresonds to your setup, because the configuration of multiple engines to Optimize is not always suited for the best import performance.

{{< note title="Heads Up!" class="warning" >}}
There is one restriction for the multiple engines feature: 
The engines are assumed to have distinct process definitions, which means that the one process definition (same key and version) is not deployed on two or more engines at the same time.
{{< /note >}}

# Multiple engines with a shared Database

In this scenario you have multiple engines distributed in a cluster, where each engine instance is connected to a shared database. See the following diagram for an illustration:

{{< img src="../img/Clustered-Engine-Shared-Database.png" title="Clustered Engine with shared Database" >}}

Now it could be possible to connect each engine to Optimize. However, the would conclude that Optimize imports the data from each engine. Since every engine accesses the same data through the shared database, Optimize would import the engine data multiple times. What is more desired in this scenario is to balance the work load on each engine during the import. Therefore, it is adviced to place a load balancer between the engines and Optimize. Thus, Optimize would only communicate to the load balancer. The following diagram depicts the described setup:

{{< img src="../img/Multiple-Engine-Shared-Database.png" title="Multiple Engines with shared Database connected to Optimize" >}}

# Multiple engines with a distributed Database

In this scenario you have multiple engines distributed in a cluster, but this time each engine has its own database. See the following diagram for an illustration:

{{< img src="../img/Clustered-Engine-Distributed-Database.png" title="Clustered Engine with distributed Database" >}}

Now you are able to connect each engine to Optimize. The data will then automatically be imported into Optimize. The following diagramm depicts the setup:

{{< img src="../img/Multiple-Engine-Distributed-Database.png" title="Multiple Engines connected to Optimize, each having its own Database" >}}

In order to set up the connections to the engines, you need add the information to the [configuration file]({{< ref "/technical-guide/configuration/_index.md" >}}). For the sake of simplicity, let's assume we have two departments, sales and marketing, each having their own engine with its own database and processes. Both are accessible in the local network. The sales engine has the port `8080` and the marketing engine the port `1234`. Now an excerpt of the configuration could look as follows:
```yaml
engines:
  sales:
    name: default
    rest: http://localhost:8080/engine-rest
    authentication:
      enabled: false
      password: ''
      user: ''
    enabled: true
  marketing:
    name: default
    rest: http://localhost:1234/engine-rest
    authentication:
      enabled: false
      password: ''
      user: ''
    enabled: true
```

`sales` and `marketing` are custom names that we chose in order to later on distinguish from where the data was originally imported.
