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

The **cloud-connect** modeler plugin offers a link between the Camunda Modeler and a Cawemo instance. It syncs all BPMN files that were once exported from Cawemo back into a special project inside Cawemo for the configured user. This way, a copy of these files is stored in Cawemo whenever they are saved in the Modeler.

# Installation

To install the plugin, unzip the `cloud-connect` folder into your Camunda Modeler `plugins folder`, depending on the operating system you are using you can find your `plugins folder` here:

#### Windows:

```
%APPDATA%/camunda-modeler/plugins
```

#### Linux:

```
$XDG_CONFIG_HOME/camunda-modeler/plugins
```

or

```
~/.config/camunda-modeler/plugins
```

#### Mac OS:

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

The plugin can be configured in the Camunda Modeler itself, after successful plugin installation, the "Cloud Connect" menu point should show up under the "Plugins" section of the Application menu. Here you can select the "configuration" item and the following window should open up:

[comment]: <> (Placeholder for a screenshot of the configuration modal)

You can find the needed information for the configuration in the `Settings page` in `Cawemo` of the desired organization where you want to upload your diagrams to.

# Usage

To use `Cloud-Connect` you open a `.bpmn` file which you previously downloaded from Cawemo, make a modification to the diagram and save it. After saving your diagram will uploaded back to Cawemo, it will get created in a special project where only diagrams uploaded from the `Camunda Modeler` take place.

[comment]: <> (Placeholder for describing what will happen to continous updated to a diagram which already exists as a diagram in the `Camunda Modeler Project`, e.g. they will at some point provoke a new milestone instead of creating a whole new diagram )
