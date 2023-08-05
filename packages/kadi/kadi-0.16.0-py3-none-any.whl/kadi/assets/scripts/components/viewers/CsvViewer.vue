<!-- Copyright 2021 Karlsruhe Institute of Technology
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
    <div class="input-group input-group-sm">
      <input class="form-control" placeholder="Filter rows" :id="filterId" v-model.trim="filter">
      <clear-button :input-id="filterId" :input="filter" :small="true" @clear-input="filter = ''"></clear-button>
    </div>
    <small class="text-muted" v-if="encoding">{{ i18n.t('misc.detectedEncoding') }} {{ encoding.toUpperCase() }}</small>
    <div class="table-responsive mt-2">
      <table class="table table-sm table-bordered table-hover">
        <thead class="bg-light" v-if="hasHeader">
          <tr>
            <th v-for="(value, index) in filteredRows[0]" :key="index">
              <strong>
                <pre class="mb-0">{{ value }}</pre>
              </strong>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in hasHeader ? filteredRows.slice(1) : filteredRows" :key="rowIndex">
            <td v-for="(value, valueIndex) in row" :key="valueIndex">
              <pre class="mb-0">{{ value }}</pre>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filter: '',
      filterId: kadi.utils.randomAlnum(),
      filteredRows: [],
    };
  },
  props: {
    rows: Array,
    encoding: {
      type: String,
      default: null,
    },
    hasHeader: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    filter() {
      const filter = this.filter.toLowerCase();
      this.filteredRows = [];

      if (this.hasHeader) {
        this.filteredRows.push(this.rows[0]);
      }

      for (const row of this.hasHeader ? this.rows.slice(1) : this.rows) {
        for (const value of row) {
          if (value.toLowerCase().includes(filter)) {
            this.filteredRows.push(row);
            break;
          }
        }
      }
    },
  },
  mounted() {
    this.filteredRows = this.rows;
  },
};
</script>
