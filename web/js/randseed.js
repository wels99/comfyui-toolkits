import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// Displays input text on a node
app.registerExtension({
  name: "toolkits.randseed",
  async nodeCreated(node, app) {
    if (node.comfyClass == "randseed") {
      const v = node.widgets.find((w) => w.name === "value");
      if (v.value == 0) {
        console.log("初始化node");
        v.value = Math.floor(Math.random() * Number.MAX_SAFE_INTEGER);
      }
    }

    // if (node.properties["Node name for S&R"] == "randseed") {
    //   console.log(node);
    // }
  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name == "randseed") {
      console.log(nodeType);
      console.log(nodeData);
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        const v = this.widgets.find((w) => w.name === "value");
        v.value = message["value"][0];
        const lv = this.widgets.find((w) => w.name === "last_value");
        lv.value = message["last_value"][0];
      };
    }

    if (nodeData.name === "XXXXXXXXX") {
      function populate(text) {
        if (this.widgets) {
          for (let i = 1; i < this.widgets.length; i++) {
            this.widgets[i].onRemove?.();
          }
          this.widgets.length = 1;
        }

        const v = [...text];
        if (!v[0]) {
          v.shift();
        }
        for (const list of v) {
          const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
          w.inputEl.readOnly = true;
          w.inputEl.style.opacity = 0.6;
          w.value = list;
        }

        requestAnimationFrame(() => {
          const sz = this.computeSize();
          if (sz[0] < this.size[0]) {
            sz[0] = this.size[0];
          }
          if (sz[1] < this.size[1]) {
            sz[1] = this.size[1];
          }
          this.onResize?.(sz);
          app.graph.setDirtyCanvas(true, false);
        });
      }

      // When the node is executed we will be sent the input text, display this in the widget
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        populate.call(this, message.text);
      };

      const onConfigure = nodeType.prototype.onConfigure;
      nodeType.prototype.onConfigure = function () {
        onConfigure?.apply(this, arguments);
        if (this.widgets_values?.length) {
          populate.call(this, this.widgets_values);
        }
      };
    }
  },
});
