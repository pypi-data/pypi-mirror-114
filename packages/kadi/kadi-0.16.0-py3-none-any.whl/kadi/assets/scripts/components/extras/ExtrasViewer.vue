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
  <div>
    <div v-if="!nestedType">
      <div class="d-flex justify-content-between mb-2">
        <div>
          <slot></slot>
        </div>
        <div v-if="hasNestedType">
          <div class="btn-group">
            <button type="button"
                    class="btn btn-link text-muted py-0 pl-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, true)">
              <i class="fas fa-minus-square"></i> Collapse all
            </button>
            <button type="button"
                    class="btn btn-link text-muted py-0 pr-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, false)">
              <i class="fas fa-plus-square"></i> Expand all
            </button>
          </div>
        </div>
      </div>
    </div>
    <ul class="list-group mb-2">
      <li class="list-group-item extra py-1 pl-3 pr-0"
          :class="{'extra-nested': depth % 2 == 1}"
          v-for="(extra, index) in extras_"
          :key="extra.id">
        <div v-if="kadi.utils.isNestedType(extra.type)">
          <div class="row align-items-center" :class="{'mb-1': extra.value.length > 0 && !extra.isCollapsed}">
            <div :class="{'col-md-4': showToolbar, 'col-md-5': !showToolbar}">
              <collapse-item show-icon-class=""
                             hide-icon-class=""
                             :id="extra.id"
                             :is-collapsed="extra.isCollapsed"
                             @collapse="extra.isCollapsed = $event">
                <strong>{{ extra.key || `(${index + 1})` }}</strong>
              </collapse-item>
            </div>
            <div :class="{'col-md-4': showToolbar, 'col-md-5': !showToolbar}">
              <collapse-item show-icon-class=""
                             hide-icon-class=""
                             :id="extra.id"
                             :is-collapsed="extra.isCollapsed"
                             @collapse="extra.isCollapsed = $event"
                             v-if="extra.isCollapsed && extra.value.length > 0">
                <strong>{...}</strong>
              </collapse-item>
            </div>
            <div class="col-md-2 d-md-flex justify-content-end">
              <small class="text-muted" :class="{'mr-3': !showToolbar}">
                {{ extra.type | prettyTypeName | capitalize }}
              </small>
            </div>
            <div class="col-md-2 d-md-flex justify-content-end" v-if="showToolbar">
              <a title="Edit extra"
                 :class="toolbarBtnClasses"
                 :href="getEditLink(extra, index)"
                 v-if="editEndpoint">
                <i class="fas fa-pencil-alt"></i>
                <span class="d-md-none">Edit extra</span>
              </a>
            </div>
          </div>
          <div v-if="extra.value.length > 0">
            <div :id="extra.id" class="collapse show">
              <extras-viewer :extras="extra.value"
                             :edit-endpoint="editEndpoint"
                             :show-validation="showValidation"
                             :nested-type="extra.type"
                             :nested-keys="[...nestedKeys, extra.key || index]"
                             :depth="depth + 1">
              </extras-viewer>
            </div>
          </div>
        </div>
        <div v-if="!kadi.utils.isNestedType(extra.type)">
          <div class="row align-items-center">
            <div :class="{'col-md-4': showToolbar, 'col-md-5': !showToolbar}">
              {{ extra.key || `(${index + 1})` }}
            </div>
            <div :class="{'col-md-4': showToolbar, 'col-md-5': !showToolbar}">
              <span v-if="extra.value !== null">
                <span v-if="extra.type === 'date'">
                  <local-timestamp :timestamp="extra.value"></local-timestamp>
                </span>
                <span v-else>{{ extra.value }}</span>
              </span>
              <span v-if="extra.value === null">
                <em>null</em>
              </span>
              <span class="text-muted">{{ extra.unit }}</span>
            </div>
            <div class="col-md-2 d-md-flex justify-content-end">
              <small class="text-muted" :class="{'mr-3': !showToolbar}">
                {{ extra.type | prettyTypeName | capitalize }}
              </small>
            </div>
            <div class="col-md-2 d-md-flex justify-content-end" v-if="showToolbar">
              <a title="Edit extra"
                 :class="toolbarBtnClasses"
                 :href="getEditLink(extra, index)"
                 v-if="editEndpoint">
                <i class="fas fa-pencil-alt"></i>
                <span class="d-md-none">Edit extra</span>
              </a>
              <button type="button"
                      title="Toggle validation"
                      class="d-block d-md-inline"
                      :class="toolbarBtnClasses"
                      @click="extra.showValidation = !extra.showValidation"
                      v-if="showValidation && extra.validation">
                <i class="fas fa-chevron-up" v-if="extra.showValidation"></i>
                <i class="fas fa-chevron-down" v-else></i>
                <span class="d-md-none">Toggle validation</span>
              </button>
            </div>
          </div>
          <div class="mt-3" v-if="extra.showValidation">
            <div class="row text-muted mb-2 mb-md-0" v-for="(value, key) in extra.validation" :key="key">
              <div :class="{'col-md-4': showToolbar, 'col-md-5': !showToolbar}">{{ key | capitalize }}</div>
              <div :class="{'col-md-4': showToolbar, 'col-md-5': !showToolbar}">{{ value }}</div>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.extra {
  margin-right: -1px;
}

.extra-nested {
  background-color: #f2f2f2;
}
</style>

<script>
export default {
  data() {
    return {
      extras_: this.extras,
      isCollapsing: false,
    };
  },
  props: {
    extras: Array,
    editEndpoint: {
      type: String,
      default: null,
    },
    editParam: {
      type: String,
      default: 'key',
    },
    showValidation: {
      type: Boolean,
      default: false,
    },
    nestedType: {
      type: String,
      default: null,
    },
    nestedKeys: {
      type: Array,
      default: () => [],
    },
    depth: {
      type: Number,
      default: 0,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-sm text-muted py-0 px-0 px-md-2 mr-1';
    },
    showToolbar() {
      return this.editEndpoint !== null || this.showValidation;
    },
    hasNestedType() {
      for (const extra of this.extras_) {
        if (kadi.utils.isNestedType(extra.type)) {
          return true;
        }
      }
      return false;
    },
  },
  methods: {
    visitExtras(extras, callback) {
      extras.forEach((extra) => {
        callback(extra);
        if (kadi.utils.isNestedType(extra.type)) {
          this.visitExtras(extra.value, callback);
        }
      });
    },
    collapseExtras(extras, collapse) {
      this.isCollapsing = true;
      this.visitExtras(extras, (extra) => extra.isCollapsed = collapse);
      // Take the collapse cooldown into account.
      window.setTimeout(() => this.isCollapsing = false, 400);
    },
    getEditLink(extra, index) {
      const url = new URL(this.editEndpoint);
      const params = new URLSearchParams(url.search);

      for (const key of this.nestedKeys) {
        params.append(this.editParam, key);
      }
      params.append(this.editParam, extra.key || index);


      url.search = params;
      return url.toString();
    },
  },
  created() {
    this.visitExtras(this.extras_, (extra) => {
      extra.id = kadi.utils.randomAlnum();
      this.$set(extra, 'showValidation', false);
      this.$set(extra, 'isCollapsed', false);
    });
  },
};
</script>
