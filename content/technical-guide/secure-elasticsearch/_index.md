---

title: "Secure Elasticsearch"
weight: 50

menu:
  main:
    identifier: "secure-elasticsearch"
    parent: "technical-guide"

---

It is possible to connect Optimize to an Elasticsearch instance or cluster which is secured by the Elasticsearch extension X-Pack. Bear in mind that X-Pack is an enterprise feature of Elasticsearch and might require to obtain a license before it can be used in a commercical context.

**Secure Elasticsearch**

All the information about how to install X-Pack to secure Elasticsearch can be found at the [Installing X-Pack in Elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/reference/6.0/installing-xpack-es.html#installing-xpack-es). Please follow the steps 1 to 5.

Some comments on the guide:

* To secure Elasticsearch should have added the at least the following settings to the Elasticsearch configuration file `elasticsearch.yml` in the config folder of your Elasticsearch distribution (please adjust the values):

    ```
    xpack.ssl.key: path/to/client.key
    xpack.ssl.certificate: path/to/client.crt
    xpack.ssl.certificate_authorities: path/to/ca.crt
    xpack.security.transport.ssl.enabled: true
    xpack.security.http.ssl.enabled: true
    xpack.security.transport.ssl.verification_mode: certificate
    ```
   
* If you want to use hostname verification within your cluster, run the `certutil cert` command once for each of your nodes and provide the --name, --dns and --ip options. 
* If you used the --dns or --ip options with the certutil cert command and you want to enable strict hostname checking, set the [verification mode](https://www.elastic.co/guide/en/elasticsearch/reference/6.0/security-settings.html#ssl-tls-settings) to `full`. Otherwise the verification mode needs to be set to `certificate`. The respective Elasticsearch setting is called `xpack.security.transport.ssl.verification_mode` and needs to be added to the `elasticsearch.yml` configuration file.
* It is recommended to set up a user just for optimize, which has only the necessary rights to execute queries in Elasticsearch. For instance, you could add
an `optimize` user with the password `IloveOptimize` and give him the `superuser` rights by executing the following command in the Elasticsearch root directory:

     ```
     ./bin/x-pack/users useradd optimize -p IloveOptimize -r superuser
     ```
     Note: Although the `superuser` role does allow Optimize to communicate with the secured Elasticsearch instance, this role also grants full access to the cluster. A user with the superuser role can also manage users, roles and impersonate any other user in the system and might be a security risk for your system.


**Enable Optimize to connect to the secured Elasticsearch instance**

To connect to the secured Elasticsearch Optimize needs a dependency - the x-pack transport client library. Since this is part of the Elasticsearch commercial license, Optimize is unfortunately not able to ship this libary automatically with the artefact. Therefore, you need to add the library and its dependency manually. To do that, download the following jar files from the given pages and place them in the `plugin` folder of the Optimize distribution:

* [x-pack-transport](https://artifacts.elastic.co/maven/org/elasticsearch/client/x-pack-transport/6.0.0/x-pack-transport-6.0.0.jar)
* [x-pack-api](https://artifacts.elastic.co/maven/org/elasticsearch/plugin/x-pack-api/6.0.0/x-pack-api-6.0.0.jar)
* [unboundid-ldapsdk](http://central.maven.org/maven2/com/unboundid/unboundid-ldapsdk/3.2.0/unboundid-ldapsdk-3.2.0.jar)
* [bcpkix-jdk15on](http://central.maven.org/maven2/org/bouncycastle/bcpkix-jdk15on/1.55/bcpkix-jdk15on-1.55.jar)
* [owasp-java-html-sanitizer](http://central.maven.org/maven2/com/googlecode/owasp-java-html-sanitizer/owasp-java-html-sanitizer/r239/owasp-java-html-sanitizer-r239.jar)
* [guava](http://central.maven.org/maven2/com/google/guava/guava/16.0.1/guava-16.0.1.jar)
* [elasticsearch-rest-client-sniffer](http://central.maven.org/maven2/org/elasticsearch/client/elasticsearch-rest-client-sniffer/6.0.0/elasticsearch-rest-client-sniffer-6.0.0.jar)
* [super-csv](http://central.maven.org/maven2/net/sf/supercsv/super-csv/2.4.0/super-csv-2.4.0.jar)

Now that you have configured your Elasticsearch instance and added the necessary dependencies to Optimize, you need to setup the connection security settings accordingly
to allow Optimize to connect to the secured Elasticsearch instance. All the necessary settings can be found in the 
[configuration guide]({{< ref "/technical-guide/configuration/_index.md#security-settings" >}}). Bear in mind that 
the verification mode in Elasticsearch and Optimize must have the same value.



