---

title: "History Cleanup"
weight: 60
layout: "single"

menu:
  main:
    identifier: "history-cleanup"
    parent: "technical-guide"

---

In order to satisfy data protection laws or just for general storage management purposes Optimize provides an automated cleanup functionality.
The cleanup is performed based on process instance data and the criteria to decide about whether an instance is to be cleaned up is based on it's end date and the configured time to live period.

## Setup

{{< note title="Heads Up!" class="warning" >}}
The cleanup is by default disabled, before enabling it though you should carefully consider what type of cleanup and what time to live period you want, otherwise historic process instance data intended for analyis might get lost irreversibly.
{{< /note >}}

The most crucial setting properties are ```ttl``` and ```mode```, their global default configuration is the following:
```
historyCleanup:
  ttl: 'P2Y'
  mode: 'all'
```

`ttl` - is the time to live period from which process instances with an end date older than that period are picked up by the cleanup process.
The default value is ```'P2Y'```, which means by default all process instances older than *2 years* at the point in time the cleanup is executed are cleaned up.
For details on the notation see the [Configuration Description](../configuration/#history-cleanup-settings) of the ttl property.

`mode` - determines what is deleted when a process instance is cleaned. The default value of ```'all'``` means the whole process instance is deleted.
For other options checkout the [Configuration Description](../configuration/#history-cleanup-settings) of the mode property.

To setup different ```ttl```s or different cleanup ```mode```s you can also provide process specific settings using the ```perProcessDefinitionConfig``` list and the process definition key.
```
historyCleanup:
  ttl: 'P2Y'
  mode: 'all'
  perProcessDefinitionConfig:
    'MyProcessDefinitionKey':
      ttl: 'P2M'
      mode: 'variables'
```
These settings overwrite the global values, are thus optional and so you are able to just override one of them for a certain process. In this particular sample the cleanup on process instances of the key ```'MyProcessDefinitionKey'``` would get cleaned up after 2 months instead of 2 years and on cleanup only their variables would get deleted instead of the whole instance.


Another important but not crucial property is that of the ```cronTrigger``` which defines at what time the cleanup should run.
```
historyCleanup:
  cronTrigger: '0 1 * * *'
```
The default is 1AM every day. To avoid any impact on daily business it is recommended to schedule the cleanup outside of business hours.
See the [Configuration Description](../configuration/#history-cleanup-settings) for further insights into this property and it's format.

Once you are confident about your cleanup configuration the last piece in the puzzle is to activate the cleanup with:
```
historyCleanup:
  enabled: true
```
Setting this property to ```true``` ultimately enables the cleanup process to be run on the next cron trigger after a full restart of the Optimize application

To summarize, here is how complete sample config might look like:
```
historyCleanup:
  enabled: true
  cronTrigger: '0 1 * * 0'
  ttl: 'P1Y'
  mode: 'variables'
  perProcessDefinitionConfig:
    'VeryConfidentProcess':
      ttl: 'P1M'
      mode: 'all'
    'KeepTwoMonthsProcess':
      ttl: 'P2M'
```
The cleanup is enabled.

It is scheduled to run every sunday at 1AM.

The global ```ttl``` applied to all process instances stored in optimize is 1 year.

The global cleanup ```mode``` performed to all process instances that passed the ttl period is to just clear their variables.

There is a process specific setup for ```'VeryConfidentProcess'``` that has a special ```ttl``` of 1 month to be used for it's process instances and those will be deleted completely due the ```'all'``` mode configured for them.

There is another process specific setup for ```'ToKeepForeverProcess'``` that has a special ```ttl``` of 2 months.