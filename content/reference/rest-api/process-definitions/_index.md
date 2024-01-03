---
title: 'Process Definitions'
weight: 80

menu:
  main:
    identifier: 'rest-api-process-definitions'
    parent: 'rest-api'
---

See the list of all available [HTTP methods](#methods) for this resource at end of this page.

# Resource Representation

```json
{
  "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<bpmn:definitions xmlns:bpmn=\"http://www.omg.org/spec/BPMN/20100524/MODEL\" xmlns:bpmndi=\"http://www.omg.org/spec/BPMN/20100524/DI\" xmlns:dc=\"http://www.omg.org/spec/DD/20100524/DC\" id=\"Definitions_1\" targetNamespace=\"http://bpmn.io/schema/bpmn\" xmlns:camunda=\"http://camunda.org/schema/1.0/bpmn\" camunda:diagramRelationId=\"7481b562-5fc4-498c-8735-514740576936\">\n  <bpmn:process id=\"Process_3ef3f8f4-0956-488c-930e-e61e1ab3d3f5\" isExecutable=\"true\">\n    <bpmn:startEvent id=\"StartEvent_1\" />\n  </bpmn:process>\n  <bpmndi:BPMNDiagram id=\"BPMNDiagram_1\">\n    <bpmndi:BPMNPlane id=\"BPMNPlane_1\" bpmnElement=\"Process_1\">\n      <bpmndi:BPMNShape id=\"_BPMNShape_StartEvent_2\" bpmnElement=\"StartEvent_1\">\n        <dc:Bounds x=\"150\" y=\"100\" width=\"36\" height=\"36\" />\n      </bpmndi:BPMNShape>\n    </bpmndi:BPMNPlane>\n  </bpmndi:BPMNDiagram>\n</bpmn:definitions>\n",
  "created": 1576453532000,
  "key": "def751d7-eccd-4f94-952e-f62988cef786",
  "name": "My First Process Definition",
  "updated": 1608075932000,
  "version": 1
}
```

<table class="table table-striped">
 <tr>
   <th>Name</th>
   <th>Type</th>
   <th>Description</th>
 </tr>
  <tr>
    <td>content</td>
    <td>string</td>
    <td>The process definition's BPMN 2.0 XML representation.</td>
  </tr>
  <tr>
    <td>created</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Creation time of the process definition.</td>
  </tr>
  <tr>
    <td>key</td>
    <td>string</td>
    <td>Key of the process definition, i.e., the id of the BPMN 2.0 XML process definition.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the process definition.</td>
  </tr>
  <tr>
    <td>updated</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Time when the process definition was last updated.</td>
  </tr>
  <tr>
    <td>version</td>
    <td>number</td>
    <td>The version of the process definition.</td>
  </tr>
</table>

# Methods
