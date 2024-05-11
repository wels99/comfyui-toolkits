import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "toolkits.randseed",
  async nodeCreated(node, app) {
    if (node.comfyClass == "randseed") {
      const v = node.widgets.find((w) => w.name === "种子");
      if (v.value == 0) {
        v.value = Math.floor(Math.random() * Number.MAX_SAFE_INTEGER);
      }
    }
  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name == "randseed") {
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        for (const key in message) {
          if (message.hasOwnProperty(key)) {
            const widget = this.widgets.find((w) => w.name === key);
            widget.value = message[key][0];
          }
        }
      };
    }
  },
});
