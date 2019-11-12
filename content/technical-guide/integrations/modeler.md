---
title: 'Camunda Modeler'
weight: 10
integrationversion: '1.0.0'

menu:
  main:
    identifier: 'camunda-modeler'
    parent: 'integrations'
    Pre: 'This page describes how you integrate the Camunda Modeler with Cawemo.'
---

For integrating the Camunda Modeler with Cawemo we offer a Modeler plugin that can be installed individually. This plugin syncs all BPMN files that were once exported from Cawemo back into a special project inside Cawemo for the configured user. This way, a copy of each file is stored in Cawemo whenever they are saved in the Modeler.

# Installation

The latest version of this plugin is {{< integrationVersion >}} and can be installed by downloading and extracting a .zip file.

## Download

You can download the current version of the plugin here: https://camunda.org/enterprise-release/cawemo/cloud-connect-modeler-plugin/cloud-connect-{{< integrationVersion >}}.zip

Should you require a different version, you can look for it here: https://camunda.org/enterprise-release/cawemo/cloud-connect-modeler-plugin/

## Extract

Extract the downloaded `cloud-connect-{{< integrationVersion >}}.zip` into it's own folder, into your Camunda Modeler `plugins folder` (example: `".../plugins/cloud-connect/"` should then contain the contents of the .zip file you downloaded), depending on the operating system you are using you can find your `plugins folder` here:

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

If the plugin was installed successfully, you should see a `Cloud-Connect` menu entry in the plugins menu of the Camunda Modeler, next time you start it up.

# Configuration

The plugin can be configured in the Camunda Modeler itself, after successful plugin installation, the "Cloud Connect" menu point should show up under the "Plugins" section of the Application menu. Here you can select the "configuration" item and the configuration window should show up.

[comment]: <> (Placeholder for a screenshot of the configuration modal)

You can find the needed information for the configuration in the `Settings page` in `Cawemo` of the desired organization where you want to upload your diagrams to.

# Usage

To sync a file from the Camunda Modeler to Cawemo you open a `.bpmn` file which you previously downloaded from Cawemo, make a modification to the diagram and save it. After saving your diagram will be uploaded back to Cawemo. It will be added to a special project for the Cawemo user that is configured in the plugin. This project will be listed in the [Home view](../../../user-guide/home/) and the diagrams will show up in the `Related Diagrams` section of the [Milestone view](../../../user-guide/milestones/).

[comment]: <> (Placeholder for describing what will happen to continuous updated to a diagram which already exists as a diagram in the `Camunda Modeler Project`, e.g. they will at some point provoke a new milestone instead of creating a whole new diagram )

# Compatibility

| Cawemo 	| Cloud Connect Plugin 	| Camunda Modeler 	|
|:------:	|:--------------------:	|:---------------:	|
| 1.0 	| - 	| - 	|
| 1.1 	| 1.0 	| 3.4.x 	|

# Note

The technical name of this plugin is `cloud connect`. In its current version, the plugin only connects to Cawemo and not to Camunda Cloud. In a future version, this might be subject to change, but for now it can only be used to sync diagrams to Cawemo.
