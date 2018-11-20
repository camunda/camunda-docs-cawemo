---

title: "Migration notes for upgrade from 2.1 to 2.2"
weight: 50

menu:
  main:
    identifier: "2.1-to-2.2"
    parent: "update"

---


To upgrade Optimize please perform the migration steps as described in the dedicated guide [Migration & Upgrade]({{< ref "/technical-guide/update/_index.md" >}}).

When upgrading Optimize certain features might not work out of the box for the old data. This is due to old versions of Optimize
do not fetch data that is necessary for this specific feature to work. For this upgrade the following features do not work on the old data:

* [Process Instance Parts]({{< ref "/user-guide/report/_index.md#process-instance-parts" >}}).
* [Canceled Instances Only Filter]({{< ref "/user-guide/filter/_index.md#canceled-instances-only-filter" >}}).

To enable this feature for your old data please follow the steps in the [Force reimport of engine data in Optimize]({{< ref "/technical-guide/update/_index.md#force-reimport-of-engine-data-in-optimize" >}}) guide.

