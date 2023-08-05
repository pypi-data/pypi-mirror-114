/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import RecordLinksGraph from 'scripts/lib/components/RecordLinksGraph.vue';

new Vue({
  el: '#vm',
  components: {
    RecordLinksGraph,
  },
  data: {
    currentTab: null,
    requestInProgress: false,
    visualizeLinks: false,
    renderLinksGraph: false,
    linkFilter: '',
  },
  watch: {
    visualizeLinks() {
      if (this.visualizeLinks) {
        // If we render the links graph component before it is shown, its size cannot be initialized correctly.
        this.renderLinksGraph = true;
      }
    },
  },
  methods: {
    changeTab(tab) {
      this.currentTab = tab;
    },
    downloadFiles() {
      this.requestInProgress = true;

      axios.post(kadi.js_resources.download_files_endpoint)
        .then(() => kadi.getNotifications())
        .catch((error) => {
          if (error.request.status === 429) {
            // Use the error message from the backend.
            kadi.alert(error.response.data.description, {type: 'info'});
          } else {
            kadi.alert(i18n.t('error.packageFiles'), {xhr: error.request});
          }
        })
        .finally(() => this.requestInProgress = false);
    },
    deleteFile(file) {
      if (!window.confirm(i18n.t('warning.deleteIdentifier', {identifier: file.name}))) {
        return;
      }

      this.$set(file, 'disabled', true);

      axios.delete(file._actions.delete)
        .then(() => {
          this.$refs.filesPagination.update();
          // Update the file revisions as well if they were loaded already.
          if (this.$refs.fileRevisionsPagination) {
            this.$refs.fileRevisionsPagination.update();
          }
          kadi.alert(i18n.t('success.deleteFile'), {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert(i18n.t('error.deleteFile'), {xhr: error.request});
          file.disabled = false;
        });
    },
  },
});
