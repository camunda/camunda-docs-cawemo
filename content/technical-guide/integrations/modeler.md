---
title: 'Camunda Modeler'
weight: 10
integrationversion: '3.0.0'

menu:
  main:
    identifier: 'camunda-modeler'
    parent: 'integrations'
    Pre: 'This page describes how you integrate the Camunda Modeler with Cawemo.'
---

For integrating the Camunda Modeler with Cawemo we offer a Modeler plugin that can be installed individually. This plugin syncs all BPMN files that were once exported from Cawemo back into a special project inside Cawemo for the configured user. This way, a copy of each file is stored in Cawemo whenever they are saved in the Modeler.
In addition, the plugin downloads all published element templates from Cawemo so that they can be used in the Modeler.

# Installation

The latest version of this plugin is {{< integrationVersion >}} and can be installed by downloading and extracting a .zip file.

## Download

You can download the current version of the plugin here: https://camunda.org/enterprise-release/cawemo/cloud-connect-modeler-plugin/cloud-connect-{{< integrationVersion >}}.zip

Should you require a different version, you can look for it here: https://camunda.org/enterprise-release/cawemo/cloud-connect-modeler-plugin/

## Extract

Extract the downloaded `cloud-connect-{{< integrationVersion >}}.zip` into its own folder inside your Camunda Modeler `plugins folder` (example: `".../plugins/cloud-connect/"` should then contain the contents of the .zip file you downloaded). Depending on the operating system you are using you can find your `plugins folder` here:

### Windows:

```
%APPDATA%/camunda-modeler/plugins
```

### Linux:

```
$XDG_CONFIG_HOME/camunda-modeler/plugins
```

or

```
~/.config/camunda-modeler/plugins
```

### Mac OS:

```
~/Library/Application Support/camunda-modeler/plugins
```

or

```
/Users/{USER_NAME}/Library/Application Support/camunda-modeler/plugins
```

[comment]: <> (Placeholder for a screenshot of the folder structure)

If the plugin was installed successfully, you should see a `Cloud Connect` menu entry in the plugins menu of the Camunda Modeler, next time you start it up.

# Configuration

You can configure the plugin directly in the Camunda Modeler. After successful plugin installation, a new entry “Cloud Connect” should appear under the “Plugins” section of the application menu. Select “Configure” to open the configuration window.

{{<img src="../cloud-connect-configure.png">}}

To use the plugin, you need to provide the Cawemo endpoint, your user’s ID, and an API key.

The _Cawemo endpoint_ is the domain/hostname of your Cawemo installation. If you are using the On-Premise version, this may depend on your company's setup. Otherwise, for Cawemo SaaS, enter `https://cawemo.com`.

You can find your user's ID and the API key on the `Settings page` in Cawemo of the desired organization you want to upload your diagrams to.

{{<img src="../cawemo-settings-page.png">}}

### Sync Catalog Projects

Enabling this option will fetch templates from one or more Cawemo _Catalog projects_ and make them available in the Modeler. For matching elements of your BPMN diagram you can choose and apply a template from within the properties panel.

### Sync Diagrams

This option pushes diagrams from Camunda Modeler into Cawemo if they were once exported from Cawemo.

# Usage

{{< note title="Heads Up!" class="warning" >}}
On Cawemo SaaS, your organization needs to have an Enterprise license enabled for these features to work.
{{< /note >}}

### Sync Catalog Projects

1. Create a new template in Cawemo.
2. Fill out your desired input/output parameters, the name, a Service task label, and save the template.
3. Open the Modeler and create a new BPMN diagram.
4. Insert a Service task and open the Properties panel on the righthand side.
5. You should see a dropdown "Element templates" from which you can choose a template that will then be applied to the Service task.

### Sync Diagrams

1. Create a new BPMN diagram in Cawemo.
2. Download it to your computer and open it in the Modeler.
3. Make modifications to the diagram and save it.
4. The diagram will be pushed back to Cawemo, but into a separate _Modeler project_ for the Cawemo user that is configured in the plugin. This project will be listed in the [Home view](../../../user-guide/home/), and the diagrams will show up in the `Related Diagrams` section of the [Milestone view](../../../user-guide/milestones/).

[comment]: <> (Placeholder for describing what will happen to continuous updated to a diagram which already exists as a diagram in the `Camunda Modeler Project`, e.g. they will at some point provoke a new milestone instead of creating a whole new diagram )

# Compatibility

<table class="table table-striped">
 <tr>
   <th>Cawemo</th>
   <th>Cloud Connect Plugin</th>
   <th>Camunda Modeler</th>
 </tr>
  <tr>
    <td>1.6</td>
    <td>3.0</td>
    <td>4.7 or newer</td>
  </tr>
  <tr>
    <td>1.5</td>
    <td>3.0</td>
    <td>4.5 or newer</td>
  </tr>
  <tr>
    <td>1.4</td>
    <td>2.0</td>
    <td>4.3 or newer</td>
  </tr>
  <tr>
    <td>1.3</td>
    <td>1.0</td>
    <td>4.x or newer</td>
  </tr>
  <tr>
    <td>1.2</td>
    <td>1.0</td>
    <td>3.7.x or newer</td>
  </tr>
 <tr>
   <td>1.1</td>
   <td>1.0</td>
   <td>3.4.x or newer</td>
 </tr>
  <tr>
    <td>1.0</td>
    <td>-</td>
    <td>-</td>
  </tr>              
</table>

# Note

The technical name of this plugin is `cloud connect`. In its current version, the plugin only connects to Cawemo and not to Camunda Cloud. In a future version, this might be subject to change, but for now it can only be used to sync diagrams to Cawemo.
