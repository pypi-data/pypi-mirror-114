<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="node" :class="[selected(), node.type]">
    <div class="mx-3 mb-3 text-center" v-if="node.type !== 'source'">
      <strong>{{ node.name }}</strong>
    </div>
    <div class="content">
      <!-- Inputs-->
      <div class="column" v-if="node.inputs.size > 0">
        <div class="input" v-for="input in inputs()" :key="input.key">
          <socket v-socket:input="input"
                  type="input"
                  :editor="editor"
                  :socket="input.socket"
                  :used="input.connections.length > 0"
                  :multi="input.multipleConnections">
          </socket>
          {{ input.name }} <strong v-if="input.param && input.param.required">*</strong>
        </div>
      </div>
      <!-- Controls-->
      <div class="column" v-if="node.controls.size > 0">
        <div class="control" v-for="control in controls()" :key="control.key" v-control="control"></div>
      </div>
      <!-- Outputs-->
      <div class="column" v-if="node.outputs.size > 0">
        <div class="output" v-for="output in outputs()" :key="output.key">
          {{ output.name }}
          <socket v-socket:output="output"
                  type="output"
                  :editor="editor"
                  :socket="output.socket"
                  :used="output.connections.length > 0"
                  :multi="output.multipleConnections">
          </socket>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

$bg-builtin: #f7f7f7;
$bg-env: #478e59;
$bg-program: #2c3e50;

$io-margin: 5px;

.node {
  background: rgba($bg-builtin, 0.85);
  border: 2px solid #2e2e2e;
  border-radius: 0.75rem;
  box-sizing: border-box;
  color: #2e2e2e;
  cursor: pointer;
  height: auto;
  min-width: 150px;
  padding-bottom: 10px;
  padding-top: 10px;
  position: relative;
  user-select: none;

  .content {
    display: table;
    width: 100%;

    .column {
      display: table-cell;
      white-space: nowrap;

      &:not(:last-child) {
        padding-right: 20px;
      }
    }
  }

  .control {
    padding: $socket-margin $socket-size * 0.5 + $socket-margin;
  }

  .input {
    margin-bottom: $io-margin;
    margin-top: $io-margin;
    text-align: left;
  }

  .output {
    margin-bottom: $io-margin;
    margin-top: $io-margin;
    text-align: right;
  }

  &.env {
    background: rgba($bg-env, 0.85);
    color: white;
  }

  &.program {
    background: rgba($bg-program, 0.85);
    color: white;
  }

  &:hover, &.selected {
    background: rgba(darken($bg-builtin, 10%), 0.85);

    &.env {
      background: rgba(darken($bg-env, 10%), 0.85);
    }

    &.program {
      background: rgba(darken($bg-program, 10%), 0.85);
    }
  }
}
</style>

<script>
import Socket from 'Socket.vue';
import VueRenderPlugin from 'rete-vue-render-plugin';

export default {
  mixins: [VueRenderPlugin.mixin],
  components: {
    Socket,
  },
  mounted() {
    // Register all control events, including custom ones.
    for (const control of this.controls()) {
      control.vueContext.$on('change-value', () => this.editor.trigger('controlchanged', control));

      for (const [key, value] of Object.entries(control.events)) {
        this.editor.on(key, value);
      }
    }
  },
};
</script>
