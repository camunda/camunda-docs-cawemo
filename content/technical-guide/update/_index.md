---

title: "Migration & Upgrade"
weight: 50

menu:
  main:
    identifier: "update"
    parent: "technical-guide"

---

Roughly every quarter of a year a new minor version of Optimize is released. These document guides you through the process of migrating your Optimize from one Optimize minor version to the other. This applies to any upgrades of the version number “after the first dot”, example: 2.1 to 2.2.

If you want to upgrade Optimize by several minor versions, you cannot do that at once but you need to perform the minor upgrades in a sequential order. For instance, if you want to upgrade from 2.1 to 2.4, you need to upgrade first from 2.1 to 2.2, then from 2.2 to 2.3 and finally from 2.3 to 2.4.

Please note that the upgrade feature is only supported from Optimize version 2.1 and onwards. To migrate from 2.0 to 2.1 please follow the [respective instructions](#migrate-from-2-0-to-2-1-only).

# Migrate instruction from 2.1 onwards

From Optimize 2.1+ you can migrate from one minor version of Optimize to the next one without loosing the data. To migrate to the latest version, please perform the following steps:

**First steps**

* Make sure that Elasticsearch has enough memory. To do that shutdown Elasticsearch and go the `config` folder of your Elasticsearch distribution. There you should find a file called `jvm.options`. Change the values of the two properties `Xms` and `Xmx` to at least `1g` so that Elasticsearch has enough memory configured. For instance, the two lines could look like the following:

```bash
-Xms1g
-Xmx1g
```
* Restart the Elasticsearch and make sure that the instance is up and running throughout the whole migration process.
* The current Optimize is shutdown, so there is a downtime during the whole migration process.
* [Back-up your Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html) instance in case something goes wrong during the migration process.  (Highly recommended, but optional)
* Make sure that you have enough storage avaialable to perform the migration. During the migration process twice the amount of the storage of the ElasticSearch data is needed. (Highly recommended)
* Back-up your `environment-config.yaml` and `environment-logback.xml` located in the `environemnt` folder of the root directory of your current Optimize in case. (Optional)

**Perform the migration**

* Go the [enterprise download page](https://docs.camunda.org/enterprise/download/#camunda-optimize) and download the new version of Optimize you want to upgrade to. For instance, if your current version is Optimize 2.2 you should download the version 2.3. Extract the downloaded archive in your prefered directory. The archive contains the Optimize application itself and the executable to upgrade Optimize from your old version to the new version.
* In the `environemnt` folder of your **current** Optimize version, you have defined all configuration defined in the `environment-config.yaml` file , e.g. for Optimize to be able to connect to the engine and Elasticsearch. Copy the old configuration file and place it in the `environment` folder of your **new** Optimize distribution. Bear in mind that the configuration settings might have changed and thus the new Optimize won't recognize your adjusted settings or complain about settings that are outdated and therefore refuses to startup. Checkout the [configuration documentation]({{< ref "/technical-guide/configuration/_index.md#system-configuration" >}}) (you might need to select the correct Optimize version) to get an overview of the allowed/possible settings and their current values. 
* Now open up a terminal and change to the `upgrade` folder of the root directory of your **new** Optimize version and run the following command (the name of the jar file depends on the version upgrade):

```bash
java -jar upgrade-optimize-from-2.X.0-to-2.Y.0.jar
```

  * During the execution the executable will output a warning to ask you to back-up your Elasticsearch data. Type 'yes' to confirm that you have backed-up the data.
  * In case there are any errors during the migration process, feel free to file a support case.
  * To get more verbose information about the upgrade, you can adjust the logging level as it is desribed in the [configuration documentation]({{< ref "/technical-guide/configuration/_index.md#logging" >}}).

**After the migration**

* It is very likely that you configured the logging of Optimize to your needs and therefore you adjusted the `environment-logback.xml` in the `environemnt` folder of the root directory of your **old** Optimize. You can now use the back-uped logging configuration and put it in the `environment` folder of the **new** Optimize to keep your logging adjustments. (Optional)
* Start the new Optimize version, as described in the [installation guide]({{< ref "/technical-guide/installation/_index.md" >}}).

**Typical erros**

* Wrong execution path: 
```bash
The upgrade has to be executed from the "upgrade" folder in the Optimize root directory!
```

     This error is stating that you should execute the upgrade jar from the `upgrade` folder of your new Optimize directory.
* Using an upgrade script that does not match your version: 
```bash
Schema version saved in Metadata does not match required [2.X.0]
```
Let's assume have Optimize 2.1 and want to upgrade to 2.3 and use the jar to upgrade from 2.2 to 2.3. Then this error occurs, because the jar expects Elasticsearch to have the schema version 2.1. Therefore, you downloaded the wrong Optimize artefact, which contained the wrong upgrade jar version.

# Migrate from 2.0 to 2.1 only

Please be aware when upgrading from 2.0 to 2.1 you cannot keep your data, which means you lose:

* all the reports, dashboard and alerts you configured so far.
* all the data you have already imported from the Camunda Platform.

To upgrade to 2.1, you can perform the following steps:

* Save the `environment-config.yaml` and the `environment-logback.xml` files from the `environment` folder.
* Delete the old version of Optimize .
* [Install Optimize.]({{< ref "/technical-guide/installation/_index.md" >}})
* Add the saved configuration files to the `environment` folder.
* Check that your configuration properties are still aligned with the [latest Optimize configuration version]({{< ref "/technical-guide/configuration/_index.md" >}}), as they might change from version to version.

Now you just have to wait until the data is imported again.

# Force reimport of engine data in Optimize

It can be the case that new features do work on data that was imported with the old version of Optimize. However, if you still want 
to use the new features on the old data, you can force a reimport of the engine data to Optimize. To do so, please perform the following
steps (this will keep all you defined reports, dashboards and alerts):

* Stop Optimize, but keep Elasticsearch running.
* Download [this executable](optimize-reimport-preparation.jar) and put it in the environment folder of your new Optimize distribution.
* Execute the `optimize-reimport-preparation.jar` with the following command:
```bash
java -jar optimize-reimport-preparation.jar
```

* Start Optimize again. Now it should import all the engine data from scratch.
